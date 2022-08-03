"""
Contains service objects for dependency injection
"""
from api.services.team_service import TeamService

# pylint: disable=missing-function-docstring
def get_team_service() -> TeamService:
    return TeamService()
