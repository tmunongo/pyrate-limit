from time import sleep, time

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse


class TokenBucket:
    def __init__(self, capacity: int, rate: int, window: int = 60):
        self.capacity = capacity
        self.tokens = capacity
        self.refill_rate = rate / window
        self.last_refill = time()

    def allow_request(self) -> bool:
        now = time()
        elapsed = now - self.last_refill
        self.tokens = min(self.capacity, self.tokens + elapsed * self.refill_rate)
        self.last_refill = now

        if self.tokens >= 1:
            self.tokens -= 1
            return True
        return False

app = FastAPI()
bucket = TokenBucket(capacity=200, rate=10, window=10)

@app.middleware("http")
async def rate_limit(request: Request, call_next):
    if bucket.allow_request():
        return await call_next(request)
    else:
        return JSONResponse(
            status_code=429,
            content={"detail": "Too Many Requests"}
        )

@app.get("/")
async def root():
    return {"message": "Request successful!"}