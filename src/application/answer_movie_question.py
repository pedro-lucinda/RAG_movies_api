from typing import Iterator
from src.domain.repository import MovieRepository
from src.infrastructure.external.openai import OpenAIClient
from src.infrastructure.config import settings

def answer_movie_question(
    repository: MovieRepository,
    openai_client: OpenAIClient,
    question: str,
    n_context_results: int = 3,
    model: str = settings.openai_chat_model
) -> Iterator[str]:
    """
    Answer a movie question using RAG pattern.
    
    Args:
        repository: Movie repository for context retrieval
        openai_client: OpenAI client for streaming
        question: User's question
        n_context_results: Number of movies to retrieve as context
        model: OpenAI model to use
        
    Yields:
        Chunks of the streaming response
    """
    movies = repository.search(question, n_results=n_context_results)
    
    context = _format_movies_as_context(movies)
    
    system_prompt = (
        "You are a helpful movie assistant. "
        "Answer questions about movies using the provided context. "
        "If the context doesn't contain relevant information, say so."
    )
    
    yield from openai_client.stream_completion(
        question=question,
        context=context,
        model=model,
        system_prompt=system_prompt
    )


def _format_movies_as_context(movies: list) -> str:
    """Format movie entities into context string with all available fields."""
    if not movies:
        return "No relevant movies found in the database."
    
    context_parts = []
    for movie in movies:
        movie_info = f"IMDb ID: {movie.imdb_id}\n"
        
        priority_fields = [
            "Title", "Original Title", "Year", "Genres", "Description",
            "IMDb Rating", "Runtime (mins)", "Directors", "Release Date",
            "Title Type", "Num Votes", "URL", "Position", "Created", 
            "Modified", "Your Rating", "Date Rated"
        ]
        
        included = set()
        
        # Add priority fields first (if they exist and have values)
        for field in priority_fields:
            if field in movie.data and movie.data[field]:
                movie_info += f"{field}: {movie.data[field]}\n"
                included.add(field)
        
        # Include any remaining fields not in priority list
        for key, value in movie.data.items():
            if key not in included and value:
                movie_info += f"{key}: {value}\n"
        
        context_parts.append(movie_info)
    
    return "\n---\n".join(context_parts)