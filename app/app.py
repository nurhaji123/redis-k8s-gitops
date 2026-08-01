from fastapi import FastAPI, HTTPException, Request
import os

import redis


app = FastAPI()

REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD")

r = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    password=REDIS_PASSWORD,
)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    print(f"Incoming request path: {request.url.path}")
    return await call_next(request)


@app.get("/")
def root():
    return {
        "message": "FastAPI is working"
    }


@app.post("/cache")
def store_value(key: str, value: str):
    r.set(key, value)

    return {
        "message": f"Stored key '{key}'"
    }


@app.get("/cache")
def get_value(key: str):
    value = r.get(key)

    if value is None:
        raise HTTPException(
            status_code=404,
            detail="Key not found",
        )

    return {
        "key": key,
        "value": value.decode(),
    }
