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

| Interface        | URL                                       |
| ---------------- | ----------------------------------------- |
| **Swagger UI**   | http://127.0.0.1:8000/schema              |
| **OpenAPI JSON** | http://127.0.0.1:8000/schema/openapi.json |

## Architecture

This project follows **Clean Architecture** principles, ensuring separation of concerns and maintainable code.

### Layers

```
┌─────────────────────────────────────────────────────────────┐
│                      API Layer                              │
│              (Routes, Schemas, SSE Utils)                   │
│         Handles HTTP requests, wires dependencies           │
└─────────────────────────┬───────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                  Application Layer                          │
│                     (Use Cases)                             │
│     Business logic orchestration, depends on abstractions   │
└─────────────────────────┬───────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                    Domain Layer                             │
│              (Entities, Ports/Interfaces)                   │
│          Core business rules, no external dependencies      │
└─────────────────────────────────────────────────────────────┘
                          ▲
                          │
┌─────────────────────────┴───────────────────────────────────┐
│                 Infrastructure Layer                        │
│         (Database, External APIs, File I/O, Config)         │
│            Implements domain interfaces (ports)             │
└─────────────────────────────────────────────────────────────┘
```

### Dependency Rule

Dependencies point **inward** toward the domain:

- **Domain** has no external dependencies
- **Application** depends only on Domain abstractions
- **Infrastructure** implements Domain interfaces
- **API** acts as the composition root, wiring everything together

### Project Structure

```
movie_search/
├── app.py                      # Application entry point
├── data/                       # Static data files
│   └── data.csv
├── scripts/                    # Utility scripts
│   └── ingest.py
└── src/
    ├── api/                    # API Layer (Presentation)
    │   ├── shared/             # Shared API utilities
    │   │   └── sse.py          # SSE formatting
    │   └── v1/movie/           # Versioned endpoints
    │       ├── route.py        # Route handlers
    │       └── schemas.py      # Request/Response schemas
    │
    ├── application/            # Application Layer (Use Cases)
    │   ├── answer_movie_question.py
    │   ├── ingest_movies.py
    │   └── search_movie.py
    │
    ├── domain/                 # Domain Layer (Core)
    │   ├── movie.py            # Movie entity
    │   ├── repository.py       # MovieRepository port
    │   └── llm.py              # LLMClient port
    │
    └── infrastructure/         # Infrastructure Layer
        ├── config.py           # Application settings
        ├── database/chromadb/
        │   ├── client.py       # ChromaDB connection
        │   └── repository.py   # MovieRepository implementation
        ├── external/
        │   └── openai.py       # LLMClient implementation
        └── file/
            └── read_csv.py     # File I/O utilities
```

## RAG Flow

The `/api/chat` endpoint uses Retrieval-Augmented Generation (RAG) to answer movie-related questions:

```
┌──────┐       ┌─────┐       ┌─────────────┐       ┌────────────┐
│ User │       │ API │       │ ChromaDBRepo│       │ OpenAIClient│
└──┬───┘       └──┬──┘       └──────┬──────┘       └─────┬──────┘
   │              │                 │                    │
   │  GET /api/chat?q=question      │                    │
   │─────────────>│                 │                    │
   │              │                 │                    │
   │              │ search(q, n=3)  │                    │
   │              │────────────────>│                    │
   │              │                 │                    │
   │              │                 │ Embed query with   │
   │              │                 │ OpenAI embeddings  │
   │              │                 │                    │
   │              │   List[Movie]   │                    │
   │              │<────────────────│                    │
   │              │                 │                    │
   │              │ Format context string                │
   │              │                 │                    │
   │              │ stream_completion(question, context) │
   │              │────────────────────────────────────>│
   │              │                 │                    │
   │              │                 │    SSE chunks      │
   │   data: ...  │<────────────────────────────────────│
   │<─────────────│                 │        ...         │
   │   data: ...  │<────────────────────────────────────│
   │<─────────────│                 │                    │
   │              │                 │                    │
   │ data: [DONE] │                 │                    │
   │<─────────────│                 │                    │
   │              │                 │                    │
```

1. **Retrieval**: The user's question is embedded using OpenAI and used to find semantically similar movies in ChromaDB
2. **Augmentation**: Retrieved movie metadata is formatted into a context string
3. **Generation**: The question and context are sent to OpenAI's chat model, which streams the response back via Server-Sent Events (SSE)
