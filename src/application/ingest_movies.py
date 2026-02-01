import logging
from src.domain.repository import MovieRepository
from src.domain.movie import Movie
from typing import List

logger = logging.getLogger(__name__)

def deduplicate_movies(movies_data: List[dict]) -> dict:
    unique_movies = {movie["Const"]: movie for movie in reversed(movies_data)}
    return dict(reversed(list(unique_movies.items())))

def ingest_movies(
    repository: MovieRepository,
    movies_data: List[dict],
    batch_size: int = 300
) -> dict:
    """
    Ingest movies into the repository with validation and type coercion.
    
    Validates essential fields (Const, Title) and skips invalid rows.
    Logs skipped rows with reasons.
    """
    skipped_count = 0
    skipped_reasons = []
    
    valid_movies_data = []
    for idx, movie_data in enumerate(movies_data, start=1):
        if not movie_data.get("Const"):
            skipped_count += 1
            reason = f"Row {idx}: Missing required field 'Const' (IMDb ID)"
            skipped_reasons.append(reason)
            logger.warning(reason)
            continue
        
        if not movie_data.get("Title"):
            skipped_count += 1
            reason = f"Row {idx} (ID: {movie_data.get('Const')}): Missing required field 'Title'"
            skipped_reasons.append(reason)
            logger.warning(reason)
            continue
        
        valid_movies_data.append(movie_data)
    
    unique_movies = deduplicate_movies(valid_movies_data)
    
    movies = []
    for imdb_id, movie_data in unique_movies.items():
        try:
            movies.append(
                Movie(
                    imdb_id=imdb_id,
                    title=movie_data.get("Title", ""),
                    data=movie_data
                )
            )
        except ValueError as e:
            skipped_count += 1
            reason = f"Movie {imdb_id}: {str(e)}"
            skipped_reasons.append(reason)
            logger.warning(reason)
            continue
    
    for i in range(0, len(movies), batch_size):
        batch = movies[i:i + batch_size]
        repository.upsert(batch)
    
    message = (
        f"{len(unique_movies)} unique movies ingested (from {len(movies_data)} rows)"
    )
    if skipped_count > 0:
        message += f", {skipped_count} rows skipped"
    
    return {
        "message": message,
        "total": len(unique_movies),
        "from_rows": len(movies_data),
        "skipped": skipped_count,
        "skipped_reasons": skipped_reasons if skipped_reasons else None
    }