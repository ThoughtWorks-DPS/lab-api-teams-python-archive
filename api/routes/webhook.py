"""
platform starter kit teams api

teams api liveness and readiness endpoints.
"""
from fastapi import APIRouter, Body, status
from api.models.examples import EXAMPLE_MESSAGE

from api.shared import logger



route = APIRouter()


@route.post("/webhook/listener",
            summary="receives SNS messages.",
            tags=["webhook"],
            status_code=status.HTTP_200_OK
            )
async def listener(incoming_message: str = Body(
                                    ..., media_type='text/plain',
                   examples={
                       "normal": {
                           "summary": "Notification",
                           "value": EXAMPLE_MESSAGE.dict()
                           }
                       }
                   )):
    """
    Accepts SNS Message for teams updates
    """
    body = incoming_message
    logger.info(body)
    return body
