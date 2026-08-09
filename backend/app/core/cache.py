import json
import time
from collections import defaultdict
from typing import Any, Optional
import redis.asyncio as redis
from app.core.config import settings
from app.core.logger import logger


class InMemoryFallbackCounter:
    """Bounded in-process rate limiter used when Redis is unreachable.
    
    Not shared across Cloud Run instances, but prevents any single
    instance from letting unlimited requests through during a Redis
    outage. This protects free-tier LLM API quotas from scrapers.
    """
    def __init__(self):
        self._counts: dict[str, int] = defaultdict(int)
        self._expiry: dict[str, float] = {}
    
    def increment(self, key: str, expire_seconds: int = 60) -> int:
        now = time.monotonic()
        # Reset if expired
        if key in self._expiry and now > self._expiry[key]:
            self._counts[key] = 0
        
        self._counts[key] += 1
        if key not in self._expiry or now > self._expiry[key]:
            self._expiry[key] = now + expire_seconds
        
        return self._counts[key]


class RedisCache:
    def __init__(self):
        self.redis = redis.from_url(settings.REDIS_URL, decode_responses=True)
        self._fallback = InMemoryFallbackCounter()
        self._redis_failures = 0
        
    async def get(self, key: str) -> Optional[Any]:
        try:
            val = await self.redis.get(key)
            if val:
                return json.loads(val)
        except Exception as e:
            logger.error("redis_get_error", key=key, error=str(e))
        return None
        
    async def set(self, key: str, value: Any, expire_seconds: int = 3600):
        try:
            await self.redis.set(key, json.dumps(value), ex=expire_seconds)
        except Exception as e:
            logger.error("redis_set_error", key=key, error=str(e))
            
    async def increment(self, key: str, expire_seconds: int = 60) -> int:
        try:
            pipe = self.redis.pipeline()
            pipe.incr(key)
            pipe.expire(key, expire_seconds)
            results = await pipe.execute()
            # Redis recovered — reset failure counter
            if self._redis_failures > 0:
                logger.info("redis_recovered", previous_failures=self._redis_failures)
                self._redis_failures = 0
            return results[0]
        except Exception as e:
            self._redis_failures += 1
            logger.error(
                "redis_increment_error",
                key=key,
                error=str(e),
                consecutive_failures=self._redis_failures,
            )
            # Fail-open WITH a ceiling: use an in-memory counter so
            # rate limiting still applies per-instance. This prevents
            # a Redis outage from turning off rate limiting entirely
            # and letting scrapers burn LLM API quotas.
            return self._fallback.increment(key, expire_seconds)
            
    async def close(self):
        await self.redis.close()

cache = RedisCache()
