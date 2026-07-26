import time
from collections import defaultdict
from fastapi import HTTPException, Request

class RateLimiter:
    def __init__(self, requests_per_minute: int = 20):
        self.requests_per_minute = requests_per_minute
        # Dictionary to store timestamps of requests per IP
        # Format: { "ip_address": [timestamp1, timestamp2, ...] }
        self.request_history: dict[str, list[float]] = defaultdict(list)

    def __call__(self, request: Request):
        # Extract client IP, fallback to 127.0.0.1 if not available
        client_ip = request.client.host if request.client else "127.0.0.1"
        now = time.time()
        
        # Get history for this IP
        history = self.request_history[client_ip]
        
        # Remove timestamps older than 60 seconds (1 minute window)
        # Using a list comprehension is fine since the lists are small (max ~20 items)
        self.request_history[client_ip] = [ts for ts in history if now - ts < 60.0]
        
        # Check if they have exceeded the limit
        if len(self.request_history[client_ip]) >= self.requests_per_minute:
            raise HTTPException(
                status_code=429,
                detail="Too Many Requests. Please wait a moment before trying again."
            )
            
        # Add the current request timestamp
        self.request_history[client_ip].append(now)
        return True

# Singleton instance for the dependency
rate_limiter = RateLimiter(requests_per_minute=20)
