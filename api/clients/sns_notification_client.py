from typing import Union
import boto3
from mypy_boto3_sns.service_resource import Topic
from api.models.sns import SyncMessage

from api.shared import settings


# pylint: disable=too-few-public-methods
class SnsNotificationClient:
    def __init__(self, sns_topic: Union[Topic, None]=None) -> None:
        if sns_topic is None:
            self.sns = boto3.resource('sns',
                    endpoint_url=settings.aws_endpoint).Topic(settings.topic_arn)
        else:
            self.sns = sns_topic

    def publish(self, message: SyncMessage):
        ...
