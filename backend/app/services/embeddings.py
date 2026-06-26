import json
import os
from typing import Any

from sentence_transformers import SentenceTransformer


class EmbeddingService:
    _instance: "EmbeddingService | None" = None

    def __new__(cls) -> "EmbeddingService":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        if getattr(self, "_initialized", False):
            return

        base_dir = os.path.dirname(os.path.dirname(__file__))
        data_path = os.path.join(base_dir, "data", "knowledge_base.json")
        with open(data_path, "r", encoding="utf-8") as handle:
            self.documents = json.load(handle)

        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.document_embeddings = self._encode_documents()
        self._initialized = True

    def _encode_documents(self) -> list[list[float]]:
        texts = [doc.get("content", "") for doc in self.documents]
        embeddings = self.model.encode(texts, convert_to_numpy=False)
        if hasattr(embeddings, "tolist"):
            return embeddings.tolist()
        return [list(embedding) for embedding in embeddings]

    def search(self, query: str) -> dict[str, Any] | None:
        if not query:
            return None

        query_embeddings = self.model.encode([query], convert_to_numpy=False)
        if hasattr(query_embeddings, "tolist"):
            query_embedding = query_embeddings.tolist()[0]
        else:
            query_embedding = list(query_embeddings[0])
        best_doc = None
        best_score = -1.0

        for index, document in enumerate(self.documents):
            current_embedding = self.document_embeddings[index]
            score = self._cosine_similarity(query_embedding, current_embedding)
            if score > best_score:
                best_score = score
                best_doc = document

        if best_doc is None:
            return None

        return {
            "title": best_doc.get("title", ""),
            "answer": best_doc.get("content", ""),
        }

    @staticmethod
    def _cosine_similarity(left: list[float], right: list[float]) -> float:
        import math

        if not left or not right or len(left) != len(right):
            return 0.0

        dot_product = sum(a * b for a, b in zip(left, right))
        left_norm = math.sqrt(sum(a * a for a in left))
        right_norm = math.sqrt(sum(b * b for b in right))
        if left_norm == 0 or right_norm == 0:
            return 0.0
        return dot_product / (left_norm * right_norm)
