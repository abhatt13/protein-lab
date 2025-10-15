import redis
from functools import wraps
import json
import pickle
from typing import Any, Callable, Optional
from app.core.config import get_settings

settings = get_settings()

try:
    redis_client = redis.from_url(settings.redis_url, decode_responses=False)
except:
    redis_client = None

def get_redis():
    return redis_client

def cache_result(expire: int = 300, key_prefix: str = ""):
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not redis_client:
                return func(*args, **kwargs)

            cache_key = f"{key_prefix}:{func.__name__}:{str(args)}:{str(kwargs)}"

            try:
                cached = redis_client.get(cache_key)
                if cached:
                    return pickle.loads(cached)
            except:
                pass

            result = func(*args, **kwargs)

            try:
                redis_client.setex(cache_key, expire, pickle.dumps(result))
            except:
                pass

            return result
        return wrapper
    return decorator

def invalidate_cache(pattern: str):
    if not redis_client:
        return

    try:
        keys = redis_client.keys(pattern)
        if keys:
            redis_client.delete(*keys)
    except:
        pass
