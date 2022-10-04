import logging
from datetime import datetime, timedelta
from functools import lru_cache, wraps

import config


def timed_lru_cache(*args, seconds: int = config.default_cache_time, **kwargs):
    def wrapper_cache(func):
        func = lru_cache(*args, **kwargs)(func)
        func.lifetime = timedelta(seconds=seconds)
        func.expiration = datetime.utcnow() + func.lifetime

        @wraps(func)
        def wrapped_func(*args, **kwargs):
            if datetime.utcnow() >= func.expiration:
                logging.info(f"Clearing {func.__name__} cache.")
                func.cache_clear()
                func.expiration = datetime.utcnow() + func.lifetime
            return func(*args, **kwargs)

        return wrapped_func

    return wrapper_cache
