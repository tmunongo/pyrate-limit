import os
from time import time

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from redis import Redis


class RedisRateLimiter:
    def __init__(self, redis: Redis, limit: int, window: int):
        self.redis = redis
        self.limit = limit
        self.window = window
    
    def allow_request(self, client_id: str) -> bool:
        now = time()
        window_start = now - self.window
        key = f"rate:{client_id}"
        
        # First remove old requests
        self.redis.zremrangebyscore(key, 0, window_start)
        
        # Count remaining requests in window
        current_requests = self.redis.zcard(key)
        
        # If under limit, add new request
        if current_requests < self.limit:
            self.redis.zadd(key, {str(now): now})
            self.redis.expire(key, self.window)
            return True
            
        return False

app = FastAPI()
redis = Redis(host=os.getenv('REDIS_HOST', 'localhost'), port=6379, decode_responses=True)
limiter = RedisRateLimiter(redis, limit=1000, window=10)

@app.middleware("http")
async def rate_limit(request: Request, call_next):
    client_id = request.client.host
    if limiter.allow_request(client_id):
        return await call_next(request)
    return JSONResponse(status_code=429, content={"detail": "Too Many Requests"})

@app.get("/")
async def root():
    return {"message": "Request successful!"}

@app.get("/test")
async def test():
    return {
        "timestamp": time(),
        "instance": os.getenv('HOSTNAME', 'unknown')
    }