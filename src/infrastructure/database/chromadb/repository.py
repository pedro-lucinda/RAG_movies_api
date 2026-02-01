from src.domain.repository import MovieRepository
from typing import List
from src.domain.movie import Movie
from chromadb import Collection

FIELD_MAPPING = {
    "Title": "title",
    "Original Title": "original_title",
    "URL": "url",
    "Title Type": "title_type",
    "IMDb Rating": "imdb_rating",
    "Runtime (mins)": "runtime_mins",
    "Year": "year",
    "Genres": "genres",
    "Num Votes": "num_votes",
    "Release Date": "release_date",
    "Directors": "directors",
    "Description": "description",
    "Your Rating": "your_rating",
    "Date Rated": "date_rated",
    "Position": "position",
    "Created": "created",
    "Modified": "modified",
}

# Reverse mapping for retrieval
REVERSE_FIELD_MAPPING = {v: k for k, v in FIELD_MAPPING.items()}


class ChromaDBMovieRepository(MovieRepository):
    def __init__(self, collection: Collection):
        self.collection = collection

    def search(self, query: str, n_results: int, include: list[str] = ['documents', 'metadatas', 'distances']) -> List[Movie]:
        """Search movies by query text."""
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results,
            include=include
        )
        
        ids = results.get("ids", [[]])[0] if "ids" in results and results["ids"] else []
        metadatas = results.get("metadatas", [[]])[0] if "metadatas" in results and results.get("metadatas") else []
        
        movies = []
        for imdb_id, metadata in zip(ids, metadatas):
            if metadata: 
                title = metadata.get("title", "") if isinstance(metadata, dict) else ""
                
                data = {}
                if isinstance(metadata, dict):
                    for meta_key, value in metadata.items():
                        if meta_key in REVERSE_FIELD_MAPPING:
                            csv_field = REVERSE_FIELD_MAPPING[meta_key]
                            data[csv_field] = value
                
                movies.append(
                    Movie(
                        imdb_id=imdb_id,
                        title=title,
                        data=data
                    )
                )
        
        return movies

    def upsert(self, movies: List[Movie]) -> None:
        """Upsert movies into the repository."""
        ids = []
        documents = []
        metadatas = []
        
        for movie in movies:
            ids.append(movie.imdb_id)
            documents.append(movie.data.get("Title", ""))
            
            metadata = {}
            
            for csv_field, meta_key in FIELD_MAPPING.items():
                value = movie.data.get(csv_field)
                if value is not None and value != "":
                    
                    if meta_key in ("imdb_rating", "your_rating"):
                        try:
                            metadata[meta_key] = float(value)
                        except (ValueError, TypeError):
                            metadata[meta_key] = str(value)
                    elif meta_key in ("year", "runtime_mins", "num_votes", "position"):
                        try:
                            metadata[meta_key] = int(value)
                        except (ValueError, TypeError):
                            metadata[meta_key] = str(value)
                    else:
                        metadata[meta_key] = str(value)
            
            metadatas.append(metadata)
        
        self.collection.upsert(
            ids=ids,
            documents=documents,
            metadatas=metadatas
        )

