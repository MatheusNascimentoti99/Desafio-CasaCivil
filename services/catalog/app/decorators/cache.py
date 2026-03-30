import functools
import inspect
import json
import logging
from typing import Any, Callable

import redis.asyncio as aioredis
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from app.config import settings

logger = logging.getLogger(__name__)

_redis: aioredis.Redis | None = None


async def init_cache() -> None:
    global _redis
    if not settings.CACHE_ENABLED:
        logger.info("Cache is disabled (CACHE_ENABLED=false)")
        return
    try:
        _redis = aioredis.from_url(
            settings.REDIS_URL,
            decode_responses=True,
            socket_connect_timeout=5,
        )
        await _redis.ping()
        logger.info("Redis connected at %s", settings.REDIS_URL)
    except Exception:
        logger.warning("Could not connect to Redis — cache disabled", exc_info=True)
        _redis = None


async def close_cache() -> None:
    global _redis
    if _redis is not None:
        await _redis.aclose()
        _redis = None
        logger.info("Redis connection closed")


def _is_dependency(param: inspect.Parameter) -> bool:
    return hasattr(param.default, "dependency")


def _build_cache_key(prefix: str, func: Callable, kwargs: dict) -> str:
    original = func.__wrapped__ if hasattr(func, "__wrapped__") else func
    sig = inspect.signature(original)

    parts = [prefix]
    for name, param in sig.parameters.items():
        if _is_dependency(param) or name.startswith("_"):
            continue
        value = kwargs.get(name, param.default)
        parts.append(str(value) if value is not None else "none")

    return ":".join(parts)


async def _delete_by_pattern(pattern: str) -> None:
    if _redis is None:
        return

    cursor: int = 0
    while True:
        cursor, keys = await _redis.scan(cursor=cursor, match=pattern, count=100)
        if keys:
            await _redis.unlink(*keys)
        if cursor == 0:
            break


def cached(prefix: str, ttl: int):
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            if _redis is None:
                return await func(*args, **kwargs)

            cache_key = _build_cache_key(prefix, func, kwargs)

            try:
                hit = await _redis.get(cache_key)
                if hit is not None:
                    return JSONResponse(content=json.loads(hit))
            except Exception:
                logger.warning("cache read failed for %s", cache_key, exc_info=True)

            result = await func(*args, **kwargs)

            try:
                encoded = jsonable_encoder(result)
                await _redis.set(cache_key, json.dumps(encoded, default=str), ex=ttl)
            except Exception:
                logger.warning("cache write failed for %s", cache_key, exc_info=True)

            return result

        return wrapper

    return decorator


def invalidates_cache(*patterns: str):
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            result = await func(*args, **kwargs)

            if _redis is None:
                return result

            for pattern in patterns:
                try:
                    resolved = pattern.format(**kwargs)

                    if "*" in resolved:
                        await _delete_by_pattern(resolved)
                    else:
                        await _redis.delete(resolved)
                except Exception:
                    logger.warning(
                        "cache invalidation failed for %s", pattern, exc_info=True
                    )

            return result

        return wrapper

    return decorator
