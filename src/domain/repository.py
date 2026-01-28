from abc import ABC, abstractmethod
from typing import List
from src.domain.movie import Movie

class MovieRepository(ABC):
  @abstractmethod
  def search(self, query: str, n_results: int) -> List[Movie]:
    """ Search movies by query text. """
    pass
  @abstractmethod
  def upsert(self, movies: List[Movie]) -> None:
    """ Upsert movies into the repository. """
    pass