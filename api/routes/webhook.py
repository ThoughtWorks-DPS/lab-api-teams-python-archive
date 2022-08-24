"""
platform starter kit teams api

teams api liveness and readiness endpoints.
"""
from datetime import datetime
from fastapi import APIRouter, status
from pydantic import BaseModel, Field, Json
from ..shared import logger

JSON_PATTERN = r'^\{\w+:\w+(,\w+:\w+)*\}$'
LETTERS_PLUS_DASH = r'^[a-zA-Z- ]+$'
NUMBERSLETTERS_PLUS_DASH = r'^[0-9a-zA-Z-]+$'


# pylint: disable=too-few-public-methods
class MessageIn(BaseModel, anystr_strip_whitespace=True):
    """schema for create-user input body"""
    Type: str = Field(..., min_length=2, max_length=30,
                      regex=LETTERS_PLUS_DASH)
    MessageId: str = Field(..., min_length=2, max_length=40,
                           regex=NUMBERSLETTERS_PLUS_DASH)
    TopicArn: str
    Message: Json
    Timestamp: datetime
    SignatureVersion: str = Field(..., min_length=1, max_length=3,
                                  regex=NUMBERSLETTERS_PLUS_DASH)
    Signature: str = Field(..., min_length=2, max_length=300)
    SigningCertURL: str = Field(..., min_length=2, max_length=300)
    UnsubscribeURL: str = Field(..., min_length=2, max_length=300)


route = APIRouter()


@route.post("/webhook/listener",
            summary="receives SNS messages.",
            tags=["webhook"],
            status_code=status.HTTP_200_OK
            )
async def listener(incoming_message: MessageIn):
    """
    Accepts SNS Message for teams updates
    """
    logger.info(incoming_message)
    return incoming_message.Message
