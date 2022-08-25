"""
Models for working with SNS topics
"""
from datetime import datetime
from pydantic import BaseModel, Field


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
    Message: str
    Timestamp: datetime
    SignatureVersion: str = Field(..., min_length=1, max_length=3,
                                  regex=NUMBERSLETTERS_PLUS_DASH)
    Signature: str = Field(..., min_length=2, max_length=300)
    SigningCertURL: str = Field(..., min_length=2, max_length=300)
    UnsubscribeURL: str = Field(..., min_length=2, max_length=300)
