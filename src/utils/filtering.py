"""News filtering utility for data science, AI, Big Tech, and agentic content."""

import re


def is_relevant_news(title: str, url: str, tags: list[str]) -> bool:
    """
    Check if a news item is relevant to data science, AI, Big Tech, or agentic topics.

    Args:
        title: News item title
        url: News item URL
        tags: Extracted tags from the item

    Returns:
        True if the news is relevant, False otherwise
    """
    text = f"{title} {url}".lower()

    # If tags exist and contain relevant keywords, it's likely relevant
    relevant_tag_keywords = [
        "ai", "machine learning", "ml", "deep learning", "neural network",
        "llm", "large language model", "gpt", "chatgpt", "claude", "gemini",
        "transformer", "reinforcement learning", "computer vision", "nlp",
        "natural language processing", "generative ai", "genai", "agentic",
        "agent", "agents", "autonomous agent", "ai agent", "multi-agent",
        "langchain", "llama", "openai", "anthropic", "mistral",
        "data science", "data scientist", "data analytics", "data analysis",
        "data engineering", "data pipeline", "big data", "data warehouse",
        "data lake", "etl", "feature engineering", "model training",
        "model deployment", "mlops", "dataops", "pandas", "numpy",
        "scikit-learn", "tensorflow", "pytorch", "keras", "jupyter",
        "statistics", "data visualization", "data mining",
        "google", "microsoft", "amazon", "meta", "facebook", "apple", "nvidia",
        "tesla", "openai", "anthropic", "alphabet", "azure", "aws", "gcp",
        "google cloud", "amazon web services", "gpu", "cuda", "tpu",
        "quantum computing", "edge computing", "cloud computing",
        "distributed systems", "vector database", "embeddings", "rag",
        "retrieval augmented generation", "fine-tuning", "prompt engineering",
        "few-shot learning", "transfer learning"
    ]

    # Check if any relevant tag is present
    if tags:
        for tag in tags:
            if any(keyword in tag.lower() for keyword in relevant_tag_keywords):
                return True

    # Check title and URL for relevant keywords
    relevant_patterns = [
        r"\b(ai|artificial intelligence|machine learning|ml|deep learning)\b",
        r"\b(llm|large language model|gpt|chatgpt|claude|gemini)\b",
        r"\b(transformer|neural network|reinforcement learning)\b",
        r"\b(computer vision|nlp|natural language processing)\b",
        r"\b(generative ai|genai|agentic|agent|agents|autonomous agent)\b",
        r"\b(langchain|llama|openai|anthropic|mistral)\b",
        r"\b(data science|data scientist|data analytics|data engineering)\b",
        r"\b(big data|data warehouse|data lake|etl|mlops|dataops)\b",
        r"\b(tensorflow|pytorch|keras|scikit-learn|pandas|numpy)\b",
        r"\b(google|microsoft|amazon|meta|facebook|apple|nvidia|tesla)\b",
        r"\b(openai|anthropic|alphabet|azure|aws|gcp)\b",
        r"\b(gpu|cuda|tpu|quantum computing|edge computing)\b",
        r"\b(vector database|embeddings|rag|retrieval augmented generation)\b",
        r"\b(fine-tuning|prompt engineering|few-shot learning|transfer learning)\b",
    ]

    for pattern in relevant_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            return True

    return False
