from collections import deque
from time import time

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse


class SlidingWindow:
    def __init__(self, limit: int, window_size: int):
        self.limit = limit  # max requests allowed
        self.window_size = window_size  # in seconds
        self.requests = deque()  # stores timestamp of each request
    
    def allow_request(self) -> bool:
        now = time()
        
        # Remove expired timestamps
        while self.requests and now - self.requests[0] > self.window_size:
            self.requests.popleft()
            
        # Check if under limit
        if len(self.requests) < self.limit:
            self.requests.append(now)
            return True
        return False

app = FastAPI()
limiter = SlidingWindow(limit=20, window_size=10)

@app.middleware("http")
async def rate_limit(request: Request, call_next):
    if limiter.allow_request():
        return await call_next(request)
    return JSONResponse(status_code=429, content={"detail": "Too Many Requests"})

@app.get("/")
async def root():
    return {"message": "Request successful!"}