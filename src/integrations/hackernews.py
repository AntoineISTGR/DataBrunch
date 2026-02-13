"""Hacker News API integration."""

import asyncio

import httpx

from src.utils.logging import get_logger

logger = get_logger(__name__)

HN_API_BASE = "https://hacker-news.firebaseio.com/v0"


async def fetch_top_story_ids(limit: int = 50) -> list[int]:
    """
    Fetch top story IDs from Hacker News.

    Args:
        limit: Maximum number of story IDs to return

    Returns:
        List of story IDs
    """
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(f"{HN_API_BASE}/topstories.json")
            response.raise_for_status()
            all_ids = response.json()
            return all_ids[:limit]
    except Exception as e:
        logger.error(f"Failed to fetch Hacker News top stories: {e}")
        return []


async def fetch_story_details(story_id: int) -> dict | None:
    """
    Fetch detailed information for a Hacker News story.

    Args:
        story_id: Hacker News story ID

    Returns:
        Story details dictionary or None if fetch fails
    """
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(f"{HN_API_BASE}/item/{story_id}.json")
            response.raise_for_status()
            return response.json()
    except Exception as e:
        logger.warning(f"Failed to fetch Hacker News story {story_id}: {e}")
        return None


async def fetch_hackernews_news(limit: int = 50) -> list[dict]:
    """
    Fetch latest news from Hacker News.

    Args:
        limit: Maximum number of stories to fetch

    Returns:
        List of story dictionaries
    """
    story_ids = await fetch_top_story_ids(limit)
    if not story_ids:
        return []

    # Fetch story details concurrently
    tasks = [fetch_story_details(story_id) for story_id in story_ids]
    stories = await asyncio.gather(*tasks)

    # Filter out None values and stories without URLs (Ask HN, etc.)
    valid_stories = [
        story
        for story in stories
        if story is not None and story.get("type") == "story" and story.get("url")
    ]

    return valid_stories
