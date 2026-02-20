"""OpenAI embeddings helper for Qdrant vector search."""

import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

_client = None
MODEL = "text-embedding-3-small"
VECTOR_SIZE = 1536


def _get_client() -> OpenAI:
    global _client
    if _client is None:
        _client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    return _client


def get_embedding(text: str) -> list[float]:
    """Generate embedding vector for a text string."""
    client = _get_client()
    text = text.replace("\n", " ").strip()
    response = client.embeddings.create(input=[text], model=MODEL)
    return response.data[0].embedding


def get_embeddings_batch(texts: list[str]) -> list[list[float]]:
    """Generate embeddings for multiple texts in one API call."""
    client = _get_client()
    cleaned = [t.replace("\n", " ").strip() for t in texts]
    response = client.embeddings.create(input=cleaned, model=MODEL)
    return [item.embedding for item in response.data]
