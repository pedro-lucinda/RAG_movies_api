import chromadb
import chromadb.utils.embedding_functions as embedding_functions
from chromadb import Collection

from src.infrastructure.config import settings

chroma_client = chromadb.PersistentClient(path=settings.chroma_db_path)

openai_ef = embedding_functions.OpenAIEmbeddingFunction(
    api_key=settings.openai_api_key,
    model_name=settings.openai_embedding_model
)

def get_chromadb_collection() -> Collection:
    """Dependency provider for ChromaDB collection."""
    try:
        collection = chroma_client.get_collection(
            name=settings.chromadb_collection_name
        )
    except Exception:
        collection = chroma_client.create_collection(
            name=settings.chromadb_collection_name,
            embedding_function=openai_ef
        )
    return collection




