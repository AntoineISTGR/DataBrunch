"""FastAPI dependency functions."""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.modules.news.service import NewsService

# This will be set by main.py after initialization
_news_service = None


def set_news_service(service: "NewsService") -> None:  # type: ignore
    """
    Set the news service instance.

    This is called during application startup.

    Args:
        service: NewsService instance
    """
    global _news_service
    _news_service = service


def get_news_service() -> "NewsService":  # type: ignore
    """
    Dependency function to get the news service instance.

    Returns:
        NewsService instance

    Raises:
        RuntimeError: If service has not been initialized
    """
    if _news_service is None:
        raise RuntimeError("NewsService not initialized")
    return _news_service
