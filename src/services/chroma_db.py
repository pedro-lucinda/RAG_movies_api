from chromadb import Collection

class ChromaDBService:
    def __init__(self, collection: Collection):
        self.collection = collection

    def search(self, query: str, n_results: int = 1, include: list[str] = ['embeddings', 'documents', 'metadatas', 'distances']) -> list[dict]:
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results, 
            include=include
        )
        return results

    def upsert_data(self, ids: list[str], documents: list[str]) -> None:
        self.collection.upsert(
            ids=ids,
            documents=documents,
        )
     