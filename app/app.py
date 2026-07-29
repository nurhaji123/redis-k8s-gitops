from fastapi import FastAPI, HTTPException, Request
import redis
import os

app = FastAPI()

# Read Redis connection information from environment variables.
# These defaults are useful during development and later become
# Kubernetes ConfigMap/Secret values.

REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD")

# Create a Redis client.
# Note: we are not yet using the password. We will improve this
# in a later stage once Redis authentication is enabled.

r = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT
)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    print(f"Incoming request path: {request.url.path}")

    response = await call_next(request)

    return response


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
            detail="Key not found"
        )

    return {
        "key": key,
        "value": value.decode()
    }


@app.get("/secret-test")
def show_secret():

    return {
        "password": os.getenv("REDIS_PASSWORD")
    }