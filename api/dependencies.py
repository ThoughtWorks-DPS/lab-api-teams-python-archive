"""
Contains service objects for dependency injection
"""
from api.services.notification_service import NotificationService
from api.services.team_service import TeamService

# pylint: disable=missing-function-docstring
def get_team_service() -> TeamService:
    return TeamService()

# pylint: disable=missing-function-docstring
def get_notification_service() -> NotificationService:
    return NotificationService(team_service=get_team_service())
