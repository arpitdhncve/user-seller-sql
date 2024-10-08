import redis
from fastapi import HTTPException

# Initialize Redis connection asynchronously
redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)


def save_token(email:str, token:str, expiry = 1800):
    try:
        redis_client.setex(email, expiry, token)
    except redis.RedisError as e:
        raise HTTPException(status_code=500, detail=str(e))


def get_token(email: str):
    try:
        return redis_client.get(email)
    except redis.RedisError as e:
        return None