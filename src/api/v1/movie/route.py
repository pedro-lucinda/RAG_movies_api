from litestar import get, post
from litestar.di import Provide
from litestar.response import Stream
from litestar.status_codes import HTTP_400_BAD_REQUEST, HTTP_500_INTERNAL_SERVER_ERROR
from litestar.exceptions import HTTPException
from chromadb import Collection
from src.infrastructure.file.read_csv import read_csv
from src.application.search_movie import search_movies as search_movies_use_case
from src.api.v1.movie.schemas import SearchMoviesResponse, MovieResponse, IngestMoviesRequest, IngestMoviesResponse
from src.api.shared.sse import sse_stream_iterator, create_error_stream, SSE_HEADERS
from src.infrastructure.config import settings
from src.infrastructure.database.chromadb.repository import ChromaDBMovieRepository
from src.infrastructure.database.chromadb.client import get_chromadb_collection
from src.application.ingest_movies import ingest_movies as ingest_movies_use_case
from src.application.answer_movie_question import answer_movie_question
from src.infrastructure.external.openai import OpenAIClient

@get(
    "/api/search",
    dependencies={"collection": Provide(get_chromadb_collection, sync_to_thread=False)},
    media_type="application/json"
)
async def search_movies(
    q: str,
    collection: Collection,
    n_results: int = 10
) -> SearchMoviesResponse:
    """Search for movies by query. Returns top 10 similar movies from ChromaDB."""
    if not q or not q.strip():
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail="Query parameter 'q' is required and cannot be empty"
        )
    
    try:
        repository = ChromaDBMovieRepository(collection)
        movies = search_movies_use_case(repository, q, n_results)
        
        return SearchMoviesResponse(
            results=[MovieResponse.from_domain(m) for m in movies],
            count=len(movies)
        )
    except ValueError as e:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )

@post(
    "/api/ingest",
    dependencies={"collection": Provide(get_chromadb_collection, sync_to_thread=False)}
)
async def ingest_movies(
    data: IngestMoviesRequest,
    collection: Collection
) -> IngestMoviesResponse:
    """Ingest movies into the database."""
    try:
        movies_data = read_csv(data.file_path)
    except FileNotFoundError:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail=f"File not found: {data.file_path}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error reading file: {str(e)}"
        )
    
    try:
        repository = ChromaDBMovieRepository(collection)
        
        result = ingest_movies_use_case(repository, movies_data)
        
        return IngestMoviesResponse(
            message=result["message"],
            total=result["total"],
            from_rows=result["from_rows"],
            skipped=result.get("skipped", 0),
            skipped_reasons=result.get("skipped_reasons")
        )
    except Exception as e:
        raise HTTPException(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error ingesting movies: {str(e)}"
        )

@get(
    "/api/chat",
    dependencies={"collection": Provide(get_chromadb_collection, sync_to_thread=False)},
)
async def chat_stream(
    q: str,
    collection: Collection,
    n_context_results: int = 3,
    model: str = settings.openai_chat_model
) -> Stream:
    """Stream AI-formulated answers using RAG with ChromaDB context via SSE."""
    if not q or not q.strip():
        return Stream(
            content=create_error_stream("Query parameter 'q' is required and cannot be empty"),
            media_type="text/event-stream",
            headers=SSE_HEADERS
        )
    
    repository = ChromaDBMovieRepository(collection)
    llm_client = OpenAIClient()
    
    stream_iterator = answer_movie_question(
        repository=repository,
        llm_client=llm_client,
        question=q,
        model=model,
        n_context_results=n_context_results
    )
    
    return Stream(
        content=sse_stream_iterator(stream_iterator),
        media_type="text/event-stream",
        headers=SSE_HEADERS
    )