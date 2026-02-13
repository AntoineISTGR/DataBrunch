"""Tests for tagging utility."""

from src.utils.tagging import extract_tags


def test_extract_tags_python():
    """Test tag extraction for Python-related content."""
    title = "New Python 3.12 Features"
    url = "https://example.com/python"
    tags = extract_tags(title, url)
    assert "python" in tags


def test_extract_tags_javascript():
    """Test tag extraction for JavaScript-related content."""
    title = "JavaScript Framework Updates"
    url = "https://example.com/js"
    tags = extract_tags(title, url)
    assert "javascript" in tags


def test_extract_tags_ai():
    """Test tag extraction for AI-related content."""
    title = "Machine Learning Breakthrough"
    url = "https://example.com/ai"
    tags = extract_tags(title, url)
    assert "machine learning" in tags or "ml" in tags


def test_extract_tags_cloud():
    """Test tag extraction for cloud-related content."""
    title = "AWS Lambda Updates"
    url = "https://example.com/aws"
    tags = extract_tags(title, url)
    assert "aws" in tags
    assert "cloud" in tags


def test_extract_tags_no_matches():
    """Test tag extraction with no matching keywords."""
    title = "Random Article About Nothing"
    url = "https://example.com/random"
    tags = extract_tags(title, url)
    assert isinstance(tags, list)
    assert len(tags) == 0


def test_extract_tags_multiple_matches():
    """Test tag extraction with multiple keywords."""
    title = "React and Vue.js Comparison for Frontend Development"
    url = "https://example.com/react-vue"
    tags = extract_tags(title, url)
    assert "react" in tags
    assert "vue" in tags
    assert "frontend" in tags


def test_extract_tags_case_insensitive():
    """Test that tag extraction is case-insensitive."""
    title = "PYTHON Programming Guide"
    url = "https://example.com/PYTHON"
    tags = extract_tags(title, url)
    assert "python" in tags


def test_extract_tags_no_duplicates():
    """Test that tags don't contain duplicates."""
    title = "Python Python Python"
    url = "https://example.com/python"
    tags = extract_tags(title, url)
    assert tags.count("python") == 1
