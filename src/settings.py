from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # OpenAI API configuration
    openai_api_key: str
    
    # ChromaDB configuration
    chromadb_collection_name: str = "movie-search"
    
    # Optional: specify .env file location
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )


# Create a singleton instance
settings = Settings()
