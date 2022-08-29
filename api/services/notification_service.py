"""
Handle SNS Notifications
"""
from api.models.sns import MessageIn
from api.services.team_service import TeamService


SUBSCRIPTION_CONFIRMATION = 'SubscriptionConfirmation'
NOTIFICATION = 'Notification'
SYNC_ALL_TEAMS = 'ALL'


class NotificationService:

    def __init__(self, team_service: TeamService) -> None:
        self.team_service = team_service

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
            self.team_service.sync_all()
        else:
            self.team_service.sync(team_name)
