"""
platform starter kit teams api

Manages Team data and environment configurations for a platform.
"""
from fastapi import FastAPI
#from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from .routes import healthz, teams
from .config import settings, route_prefix

tags_metadata = [
    {
        "name": "teams",
        "description": "Return the list of all defined teams."
    }
]

api = FastAPI(
    title=settings.title,
    description=settings.description,
    version=settings.releaseId,
    openapi_tags=tags_metadata,
    docs_url=f"{route_prefix}/apidocs",
    openapi_url=f"{route_prefix}/openapi.json",
    redoc_url=None,
    debug=settings.debug
)

api.include_router(teams.route, prefix=route_prefix)
api.include_router(healthz.route, prefix=route_prefix)

@api.get(route_prefix, summary="list all teams", tags=["teams"])
async def root():
    """
    root endpoint.
    List all teams.
    """
    return { "message": "list teams" }

# FastAPIInstrumentor.instrument_app(api)
