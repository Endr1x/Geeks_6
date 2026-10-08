import redis
from django.conf import settings

redis_client = redis.Redis(
    host=getattr(settings, 'REDIS_HOST', '127.0.0.1'),
    port=getattr(settings, 'REDIS_PORT', 6379),
    db=getattr(settings, 'REDIS_DB', 0),
    decode_responses=True
)

def save_confirmation_code(email: str, code: str):
    redis_client.setex(f"confirmation:{email}", 300, code)

def get_confirmation_code(email: str) -> str:
    return redis_client.get(f"confirmation:{email}")

def delete_confirmation_code(email: str):
    redis_client.delete(f"confirmation:{email}")
