"""
platform starter kit teams api

teams api liveness and readiness endpoints.
"""
from datetime import datetime
from fastapi import APIRouter, status, Response
from pydantic import BaseModel, constr
import logging
from ..config import settings
from ..shared import logger
import json

JSON_PATTERN = r'^\{\w+:\w+(,\w+:\w+)*\}$'
LETTERS_PLUS_DASH = r'^[a-zA-Z- ]+$'
NUMBERSLETTERS_PLUS_DASH = r'^[0-9a-zA-Z-]+$'

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
async def get_healthz_liveness(message: MessageIn, response: Response):
    """
    Returns 200 if service is running.
    """

    logger.info(message.Message)
    return message

# format of the received message
# {
#   "Type" : "Notification",
#   "MessageId" : "22b80b92-fdea-4c2c-8f9d-bdfb0c7bf324",
#   "TopicArn" : "arn:aws:sns:us-west-2:123456789012:MyTopic",
#   "Subject" : "My First Message",
#   "Message" : "Hello world!",
#   "Timestamp" : "2012-05-02T00:54:06.655Z",
#   "SignatureVersion" : "1",
#   "Signature" : "EXAMPLEw6JRN...",
#   "SigningCertURL" : "https://sns.us-west-2.amazonaws.com/SimpleNotificationService-f3ecfb7224c7233fe7bb5f59f96de52f.pem",
#   "UnsubscribeURL" : "https://sns.us-west-2.amazonaws.com/?Action=Unsubscribe&SubscriptionArn=arn:aws:sns:us-west-2:123456789012:MyTopic:c9135db0-26c4-47ec-8998-413945fb5a96"
# }