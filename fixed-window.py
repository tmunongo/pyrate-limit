from time import time

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse


class RateLimiter:
    def __init__(self, limit: int, window_size: int):
        self.limit = limit
        self.window_size = window_size
        self.requests = 0
        self.window_start = time()

    def allow_request(self) -> bool:
        now = time()
        # Reset window if expired
        if now - self.window_start > self.window_size:
            self.requests = 0
            self.window_start = now
        
        # Check if under limit
        if self.requests < self.limit:
            self.requests += 1
            return True
        return False

app = FastAPI()
limiter = RateLimiter(limit=20, window_size=10)

@app.middleware("http")
async def rate_limit(request: Request, call_next):
    if limiter.allow_request():
        return await call_next(request)
    return JSONResponse(
        status_code=429,
        content={"detail": "Too Many Requests"}
    )

@app.get("/")
def root():
    return {"message": "Request successful!"}