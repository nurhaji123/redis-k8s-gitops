import os

import redis
from fastapi import FastAPI, HTTPException, Request


app = FastAPI()

REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD")

HEALTH_PATHS = {
    "/health/live",
    "/health/ready",
}

r = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    password=REDIS_PASSWORD,
    socket_connect_timeout=1,
    socket_timeout=1,
)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    if request.url.path not in HEALTH_PATHS:
        print(f"Incoming request path: {request.url.path}")

    return await call_next(request)


@app.get("/")
def root():
    return {
        "message": "FastAPI is working"
    }


@app.get("/health/live")
def health_live():
    return {
        "status": "live"
    }


@app.get("/health/ready")
def health_ready():
    try:
        r.ping()
    except redis.RedisError as error:
        raise HTTPException(
            status_code=503,
            detail="Redis is unavailable",
        ) from error

    return {
        "status": "ready"
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
