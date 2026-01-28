from pydantic import BaseModel, Field
from typing import List, Optional
from src.infrastructure.config import settings
from src.domain.movie import Movie
# Request Schemas
class SearchMoviesRequest(BaseModel):
    query: str = Field(..., description="Search query text", min_length=1)
    n_results: int = Field(default=1, ge=1, le=100, description="Number of results to return")

class IngestMoviesRequest(BaseModel):
    file_path: str = Field(..., description="Path to CSV file")

# Response Schemas
class MovieResponse(BaseModel):
    """Movie representation for API responses."""
    imdb_id: str
    title: Optional[str] = None  
    year: Optional[str] = None  
    data: dict 
    
    @classmethod
    def from_domain(cls, movie: Movie) -> 'MovieResponse':
        """Convert domain Movie entity to API response."""
        year = movie.data.get("Year")
        year_str = str(year) if year is not None and year != "" else None
        
        return cls(
            imdb_id=movie.imdb_id,
            title=movie.data.get("Title"),
            year=year_str,
            data=movie.data
        )

class SearchMoviesResponse(BaseModel):
    results: List[MovieResponse]
    count: int

class IngestMoviesResponse(BaseModel):
    message: str
    total: int
    from_rows: int
    skipped: Optional[int] = 0
    skipped_reasons: Optional[List[str]] = None


class ChatStreamRequest(BaseModel):
    question: str = Field(..., description="Message text", min_length=1)
    n_context_results: int = Field(default=3, ge=1, le=100, description="Number of context results to return")
    model: str = Field(default=settings.openai_chat_model, description="Model to use for the answer")

class ErrorResponse(BaseModel):
    """Error response schema."""
    error: str
    detail: Optional[str] = None
