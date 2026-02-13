"""Tests for error handling in NewsService."""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from src.modules.news.service import NewsService
from src.utils.cache import AsyncCache


@pytest.fixture
def cache():
    """Create a cache instance for testing."""
    return AsyncCache(ttl_seconds=60)


@pytest.fixture
def service(cache):
    """Create a NewsService instance for testing."""
    return NewsService(cache=cache, rss_feed_urls=["https://example.com/feed"])


@pytest.mark.asyncio
async def test_get_latest_news_handles_cache_read_error(service):
    """Test that cache read errors are handled gracefully."""
    # Mock cache to raise an exception on get
    service._cache.get = AsyncMock(side_effect=Exception("Cache read error"))

    # Should not raise, should continue without cache
    with patch.object(service, "_fetch_all_sources", new_callable=AsyncMock) as mock_fetch:
        mock_fetch.return_value = ([], {"failed_sources": []})
        result = await service.get_latest_news(limit=10)

        assert result.items == []
        assert "failed_sources" in result.meta


@pytest.mark.asyncio
async def test_get_latest_news_handles_fetch_error(service):
    """Test that fetch errors return empty response with error metadata."""
    # Mock cache to return None (cache miss)
    service._cache.get = AsyncMock(return_value=None)
    service._cache.set = AsyncMock()

    # Mock fetch to raise an exception
    service._fetch_all_sources = AsyncMock(side_effect=Exception("Fetch error"))

    result = await service.get_latest_news(limit=10)

    assert result.items == []
    assert result.meta["failed_sources"] == ["all"]
    assert "error" in result.meta


@pytest.mark.asyncio
async def test_get_latest_news_handles_cache_write_error(service):
    """Test that cache write errors are handled gracefully."""
    # Mock cache
    service._cache.get = AsyncMock(return_value=None)
    service._cache.set = AsyncMock(side_effect=Exception("Cache write error"))

    # Mock successful fetch
    with patch.object(service, "_fetch_all_sources", new_callable=AsyncMock) as mock_fetch:
        mock_fetch.return_value = ([], {"failed_sources": []})
        result = await service.get_latest_news(limit=10)

        # Should still return result even if cache write fails
        assert result.items == []
        assert "failed_sources" in result.meta


def test_normalize_hackernews_item_filters_empty_url(service):
    """Test that items with empty URLs are filtered out."""
    item = {
        "id": 123,
        "title": "Test Story",
        "url": "",  # Empty URL
        "time": 1234567890,
        "score": 10,
    }

    result = service._normalize_hackernews_item(item)
    assert result is None


def test_normalize_rss_item_filters_empty_url(service):
    """Test that RSS items with empty URLs are filtered out."""
    item = {
        "title": "Test Article",
        "url": "",  # Empty URL
        "published_at": None,
    }

    result = service._normalize_rss_item(item, index=0)
    assert result is None


def test_normalize_hackernews_item_handles_missing_url(service):
    """Test that items with missing URL field are filtered out."""
    item = {
        "id": 123,
        "title": "Test Story",
        # No URL field
        "time": 1234567890,
        "score": 10,
    }

    result = service._normalize_hackernews_item(item)
    assert result is None


def test_normalize_rss_item_handles_missing_url(service):
    """Test that RSS items with missing URL field are filtered out."""
    item = {
        "title": "Test Article",
        # No URL field
        "published_at": None,
    }

    result = service._normalize_rss_item(item, index=0)
    assert result is None
