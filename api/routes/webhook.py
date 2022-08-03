"""
platform starter kit teams api

teams api liveness and readiness endpoints.
"""
from datetime import datetime
from fastapi import APIRouter, status
from pydantic import BaseModel, constr
from ..shared import logger

JSON_PATTERN = r'^\{\w+:\w+(,\w+:\w+)*\}$'
LETTERS_PLUS_DASH = r'^[a-zA-Z- ]+$'
NUMBERSLETTERS_PLUS_DASH = r'^[0-9a-zA-Z-]+$'

# pylint: disable=too-few-public-methods
class MessageIn(BaseModel, anystr_strip_whitespace=True, extra="forbid"):
    """schema for create-user input body"""
    type: constr(min_length=2, max_length=30, regex=LETTERS_PLUS_DASH)
    MessageId: constr(min_length=2, max_length=40, regex=NUMBERSLETTERS_PLUS_DASH)
    Subject: constr(min_length=2, max_length=30, regex=LETTERS_PLUS_DASH)
    Message: str
    Timestamp: datetime
    SignatureVersion: constr(min_length=2, max_length=3, regex=NUMBERSLETTERS_PLUS_DASH)
    Signature: constr(min_length=2, max_length=300, regex=LETTERS_PLUS_DASH)
    SigningCertURL: constr(min_length=2, max_length=300, regex=LETTERS_PLUS_DASH)
    UnsubscribeURL: constr(min_length=2, max_length=300, regex=LETTERS_PLUS_DASH)


route = APIRouter()

@route.post("/webhook/listener",
           summary="receives SNS messages.",
           tags=["webhook"],
           status_code=status.HTTP_200_OK
           )
async def get_healthz_liveness(message: MessageIn):
    """
    Returns 200 if service is running.
    """

    logger.info(message.Message)
    return message
