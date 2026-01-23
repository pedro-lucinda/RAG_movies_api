from litestar import post
from src.file.prepare_data import prepare_data_for_upsert
from src.services.document_service import DocumentService
from src.settings import settings


@post("/search/{search_text:str}")
async def search_movies(search_text: str, n_results: int, include: list[str] ) -> dict:
    """Search for movies in the database."""
    document_service = DocumentService(settings.chromadb_collection_name)
    results = document_service.query_document(search_text, n_results, include)
    return results


@post("/ingest/{file_path:path}")
async def ingest_movies(file_path: str ) -> dict:
    """Ingest movies into the database."""
    data_to_upsert = prepare_data_for_upsert(file_path)
    document_service = DocumentService(settings.chromadb_collection_name)
    document_service.upsert_document(data_to_upsert["ids"], data_to_upsert["documents"])
    return {"message": "Movies ingested successfully"}