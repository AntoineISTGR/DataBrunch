"""Main application entry point."""

import os
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI

from src.modules.news.service import NewsService
from src.server.dependencies import set_news_service
from src.server.routes import router
from src.utils.cache import AsyncCache
from src.utils.logging import setup_logging

# Load environment variables
load_dotenv()

# Setup logging
setup_logging()

# Global cache instance (controlled singleton)
_cache: AsyncCache | None = None
_news_service: NewsService | None = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager.

    Initializes and cleans up resources.
    """
    global _cache, _news_service

    # Initialize cache
    cache_ttl = int(os.getenv("CACHE_TTL_SECONDS", "60"))
    _cache = AsyncCache(ttl_seconds=cache_ttl)

    # Initialize news service with multiple RSS feeds focused on AI, Data Science, and Big Tech
    rss_feed_urls_env = os.getenv("RSS_FEED_URLS", "")
    if rss_feed_urls_env:
        # Parse comma-separated list from environment
        rss_feed_urls = [url.strip() for url in rss_feed_urls_env.split(",") if url.strip()]
    else:
        # Default RSS feeds for AI, Data Science, and Big Tech
        rss_feed_urls = [
            "https://techcrunch.com/feed/",
            "https://www.theverge.com/rss/index.xml",
            "https://feeds.feedburner.com/oreilly/radar",
            "https://www.wired.com/feed/rss",
            "https://www.technologyreview.com/feed/",
        ]

    _news_service = NewsService(cache=_cache, rss_feed_urls=rss_feed_urls)

    # Set the service in dependencies module for route injection
    set_news_service(_news_service)

    yield

    # Cleanup
    if _cache:
        await _cache.clear()


# Create FastAPI app
app = FastAPI(
    title="Tech News Aggregator API",
    description="Aggregates tech news from Hacker News and RSS feeds",
    version="1.0.0",
    lifespan=lifespan,
)

# Include routes
app.include_router(router)
