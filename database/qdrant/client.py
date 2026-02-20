"""Qdrant vector database client — search and manage collections."""

import os
from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance, VectorParams, PointStruct,
    Filter, FieldCondition, MatchValue
)
from dotenv import load_dotenv

from .embeddings import get_embedding, VECTOR_SIZE

load_dotenv()

QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")

# Collection names
KNOWLEDGE_COLLECTION = "yael_knowledge"
CONVERSATIONS_COLLECTION = "yael_conversations"
FACTS_COLLECTION = "yael_facts"

ALL_COLLECTIONS = [KNOWLEDGE_COLLECTION, CONVERSATIONS_COLLECTION, FACTS_COLLECTION]


class QdrantManager:
    """Manages Qdrant collections for the Yael bot."""

    def __init__(self):
        self.client = QdrantClient(url=QDRANT_URL)

    def ensure_collections(self):
        """Create collections if they don't exist."""
        existing = {c.name for c in self.client.get_collections().collections}
        for name in ALL_COLLECTIONS:
            if name not in existing:
                self.client.create_collection(
                    collection_name=name,
                    vectors_config=VectorParams(size=VECTOR_SIZE, distance=Distance.COSINE),
                )
                print(f"[OK] Collection created: {name}")
            else:
                print(f"[EXISTS] Collection: {name}")

    def upsert_point(self, collection: str, point_id: int, text: str, payload: dict):
        """Insert or update a single point with its embedding."""
        vector = get_embedding(text)
        self.client.upsert(
            collection_name=collection,
            points=[
                PointStruct(id=point_id, vector=vector, payload=payload)
            ],
        )

    def upsert_points_batch(self, collection: str, items: list[dict]):
        """Batch upsert: each item needs 'id', 'text', 'payload'."""
        from .embeddings import get_embeddings_batch

        texts = [item["text"] for item in items]
        vectors = get_embeddings_batch(texts)

        points = [
            PointStruct(
                id=item["id"],
                vector=vec,
                payload=item["payload"],
            )
            for item, vec in zip(items, vectors)
        ]
        self.client.upsert(collection_name=collection, points=points)

    def search(
        self,
        collection: str,
        query: str,
        limit: int = 5,
        type_filter: str | None = None,
    ) -> list[dict]:
        """Semantic search in a collection. Returns list of payload dicts with score."""
        vector = get_embedding(query)

        query_filter = None
        if type_filter:
            query_filter = Filter(
                must=[FieldCondition(key="type", match=MatchValue(value=type_filter))]
            )

        results = self.client.query_points(
            collection_name=collection,
            query=vector,
            limit=limit,
            query_filter=query_filter,
        ).points

        return [
            {**point.payload, "score": point.score, "id": point.id}
            for point in results
        ]

    def get_collection_count(self, collection: str) -> int:
        """Get number of points in a collection."""
        info = self.client.get_collection(collection)
        return info.points_count
