"""
Handle SNS Notifications
"""
from mypy_boto3_sns.service_resource import Topic
from api.models.sns import MessageIn
from api.services.team_service import TeamService


SUBSCRIPTION_CONFIRMATION = 'SubscriptionConfirmation'
NOTIFICATION = 'Notification'
SYNC_ALL_TEAMS = 'ALL'

# pylint: disable=too-few-public-methods
class NotificationService:
    """
    Service for managing SNS notifications both parsing and notifying
    """

    def __init__(self, team_service: TeamService, notification_client: Topic) -> None:
        self.team_service = team_service
        self.notification_client = notification_client

    def handle(self, message: MessageIn) -> None:
        """
        Take a message and determine if it's a notification or confirmation.
        For notifications it should determine whether to sync all teams or an
        individual team

        Args:
            message: (MessageIn) incoming message from SNS
                     Could be of Type Notification, or SubscriptionConfirmation
        """
        team_name = message.Message.Sync
        if team_name == SYNC_ALL_TEAMS:
            teams = self.team_service.get_all()
            for team in teams:
                self.notification_client.publish(team)

        else:
            self.team_service.sync(team_name)
