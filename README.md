# Tech News Aggregator API

A production-quality FastAPI application that aggregates tech news from Hacker News and RSS feeds, **focused on Data Science, AI, Big Tech, and Agentic topics**. Returns normalized results with smart filtering and caching support.

## Features

- **Multi-source aggregation**: Fetches news from Hacker News Firebase API and multiple configurable RSS feeds
- **Smart filtering**: Automatically filters news to focus on Data Science, AI, Big Tech, and Agentic topics
- **Normalized output**: All news items are returned in a consistent schema
- **In-memory caching**: Async cache with configurable TTL to reduce API calls
- **Fault tolerance**: Returns partial results even if one source fails
- **Strong typing**: Full type hints and Pydantic v2 models
- **Comprehensive tests**: Unit tests for normalization, tagging, and cache behavior
- **Beautiful web interface**: Modern, responsive UI for browsing news

## Tech Stack

- Python 3.11+
- FastAPI
- Uvicorn
- httpx (async HTTP client)
- feedparser (RSS parsing)
- Pydantic v2
- pytest
- Ruff (linting)

## Project Structure

```
.
├── src/
│   ├── main.py                 # Application entry point
│   ├── server/
│   │   └── routes.py           # API route handlers
│   ├── modules/
│   │   └── news/
│   │       ├── models.py       # Pydantic models
│   │       └── service.py      # News aggregation service
│   ├── integrations/
│   │   ├── hackernews.py       # Hacker News API client
│   │   └── rss.py              # RSS feed client
│   └── utils/
│       ├── cache.py            # In-memory async cache
│       ├── tagging.py          # Tag extraction utility
│       └── logging.py          # Logging configuration
├── tests/
│   ├── test_cache.py           # Cache TTL tests
│   ├── test_tagging.py         # Tag extraction tests
│   └── test_normalization.py  # Normalization logic tests
├── requirements.txt
├── pyproject.toml
├── .env.example
└── README.md
```

## Setup Instructions

### Prerequisites

- Python 3.11 or higher
- pip (Python package installer)

### Step 1: Create Virtual Environment

Create a virtual environment using Python's built-in `venv`:

```bash
python -m venv .venv
```

### Step 2: Activate Virtual Environment

**On macOS/Linux:**
```bash
source .venv/bin/activate
```

**On Windows:**
```bash
.venv\Scripts\activate
```

After activation, you should see `(.venv)` in your terminal prompt.

### Step 3: Install Dependencies

Install all required packages:

```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables (Optional)

Copy the example environment file:

```bash
# On macOS/Linux
cp .env.example .env

# On Windows
copy .env.example .env
```

Edit `.env` to customize settings:

```env
# RSS Feed URLs (comma-separated, defaults to TechCrunch, The Verge, O'Reilly Radar, Wired if not set)
RSS_FEED_URLS=https://techcrunch.com/feed/,https://www.theverge.com/rss/index.xml

# Cache TTL in seconds (defaults to 60 if not set)
CACHE_TTL_SECONDS=60
```

**Note:** The aggregator now filters news to focus on Data Science, AI, Big Tech, and Agentic topics. Only relevant articles are displayed.

## Running the Application

Start the development server with auto-reload:

```bash
uvicorn src.main:app --reload
```

The API will be available at `http://localhost:8000`

**Web Interface:** Visit `http://localhost:8000` in your browser to see a beautiful web interface for viewing news.

API documentation (Swagger UI) is available at `http://localhost:8000/docs`

## Web Interface

Visit `http://localhost:8000` to access the web interface. The interface provides:

- **Beautiful card-based layout** for easy reading
- **Real-time news loading** from all sources
- **Configurable limit** for number of articles
- **Auto-refresh** every 60 seconds
- **Source indicators** (Hacker News / RSS)
- **Tags display** for each article
- **Direct links** to articles and comments
- **Responsive design** for mobile and desktop

## API Endpoints

### GET /

Web interface for viewing news in a user-friendly format.

**Example:**
Open `http://localhost:8000` in your browser.

### GET /health

Health check endpoint.

**Response:**
```json
{
  "ok": true
}
```

**Example:**
```bash
curl http://localhost:8000/health
```

### GET /news

Get latest tech news from aggregated sources.

**Query Parameters:**
- `limit` (optional): Number of news items to return (1-50, default: 20)

**Response:**
```json
{
  "items": [
    {
      "id": "hn_12345",
      "title": "Article Title",
      "url": "https://example.com/article",
      "source": "hackernews",
      "published_at": "2024-01-01T12:00:00",
      "score": 100,
      "comments_url": "https://news.ycombinator.com/item?id=12345",
      "tags": ["python", "tech"]
    }
  ],
  "meta": {
    "failed_sources": []
  }
}
```

**Examples:**
```bash
# Get default 20 news items
curl http://localhost:8000/news

# Get 10 news items
curl http://localhost:8000/news?limit=10

# Get maximum 50 news items
curl http://localhost:8000/news?limit=50
```

## Running Tests

Run all tests with pytest:

```bash
pytest
```

Run tests with verbose output:

```bash
pytest -v
```

Run a specific test file:

```bash
pytest tests/test_cache.py
```

## Linting

Check code style and quality with Ruff:

```bash
ruff check .
```

Auto-fix issues where possible:

```bash
ruff check . --fix
```

## Development

### Architecture Principles

- **Separation of concerns**: Business logic is in service layer, not route handlers
- **Strong typing**: All functions use type hints
- **Async/await**: Consistent use of async patterns throughout
- **No global state**: Except controlled cache instance
- **Small functions**: Each function has a single responsibility
- **Comprehensive docstrings**: All public functions are documented

### Adding New Sources

To add a new news source:

1. Create a new integration module in `src/integrations/`
2. Implement a fetch function that returns a list of raw news items
3. Add normalization logic in `NewsService._normalize_*_item()`
4. Update `NewsService._fetch_all_sources()` to include the new source

### Cache Behavior

- Cache key format: `news_limit_{limit}`
- Default TTL: 60 seconds (configurable via `CACHE_TTL_SECONDS`)
- Cache is cleared on application shutdown
- Expired entries are automatically removed on access

## Error Handling

The API is designed to be fault-tolerant:

- If Hacker News API fails, RSS results are still returned
- If RSS feed fails, Hacker News results are still returned
- Failed sources are indicated in the `meta.failed_sources` field
- Individual item fetch failures are logged but don't stop aggregation

## License

This project is provided as-is for educational and development purposes.
