from litestar import Litestar
from litestar.config.cors import CORSConfig
from litestar.openapi.plugins import SwaggerRenderPlugin
from litestar.openapi import OpenAPIConfig
from src.infrastructure.config import settings
from src.api.v1.movie.route import search_movies, ingest_movies, chat_stream


def on_startup(app: Litestar) -> None:
    """Store settings in application state."""
    app.state.settings = settings


app = Litestar(
    route_handlers=[search_movies, ingest_movies, chat_stream],
    debug=True,
    on_startup=[on_startup],
    openapi_config=OpenAPIConfig(
        title="Movie Search",
        version="1.0.0",
        render_plugins=[SwaggerRenderPlugin()],
    ),
    cors_config=CORSConfig(
        allow_origins=["*"],
        allow_methods=["GET", "OPTIONS"],
        allow_headers=["*"],
        allow_credentials=True,
    ),
)