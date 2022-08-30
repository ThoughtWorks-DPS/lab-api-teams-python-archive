"""
Holds the different clients to be used for sending notifications
"""
from typing import Union
import boto3
from mypy_boto3_sns.service_resource import Topic
from api.models.team import Team
from api.shared import settings, logger


# pylint: disable=too-few-public-methods
class SnsNotificationClient:
    """
    Client for publishing to AWS SNS

    Args:
        sns_topic: (Topic | None) the sns topic to be published to,
        otherwise it will be instantiated
    """
    def __init__(self, sns_topic: Union[Topic, None]=None) -> None:
        if sns_topic is None:
            self.sns = boto3.resource('sns',
                    endpoint_url=settings.aws_endpoint).Topic(settings.topic_arn)
        else:
            self.sns = sns_topic

    def publish(self, team: Team):
        """
        publish a team sync event to SNS

        Args:
            team: (Team) Individual team to be synced
        """
        logger.debug(team)
