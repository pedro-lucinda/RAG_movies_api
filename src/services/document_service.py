from src.services.chroma_db import ChromaDBService
from chromadb import Collection

class DocumentService:
    def __init__(self, collection: Collection):
        self.db_service = ChromaDBService(collection)

    def query_document(self, query: str, n_results: int = 1, include: list[str] = ['embeddings', 'documents', 'metadatas', 'distances']) -> list[dict]:
        return self.db_service.search(
            query=query,
            n_results=n_results, 
            include=include
        )

    def upsert_document(self, ids: list[str], documents: list[str]) -> None:
        return self.db_service.upsert_data(
            ids=ids,
            documents=documents,
        )