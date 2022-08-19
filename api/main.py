"""
platform starter kit teams api

Manages Team data and environment configurations for a platform.
"""
from fastapi import FastAPI, Depends
import json_logging

from .dependencies import get_team_service
from .routes import healthz, teams, webhook
from .config import settings, route_prefix

tags_metadata = [
    {
        "name": "teams",
        "description": "Manage platform starter kit customer team data and configuration."
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
json_logging.init_fastapi(enable_json=True)
json_logging.init_request_instrument(api)

# client = boto3.client("sns", endpoint_url="http://localhost:4566", region_name="us-east-2")
# topic = client.create_topic(Name='TeamsEvents', Attributes={'FifoQueue': 'true'})
# response = client.subscribe(
#     TopicArn=topic['TopicArn'],
#     Protocol='http',
#     Endpoint='http://localhost:8000/v1/teams/webhook/listener',
# )

api.include_router(teams.route, prefix=route_prefix)
api.include_router(healthz.route, prefix=route_prefix)
api.include_router(webhook.route, prefix=route_prefix)

@api.get(route_prefix, summary="List all teams", tags=["teams"])
async def root(team_service=Depends(get_team_service)):
    """
    root endpoint.
    List all teams.
    """
    return team_service.get_all()

# FastAPIInstrumentor.instrument_app(api)
