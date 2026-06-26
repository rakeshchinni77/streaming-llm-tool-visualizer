from app.services.embeddings import EmbeddingService


class KnowledgeTool:
    def search_knowledge(self, query: str) -> dict:
        if not query:
            return {"title": "", "answer": ""}

        service = EmbeddingService()
        result = service.search(query)
        if not result:
            return {"title": "", "answer": ""}
        return result
