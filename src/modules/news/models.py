"""News data models."""

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field, HttpUrl


class NewsItem(BaseModel):
    """
    Normalized news item model.

    All news items from different sources are converted to this format.
    """

    id: str = Field(..., description="Unique identifier for the news item")
    title: str = Field(..., description="News item title")
    url: HttpUrl = Field(..., description="URL to the news item")
    source: Literal["hackernews", "rss"] = Field(
        ..., description="Source of the news item"
    )
    published_at: datetime = Field(..., description="Publication timestamp")
    score: int | None = Field(
        None, description="Score/points (Hacker News only)"
    )
    comments_url: HttpUrl | None = Field(
        None, description="URL to comments/discussion"
    )
    tags: list[str] = Field(
        default_factory=list, description="Extracted tags from title/URL"
    )


class NewsResponse(BaseModel):
    """Response model for the /news endpoint."""

    items: list[NewsItem] = Field(..., description="List of news items")
    meta: dict = Field(
        default_factory=dict,
        description="Metadata about the request (e.g., failed sources)",
    )
