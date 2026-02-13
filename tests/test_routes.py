"""Tests for API route handlers."""

import pytest
from unittest.mock import AsyncMock, MagicMock

from fastapi.testclient import TestClient

from src.main import app
from src.server.dependencies import get_news_service


@pytest.fixture
def client():
    """Create a test client."""
    return TestClient(app)


@pytest.mark.asyncio
async def test_get_news_handles_service_error():
    """Test that endpoint handles service errors gracefully."""
    # Use FastAPI's dependency override
    mock_service = MagicMock()
    mock_service.get_latest_news = AsyncMock(side_effect=Exception("Service error"))
    
    app.dependency_overrides[get_news_service] = lambda: mock_service
    
    try:
        client = TestClient(app)
        response = client.get("/news?limit=10")

        assert response.status_code == 500
        assert "Failed to fetch news" in response.json()["detail"]
    finally:
        app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_get_news_handles_runtime_error():
    """Test that endpoint handles RuntimeError (service not initialized) with 503."""
    # Use FastAPI's dependency override
    mock_service = MagicMock()
    mock_service.get_latest_news = AsyncMock(
        side_effect=RuntimeError("Service not initialized")
    )
    
    app.dependency_overrides[get_news_service] = lambda: mock_service
    
    try:
        client = TestClient(app)
        response = client.get("/news?limit=10")

        assert response.status_code == 503
        assert "not available" in response.json()["detail"]
    finally:
        app.dependency_overrides.clear()


def test_get_news_validates_limit_range():
    """Test that limit parameter is validated correctly."""
    # Provide a mock service to avoid dependency initialization errors
    from unittest.mock import MagicMock, AsyncMock
    from src.modules.news.models import NewsResponse
    
    mock_service = MagicMock()
    mock_service.get_latest_news = AsyncMock(return_value=NewsResponse(items=[], meta={}))
    app.dependency_overrides[get_news_service] = lambda: mock_service
    
    try:
        client = TestClient(app)

        # Test limit too high - should be validation error (422)
        response = client.get("/news?limit=100")
        assert response.status_code == 422, "Limit > 50 should be rejected"
        assert "detail" in response.json()

        # Test limit too low - should be validation error (422)
        response = client.get("/news?limit=0")
        assert response.status_code == 422, "Limit < 1 should be rejected"
        assert "detail" in response.json()

        # Test valid limit - validation should pass
        response = client.get("/news?limit=10")
        # Should not be a validation error (422)
        assert response.status_code != 422, "Valid limit should not cause validation error"
    finally:
        app.dependency_overrides.clear()


def test_health_check():
    """Test health check endpoint."""
    client = TestClient(app)
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"ok": True}


def test_home_route():
    """Test home route returns HTML."""
    client = TestClient(app)
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
