import chromadb
import chromadb.utils.embedding_functions as embedding_functions
import sys
from pathlib import Path

# Add project root to path for imports
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from src.settings import settings

chroma_client = chromadb.Client()

openai_ef = embedding_functions.OpenAIEmbeddingFunction(
    api_key=settings.openai_api_key,
    model_name="text-embedding-3-small"
)
collection = chroma_client.create_collection(
    name=settings.chromadb_collection_name,
    embedding_function=openai_ef
)

