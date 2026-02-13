"""API route handlers."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import HTMLResponse

from src.modules.news.models import NewsResponse
from src.modules.news.service import NewsService
from src.server.dependencies import get_news_service
from src.server.templates import HTML_TEMPLATE
from src.utils.logging import get_logger

logger = get_logger(__name__)

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def home() -> HTMLResponse:
    """
    Home page with web interface for viewing news.

    Returns:
        HTML page with news interface
    """
    return HTMLResponse(content=HTML_TEMPLATE)


@router.get("/health")
async def health_check() -> dict[str, bool]:
    """
    Health check endpoint.

    Returns:
        Dictionary with "ok" status
    """
    return {"ok": True}


@router.get("/news", response_model=NewsResponse)
async def get_news(
    limit: Annotated[int, Query(ge=1, le=50, description="Number of news items to return")] = 20,
    news_service: NewsService = Depends(get_news_service),
) -> NewsResponse:
    """
    Get latest tech news from aggregated sources.

    Args:
        limit: Maximum number of news items to return (1-50, default 20)
        news_service: Injected news service instance

    Returns:
        NewsResponse with aggregated news items

    Raises:
        HTTPException: If the service fails to fetch news or is not initialized
    """
    try:
        return await news_service.get_latest_news(limit=limit)
    except RuntimeError as e:
        # Service not initialized
        logger.error(f"Service initialization error: {e}")
        raise HTTPException(
            status_code=503,
            detail="News service is not available. Please try again later."
        ) from e
    except Exception as e:
        # Log the full error for debugging
        logger.exception(f"Unexpected error fetching news: {e}")
        raise HTTPException(
            status_code=500,
            detail="Failed to fetch news. Please try again later."
        ) from e
