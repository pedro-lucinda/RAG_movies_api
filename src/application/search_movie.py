from typing import List
from src.domain.repository import MovieRepository
from src.domain.movie import Movie

def search_movies(
    repository: MovieRepository,
    query: str,
    n_results: int = 1
) -> List[Movie]:
    """Search for movies by query text."""

    if not query or not query.strip():
        raise ValueError("Query is required")
    
    if n_results < 1:
        raise ValueError("Number of results must be greater than 0")
    
    return repository.search(query, n_results)