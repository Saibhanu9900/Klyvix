from fastapi import HTTPException, Request
from app.core.config import settings
from app.core.cache import cache

class RateLimiter:
    def __init__(self, requests_per_minute: int = 10, prefix: str = "rate_limit"):
        self.requests_per_minute = requests_per_minute
        self.prefix = prefix

    async def __call__(self, request: Request):
        # Extract client IP, fallback to 127.0.0.1 if not available
        client_ip = request.client.host if request.client else "127.0.0.1"
        key = f"{self.prefix}:{client_ip}"
        
        # Increment counter in Redis
        current_requests = await cache.increment(key, expire_seconds=60)
        
        # Check if they have exceeded the limit
        if current_requests > self.requests_per_minute:
            raise HTTPException(
                status_code=429,
                detail="Too Many Requests. Please wait a moment before trying again."
            )
            
        return True

# Singleton instances for dependencies
rate_limiter = RateLimiter(requests_per_minute=settings.RATE_LIMIT_PER_MINUTE, prefix="api_limit")
upload_limiter = RateLimiter(requests_per_minute=settings.UPLOAD_RATE_LIMIT, prefix="upload_limit")
