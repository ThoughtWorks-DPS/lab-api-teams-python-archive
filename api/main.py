"""
platform starter kit teams api

Manages Team data and environment configurations for a platform.
"""
from fastapi import FastAPI, Depends
import json_logging
import boto3

from api.routes import exceptions
from .dependencies import get_team_service
from .routes import healthz, teams, webhook
from .config import settings, route_prefix
from .shared import logger

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

# @api.middleware("http")
# async def print_incoming_request(request: Request, call_next):
#     """change SNS notifications to have content-type as application/json"""
#     if request.headers.get('x-amz-sns-message-type') == 'Notification':
#         new_headers = request.headers.mutablecopy()
#         new_headers['content-type'] = 'application/json'
#         # pylint: disable=protected-access
#         request._headers = new_headers
#         request.scope.update(headers=request.headers.raw)
#     return await call_next(request)


if settings.subscribe_to_topic:
    client = boto3.client("sns", endpoint_url=settings.aws_endpoint, region_name="us-east-1")
    logger.debug("Subscribing to topic %s", settings.topic_arn)
    response = client.subscribe(
        TopicArn=settings.topic_arn,
        Protocol='http',
        Endpoint=settings.webhook_endpoint
    )

api.include_router(teams.route, prefix=route_prefix)
api.include_router(healthz.route, prefix=route_prefix)
api.include_router(webhook.route, prefix=route_prefix)
api.add_exception_handler(exceptions.RequestValidationError,
                          exceptions.custom_validation_exception_handler)


@api.get(route_prefix, summary="List all teams", tags=["teams"])
async def root(team_service=Depends(get_team_service)):
    """
    root endpoint.
    List all teams.
    """
    return team_service.get_all()

# FastAPIInstrumentor.instrument_app(api)
