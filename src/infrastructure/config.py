from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # OpenAI API configuration
    openai_api_key: str
    openai_embedding_model: str = "text-embedding-3-small"
    openai_chat_model: str = "gpt-4o-mini"
    
    # ChromaDB configuration
    chromadb_collection_name: str = "movies"
    chroma_db_path: str = "./chroma_db"
    
    # CSV configuration
    csv_path: str = "src/data/data.csv"
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

# Singleton instance
settings = Settings()