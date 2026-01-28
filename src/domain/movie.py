from dataclasses import dataclass


@dataclass
class Movie:
  imdb_id: str
  title: str
  data: dict

  def __post_init__(self):
    if not self.imdb_id:
      raise ValueError("IMDb ID is required")
    if not self.title:
      raise ValueError("Title is required")
