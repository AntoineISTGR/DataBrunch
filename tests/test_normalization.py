"""Tests for news item normalization logic."""

from datetime import datetime

from src.modules.news.models import NewsItem
from src.modules.news.service import NewsService
from src.utils.cache import AsyncCache


def test_normalize_hackernews_item():
    """Test normalization of Hacker News items."""
    cache = AsyncCache(ttl_seconds=60)
    service = NewsService(cache=cache, rss_feed_url="https://example.com/feed")

    hn_item = {
        "id": 12345,
        "title": "Test Article",
        "url": "https://example.com/article",
        "time": 1609459200,  # 2021-01-01 00:00:00 UTC
        "score": 100,
        "type": "story",
    }

    normalized = service._normalize_hackernews_item(hn_item)

    assert normalized is not None
    assert normalized.id == "hn_12345"
    assert normalized.title == "Test Article"
    assert str(normalized.url) == "https://example.com/article"
    assert normalized.source == "hackernews"
    assert normalized.score == 100
    assert normalized.comments_url is not None
    assert "12345" in str(normalized.comments_url)
    assert isinstance(normalized.published_at, datetime)
    assert isinstance(normalized.tags, list)


def test_normalize_hackernews_item_missing_fields():
    """Test normalization handles missing optional fields."""
    cache = AsyncCache(ttl_seconds=60)
    service = NewsService(cache=cache, rss_feed_url="https://example.com/feed")

    hn_item = {
        "id": 12345,
        "title": "Test Article",
        "url": "https://example.com/article",
        "time": 1609459200,
        "type": "story",
        # No score field
    }

    normalized = service._normalize_hackernews_item(hn_item)

    assert normalized is not None
    assert normalized.score is None


def test_normalize_rss_item():
    """Test normalization of RSS feed items."""
    cache = AsyncCache(ttl_seconds=60)
    service = NewsService(cache=cache, rss_feed_url="https://example.com/feed")

    rss_item = {
        "title": "RSS Article",
        "url": "https://example.com/rss-article",
        "published_at": datetime(2021, 1, 1, 12, 0, 0),
    }

    normalized = service._normalize_rss_item(rss_item, index=0)

    assert normalized is not None
    assert normalized.id.startswith("rss_")
    assert normalized.title == "RSS Article"
    assert str(normalized.url) == "https://example.com/rss-article"
    assert normalized.source == "rss"
    assert normalized.score is None
    assert normalized.comments_url is None
    assert normalized.published_at == datetime(2021, 1, 1, 12, 0, 0)
    assert isinstance(normalized.tags, list)


def test_normalize_rss_item_default_date():
    """Test normalization uses current time if date is missing."""
    cache = AsyncCache(ttl_seconds=60)
    service = NewsService(cache=cache, rss_feed_url="https://example.com/feed")

    rss_item = {
        "title": "RSS Article",
        "url": "https://example.com/rss-article",
        # No published_at
    }

    normalized = service._normalize_rss_item(rss_item, index=0)

    assert normalized is not None
    assert isinstance(normalized.published_at, datetime)


def test_normalize_invalid_item():
    """Test normalization handles invalid items gracefully."""
    cache = AsyncCache(ttl_seconds=60)
    service = NewsService(cache=cache, rss_feed_url="https://example.com/feed")

    # Invalid item missing required fields
    invalid_item = {}

    normalized = service._normalize_hackernews_item(invalid_item)
    assert normalized is None

    normalized = service._normalize_rss_item(invalid_item, index=0)
    assert normalized is None


def test_news_item_model_validation():
    """Test that NewsItem model validates correctly."""
    item = NewsItem(
        id="test_1",
        title="Test Title",
        url="https://example.com",
        source="hackernews",
        published_at=datetime.utcnow(),
        score=10,
        comments_url="https://news.ycombinator.com/item?id=1",
        tags=["python", "tech"],
    )

    assert item.id == "test_1"
    assert item.title == "Test Title"
    assert item.source == "hackernews"
    assert item.score == 10
    assert len(item.tags) == 2


def test_news_item_model_rss_source():
    """Test NewsItem with RSS source."""
    item = NewsItem(
        id="rss_1",
        title="RSS Title",
        url="https://example.com/rss",
        source="rss",
        published_at=datetime.utcnow(),
        score=None,
        comments_url=None,
        tags=[],
    )

    assert item.source == "rss"
    assert item.score is None
    assert item.comments_url is None
