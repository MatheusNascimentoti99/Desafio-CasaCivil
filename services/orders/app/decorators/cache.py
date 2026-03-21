"""
Decorator-based Redis cache layer for the Orders service.

Provides two decorators that can be applied to FastAPI route handlers:
- @cached(prefix, ttl)           — cache-aside pattern for read endpoints
- @invalidates_cache(*patterns)  — active invalidation for write endpoints

The service layer remains completely untouched; caching is a cross-cutting
concern handled exclusively at the router level.

All Redis errors are logged and swallowed — the application never crashes
because of cache failures (graceful degradation).
"""

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

# ── Connection pool (module-level singleton) ─────────────────

_redis: aioredis.Redis | None = None


async def init_cache() -> None:
    """Create the Redis connection pool. Called once during app startup."""
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
    """Close the Redis connection pool. Called once during app shutdown."""
    global _redis
    if _redis is not None:
        await _redis.aclose()
        _redis = None
        logger.info("Redis connection closed")


# ── Internal helpers ─────────────────────────────────────────

def _is_dependency(param: inspect.Parameter) -> bool:
    """Return True if the parameter is injected by FastAPI's Depends()."""
    return hasattr(param.default, "dependency")


def _build_cache_key(prefix: str, func: Callable, kwargs: dict) -> str:
    """
    Build a cache key from the function's non-dependency arguments.

    Example:
        prefix="order", func(order_id=UUID, db=Depends, _user=Depends)
        → "order:3fa85f64-..."
    """
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
    """Delete all keys matching *pattern* using SCAN + UNLINK (non-blocking)."""
    if _redis is None:
        return
    cursor: int = 0
    while True:
        cursor, keys = await _redis.scan(cursor=cursor, match=pattern, count=100)
        if keys:
            await _redis.unlink(*keys)
        if cursor == 0:
            break


# ── Public decorators ────────────────────────────────────────

def cached(prefix: str, ttl: int):
    """
    Cache-aside decorator for **GET** route handlers.

    On cache hit  → returns a ``JSONResponse`` directly (fast path).
    On cache miss → calls the handler, serialises the result, stores it in
                    Redis with the given TTL, and returns normally.

    Usage::

        @router.get("/{order_id}", response_model=OrderResponse)
        @cached(prefix="order", ttl=60)
        async def get_order(order_id: uuid.UUID, db=Depends(get_db)):
            ...
    """

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            # If Redis is unavailable, skip caching entirely
            if _redis is None:
                return await func(*args, **kwargs)

            cache_key = _build_cache_key(prefix, func, kwargs)

            # 1. Try cache
            try:
                hit = await _redis.get(cache_key)
                if hit is not None:
                    return JSONResponse(content=json.loads(hit))
            except Exception:
                logger.warning("cache read failed for %s", cache_key, exc_info=True)

            # 2. Cache miss → call handler
            result = await func(*args, **kwargs)

            # 3. Store in cache
            try:
                encoded = jsonable_encoder(result)
                await _redis.set(cache_key, json.dumps(encoded, default=str), ex=ttl)
            except Exception:
                logger.warning("cache write failed for %s", cache_key, exc_info=True)

            return result

        return wrapper

    return decorator


def invalidates_cache(*patterns: str):
    """
    Cache invalidation decorator for **write** route handlers (POST, PATCH, …).

    After the handler executes successfully, deletes all Redis keys that match
    the given patterns.  Patterns support:

    - Wildcards:  ``"orders:list:*"``
    - Interpolation from handler kwargs: ``"order:{order_id}"``

    Usage::

        @router.patch("/{order_id}/status", response_model=OrderResponse)
        @invalidates_cache("order:{order_id}", "orders:list:*")
        async def patch_order_status(order_id: uuid.UUID, ...):
            ...
    """

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            result = await func(*args, **kwargs)

            if _redis is None:
                return result

            for pattern in patterns:
                try:
                    # Interpolate kwargs into pattern
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
