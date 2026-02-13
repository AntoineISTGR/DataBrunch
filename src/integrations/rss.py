"""RSS feed integration."""

from datetime import datetime

import feedparser

from src.utils.logging import get_logger

logger = get_logger(__name__)


async def fetch_rss_news(feed_url: str, limit: int = 50) -> list[dict]:
    """
    Fetch latest news from an RSS feed.

    Args:
        feed_url: URL of the RSS feed
        limit: Maximum number of items to return

    Returns:
        List of feed entry dictionaries
    """
    try:
        import httpx

        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(feed_url)
            response.raise_for_status()
            feed = feedparser.parse(response.text)

            entries = []
            for entry in feed.entries[:limit]:
                # Parse published date
                published_at = None
                if hasattr(entry, "published_parsed") and entry.published_parsed:
                    try:
                        published_at = datetime(*entry.published_parsed[:6])
                    except (ValueError, TypeError):
                        pass

                # Fallback to current time if no date available
                if published_at is None:
                    published_at = datetime.utcnow()

                entries.append(
                    {
                        "title": entry.get("title", ""),
                        "url": entry.get("link", ""),
                        "published_at": published_at,
                    }
                )

            return entries
    except Exception as e:
        logger.error(f"Failed to fetch RSS feed from {feed_url}: {e}")
        return []
