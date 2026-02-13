"""In-memory async cache with TTL support."""

import asyncio
import time
from typing import Any, Optional, TypeVar

T = TypeVar("T")


class AsyncCache:
    """
    Thread-safe in-memory cache with TTL support.

    This cache stores key-value pairs with an expiration time.
    Expired entries are automatically removed on access.
    """

    def __init__(self, ttl_seconds: int = 60) -> None:
        """
        Initialize the cache.

        Args:
            ttl_seconds: Time-to-live in seconds for cache entries
        """
        self._cache: dict[str, tuple[Any, float]] = {}
        self._lock = asyncio.Lock()
        self._ttl_seconds = ttl_seconds

    async def get(self, key: str) -> Optional[T]:
        """
        Get a value from the cache if it exists and hasn't expired.

        Args:
            key: Cache key

        Returns:
            Cached value or None if not found or expired
        """
        async with self._lock:
            if key not in self._cache:
                return None

            value, expiry_time = self._cache[key]
            current_time = time.time()

            if current_time >= expiry_time:
                # Entry has expired, remove it
                del self._cache[key]
                return None

            return value

    async def set(self, key: str, value: T) -> None:
        """
        Store a value in the cache with TTL.

        Args:
            key: Cache key
            value: Value to cache
        """
        async with self._lock:
            expiry_time = time.time() + self._ttl_seconds
            self._cache[key] = (value, expiry_time)

    async def clear(self) -> None:
        """Clear all entries from the cache."""
        async with self._lock:
            self._cache.clear()

    async def _cleanup_expired(self) -> None:
        """
        Remove all expired entries from the cache.

        This is called automatically but can be invoked manually.
        """
        async with self._lock:
            current_time = time.time()
            expired_keys = [
                key
                for key, (_, expiry_time) in self._cache.items()
                if current_time >= expiry_time
            ]
            for key in expired_keys:
                del self._cache[key]
