# Movie Search API

A semantic movie search API built with Litestar and ChromaDB.

## Prerequisites

- Python 3.12+
- [uv](https://docs.astral.sh/uv/) package manager

## Setup

1. **Install dependencies:**

   ```bash
   uv sync
   ```

2. **Configure environment variables:**

   Create a `.env` file in the project root:

   ```bash
   OPENAI_API_KEY=your-openai-api-key
   CHROMADB_COLLECTION_NAME=movie-search  # optional, has default
   ```

## Running the Server

```bash
uv run litestar run --reload
```

## API Documentation

Once the server is running, access the interactive API docs at:

| Interface | URL |
|-----------|-----|
| **Swagger UI** | http://127.0.0.1:8000/schema |
| **OpenAPI JSON** | http://127.0.0.1:8000/schema/openapi.json |
