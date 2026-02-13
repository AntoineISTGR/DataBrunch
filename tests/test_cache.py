"""Tests for cache TTL expiration behavior."""

import asyncio

import pytest

from src.utils.cache import AsyncCache


@pytest.mark.asyncio
async def test_cache_set_and_get():
    """Test basic cache set and get operations."""
    cache = AsyncCache(ttl_seconds=60)
    await cache.set("key1", "value1")
    result = await cache.get("key1")
    assert result == "value1"


@pytest.mark.asyncio
async def test_cache_get_nonexistent():
    """Test getting a non-existent key returns None."""
    cache = AsyncCache(ttl_seconds=60)
    result = await cache.get("nonexistent")
    assert result is None


@pytest.mark.asyncio
async def test_cache_ttl_expiration():
    """Test that cache entries expire after TTL."""
    cache = AsyncCache(ttl_seconds=1)  # Very short TTL for testing
    await cache.set("key1", "value1")

    # Should be available immediately
    result = await cache.get("key1")
    assert result == "value1"

    # Wait for expiration
    await asyncio.sleep(1.1)

    # Should be expired now
    result = await cache.get("key1")
    assert result is None


@pytest.mark.asyncio
async def test_cache_clear():
    """Test clearing the cache."""
    cache = AsyncCache(ttl_seconds=60)
    await cache.set("key1", "value1")
    await cache.set("key2", "value2")

    await cache.clear()

    assert await cache.get("key1") is None
    assert await cache.get("key2") is None


@pytest.mark.asyncio
async def test_cache_concurrent_access():
    """Test that cache handles concurrent access correctly."""
    cache = AsyncCache(ttl_seconds=60)

    # Set multiple values concurrently
    await asyncio.gather(
        cache.set("key1", "value1"),
        cache.set("key2", "value2"),
        cache.set("key3", "value3"),
    )

    # Get multiple values concurrently
    results = await asyncio.gather(
        cache.get("key1"),
        cache.get("key2"),
        cache.get("key3"),
    )

    assert results == ["value1", "value2", "value3"]


@pytest.mark.asyncio
async def test_cache_overwrite():
    """Test that setting a key overwrites the previous value."""
    cache = AsyncCache(ttl_seconds=60)
    await cache.set("key1", "value1")
    await cache.set("key1", "value2")

    result = await cache.get("key1")
    assert result == "value2"


@pytest.mark.asyncio
async def test_cache_different_types():
    """Test that cache can store different types."""
    cache = AsyncCache(ttl_seconds=60)

    await cache.set("str", "string")
    await cache.set("int", 42)
    await cache.set("list", [1, 2, 3])
    await cache.set("dict", {"key": "value"})

    assert await cache.get("str") == "string"
    assert await cache.get("int") == 42
    assert await cache.get("list") == [1, 2, 3]
    assert await cache.get("dict") == {"key": "value"}
