# Simple Folder Structure

```
movie_search/
│
├── app.py                    # Litestar app entry point
├── pyproject.toml
├── README.md
│
└── src/
    │
    ├── domain/               # Business entities & interfaces
    │   ├── __init__.py
    │   ├── movie.py
    │   └── repository.py     # Abstract repository interface
    │
    ├── application/          # Use cases (business logic)
    │   ├── __init__.py
    │   ├── search_movies.py
    │   └── ingest_movies.py
    │
    ├── infrastructure/       # External services & database
    │   ├── __init__.py
    │   ├── database/
    │   │   └── chromadb.py   # ChromaDB client & repository impl
    │   ├── external/
    │   │   └── openai.py     # OpenAI client
    │   └── config.py         # Settings
    │
    └── api/                  # HTTP layer
        ├── __init__.py
        └── v1/
            └── movies/
                ├── __init__.py
                ├── routes.py      # Route handlers
                └── schemas.py     # Pydantic schemas
```

## What Goes Where

- **Domain**: Pure business logic, no external dependencies
- **Application**: Orchestrates use cases, depends on domain
- **Infrastructure**: Database, external APIs, config
- **API**: HTTP endpoints, request/response handling
