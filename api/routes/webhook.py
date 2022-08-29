"""
platform starter kit teams api

teams api liveness and readiness endpoints.
"""
from fastapi import APIRouter, Body, Depends, status
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
from api.dependencies import get_notification_service
from api.models.examples import EXAMPLE_MESSAGE
from api.models.sns import MessageIn
from api.services.notification_service import NotificationService

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
                   ),
                   notification_service: NotificationService = Depends(get_notification_service)):
    """
    Accepts SNS Message for teams updates
    """
    try:
        message = MessageIn.parse_raw(incoming_message)
        notification_service.handle(message)
    except ValidationError as ex:
        logger.info(ex.errors)
        print(ex.errors)
        raise RequestValidationError(ex.raw_errors) from ex
