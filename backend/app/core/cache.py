import json
from typing import Any, Optional
import redis.asyncio as redis
from app.core.config import settings
from app.core.logger import logger

class RedisCache:
    def __init__(self):
        self.redis = redis.from_url(settings.REDIS_URL, decode_responses=True)
        
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
            return results[0]
        except Exception as e:
            logger.error("redis_increment_error", key=key, error=str(e))
            # Fail-open: allow the request through when Redis is unavailable
            # (e.g. cold starts on serverless). A few unrate-limited requests
            # are better than a total outage for a demo app.
            return 1
            
    async def close(self):
        await self.redis.close()

cache = RedisCache()
