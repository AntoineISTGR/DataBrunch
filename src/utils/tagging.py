"""Tagging utility for news items."""

import re


def extract_tags(title: str, url: str) -> list[str]:
    """
    Extract tags from news item title and URL.

    Tags are extracted based on common tech keywords found in the title
    or URL. This is a simple keyword-based approach.

    Args:
        title: News item title
        url: News item URL

    Returns:
        List of extracted tags (lowercase, unique)
    """
    text = f"{title} {url}".lower()

    # Data Science, AI, Big Tech, and Agentic keywords
    keywords = [
        # AI & Machine Learning
        "ai",
        "artificial intelligence",
        "machine learning",
        "ml",
        "deep learning",
        "neural network",
        "neural networks",
        "llm",
        "large language model",
        "gpt",
        "chatgpt",
        "claude",
        "gemini",
        "transformer",
        "transformer model",
        "reinforcement learning",
        "rl",
        "computer vision",
        "nlp",
        "natural language processing",
        "generative ai",
        "genai",
        "agentic",
        "agent",
        "agents",
        "autonomous agent",
        "ai agent",
        "multi-agent",
        "langchain",
        "llama",
        "openai",
        "anthropic",
        "mistral",
        # Data Science
        "data science",
        "data scientist",
        "data analytics",
        "data analysis",
        "data engineering",
        "data pipeline",
        "big data",
        "data warehouse",
        "data lake",
        "etl",
        "feature engineering",
        "model training",
        "model deployment",
        "mlops",
        "dataops",
        "pandas",
        "numpy",
        "scikit-learn",
        "tensorflow",
        "pytorch",
        "keras",
        "jupyter",
        "notebook",
        "python",
        "r language",
        "statistics",
        "data visualization",
        "data mining",
        # Big Tech Companies
        "google",
        "microsoft",
        "amazon",
        "meta",
        "facebook",
        "apple",
        "nvidia",
        "tesla",
        "openai",
        "anthropic",
        "alphabet",
        "azure",
        "aws",
        "gcp",
        "google cloud",
        "amazon web services",
        # Related Technologies
        "gpu",
        "cuda",
        "tpu",
        "quantum computing",
        "edge computing",
        "cloud computing",
        "distributed systems",
        "vector database",
        "embeddings",
        "rag",
        "retrieval augmented generation",
        "fine-tuning",
        "prompt engineering",
        "few-shot learning",
        "transfer learning",
    ]

    found_tags: list[str] = []
    for keyword in keywords:
        # Use word boundaries to avoid partial matches
        pattern = r"\b" + re.escape(keyword) + r"\b"
        if re.search(pattern, text):
            found_tags.append(keyword)

    # Remove duplicates while preserving order
    return list(dict.fromkeys(found_tags))
