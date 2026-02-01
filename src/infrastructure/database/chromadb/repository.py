from src.domain.repository import MovieRepository
from typing import List
from src.domain.movie import Movie
from chromadb import Collection

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
                    if "title" in metadata:
                        data["Title"] = metadata["title"]
                    if "url" in metadata:
                        data["URL"] = metadata["url"]
                    if "imdb_rating" in metadata:
                        data["IMDb Rating"] = metadata["imdb_rating"]
                    if "year" in metadata:
                        data["Year"] = metadata["year"]
                
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
            
            title = movie.data.get("Title")
            if title:
                metadata["title"] = str(title)
            
            url = movie.data.get("URL")
            if url:
                metadata["url"] = str(url)
            
            imdb_rating = movie.data.get("IMDb Rating")
            if imdb_rating is not None and imdb_rating != "":
                try:
                    metadata["imdb_rating"] = float(imdb_rating)
                except (ValueError, TypeError):
                    pass
            
            year = movie.data.get("Year")
            if year is not None and year != "":
                try:
                    metadata["year"] = int(year)
                except (ValueError, TypeError):
                    pass
            
            metadatas.append(metadata)
        
        self.collection.upsert(
            ids=ids,
            documents=documents,
            metadatas=metadatas
        )

