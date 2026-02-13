"""News aggregation service."""

import asyncio
from datetime import datetime

from src.integrations.hackernews import fetch_hackernews_news
from src.integrations.rss import fetch_rss_news
from src.modules.news.models import NewsItem, NewsResponse
from src.utils.cache import AsyncCache
from src.utils.filtering import is_relevant_news
from src.utils.logging import get_logger
from src.utils.tagging import extract_tags

logger = get_logger(__name__)


class NewsService:
    """Service for aggregating and normalizing news from multiple sources."""

    def __init__(
        self,
        cache: AsyncCache,
        rss_feed_urls: list[str],
    ) -> None:
        """
        Initialize the news service.

        Args:
            cache: Cache instance for storing aggregated results
            rss_feed_urls: List of RSS feed URLs to fetch
        """
        self._cache = cache
        self._rss_feed_urls = rss_feed_urls if isinstance(rss_feed_urls, list) else [rss_feed_urls]

    def _normalize_hackernews_item(self, item: dict) -> NewsItem | None:
        """
        Normalize a Hacker News story to NewsItem format.

        Args:
            item: Raw Hacker News story dictionary

        Returns:
            Normalized NewsItem or None if conversion fails
        """
        try:
            # Hacker News uses Unix timestamps
            published_at = datetime.fromtimestamp(item.get("time", 0))

            # Build comments URL
            story_id = item.get("id")
            comments_url = (
                f"https://news.ycombinator.com/item?id={story_id}"
                if story_id
                else None
            )

            url = item.get("url", "")
            title = item.get("title", "")

            # Validate URL is not empty before creating NewsItem
            # Pydantic's HttpUrl will reject empty strings
            if not url or not url.strip():
                logger.warning(f"Skipping Hacker News item {story_id}: empty URL")
                return None

            return NewsItem(
                id=f"hn_{story_id}",
                title=title,
                url=url,
                source="hackernews",
                published_at=published_at,
                score=item.get("score"),
                comments_url=comments_url,
                tags=extract_tags(title, url),
            )
        except Exception as e:
            logger.warning(f"Failed to normalize Hacker News item: {e}")
            return None

    def _normalize_rss_item(self, item: dict, index: int) -> NewsItem | None:
        """
        Normalize an RSS feed entry to NewsItem format.

        Args:
            item: Raw RSS feed entry dictionary
            index: Index for generating unique ID

        Returns:
            Normalized NewsItem or None if conversion fails
        """
        try:
            url = item.get("url", "")
            title = item.get("title", "")

            # Validate URL is not empty before creating NewsItem
            # Pydantic's HttpUrl will reject empty strings
            if not url or not url.strip():
                logger.warning(f"Skipping RSS item at index {index}: empty URL")
                return None

            return NewsItem(
                id=f"rss_{index}_{hash(url)}",
                title=title,
                url=url,
                source="rss",
                published_at=item.get("published_at", datetime.utcnow()),
                score=None,
                comments_url=None,
                tags=extract_tags(title, url),
            )
        except Exception as e:
            logger.warning(f"Failed to normalize RSS item: {e}")
            return None

    async def _fetch_all_sources(self, limit: int) -> tuple[list[NewsItem], dict]:
        """
        Fetch news from all sources concurrently.

        Args:
            limit: Maximum number of items per source

        Returns:
            Tuple of (list of normalized news items, metadata dict)
        """
        meta: dict = {"failed_sources": []}

        # Fetch from all sources concurrently
        hn_task = asyncio.create_task(fetch_hackernews_news(limit * 2))  # Fetch more to filter

        # Fetch from all RSS feeds
        rss_tasks = [
            asyncio.create_task(fetch_rss_news(url, limit))
            for url in self._rss_feed_urls
        ]

        results = await asyncio.gather(
            hn_task, *rss_tasks, return_exceptions=True
        )

        hn_results = results[0]
        rss_results_list = results[1:]

        normalized_items: list[NewsItem] = []

        # Process Hacker News results
        if isinstance(hn_results, Exception):
            logger.error(f"Hacker News fetch failed: {hn_results}")
            meta["failed_sources"].append("hackernews")
        elif isinstance(hn_results, list):
            for item in hn_results:
                normalized = self._normalize_hackernews_item(item)
                if normalized and is_relevant_news(
                    normalized.title, str(normalized.url), normalized.tags
                ):
                    normalized_items.append(normalized)
        else:
            logger.warning(f"Unexpected Hacker News result type: {type(hn_results)}")
            meta["failed_sources"].append("hackernews")

        # Process RSS results from all feeds
        for feed_index, rss_results in enumerate(rss_results_list):
            feed_url = self._rss_feed_urls[feed_index] if feed_index < len(self._rss_feed_urls) else "unknown"
            if isinstance(rss_results, Exception):
                logger.error(f"RSS fetch failed for {feed_url}: {rss_results}")
                meta["failed_sources"].append(f"rss_{feed_index}")
            elif isinstance(rss_results, list):
                for item_index, item in enumerate(rss_results):
                    normalized = self._normalize_rss_item(item, feed_index * 1000 + item_index)
                    if normalized and is_relevant_news(
                        normalized.title, str(normalized.url), normalized.tags
                    ):
                        normalized_items.append(normalized)
            else:
                logger.warning(f"Unexpected RSS result type for {feed_url}: {type(rss_results)}")
                meta["failed_sources"].append(f"rss_{feed_index}")

        return normalized_items, meta

    async def get_latest_news(self, limit: int = 20) -> NewsResponse:
        """
        Get the latest news items from all sources.

        Results are cached and sorted by published_at descending.

        Args:
            limit: Maximum number of items to return (max 50)

        Returns:
            NewsResponse with items and metadata
        """
        # Enforce max limit
        limit = min(limit, 50)

        # Check cache (fail gracefully if cache fails)
        cache_key = f"news_limit_{limit}"
        try:
            cached = await self._cache.get(cache_key)
            if cached is not None:
                logger.debug(f"Returning cached news for limit={limit}")
                return cached
        except Exception as e:
            logger.warning(f"Cache read failed, continuing without cache: {e}")

        # Fetch from all sources
        try:
            items, meta = await self._fetch_all_sources(limit)
        except Exception as e:
            logger.error(f"Failed to fetch news from sources: {e}")
            # Return empty response rather than failing completely
            return NewsResponse(
                items=[],
                meta={"failed_sources": ["all"], "error": str(e)}
            )

        # Sort by published_at descending
        try:
            items.sort(key=lambda x: x.published_at, reverse=False)
        except Exception as e:
            logger.error(f"Failed to sort items: {e}")
            # Continue with unsorted items

        # Apply limit after sorting
        items = items[:limit]

        # Create response
        response = NewsResponse(items=items, meta=meta)

        # Cache the response (fail gracefully if cache fails)
        try:
            await self._cache.set(cache_key, response)
        except Exception as e:
            logger.warning(f"Cache write failed: {e}")

        return response
