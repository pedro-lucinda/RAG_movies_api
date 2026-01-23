from litestar import Litestar
from litestar.openapi.plugins import SwaggerRenderPlugin
from litestar.openapi import OpenAPIConfig
from litestar.datastructures import State
from src.settings import settings
from src.api.v1.movies.controller import search_movies, ingest_movies


def on_startup(app: Litestar) -> None:
    """Store settings in application state."""
    app.state.settings = settings


app = Litestar(
    route_handlers=[search_movies, ingest_movies],
    debug=True,
    on_startup=[on_startup],
    openapi_config=OpenAPIConfig(
        title="Movie Search",
        version="1.0.0",
        render_plugins=[SwaggerRenderPlugin()],
    ),
    
)