"""
Service for managing team CRUD
"""
from typing import List
from fastapi import status

from api.models.team import Team
from api.repositories.team_repository import TeamRepository
from api.routes.exceptions import ApiException

DUPLICATE_TEAM_TITLE = 'Team already exists'
DUPLICATE_TEAM_ERROR_DETAIL = 'Team %s already exists'


class TeamService():
    """Service for managing team CRUD"""
    def __init__(self, team_repository=None) -> None:
        if team_repository is None:
            self.repository = TeamRepository()
        else:
            self.repository = team_repository

    def create_team(self, team_name: str) -> Team:
        """
        Create a team

        Args:
            team_name (str): Name of the team to create

        Returns:
            a Team object with the given name

        Raises:
            ApiException: A team already exists, 409 Conflict
        """
        if self.repository.get(team_name) is None:
            new_team = Team(name=team_name)
            self.repository.put(new_team)
            return new_team
        raise ApiException(detail=DUPLICATE_TEAM_ERROR_DETAIL.format(team_name),
                           status_code=status.HTTP_409_CONFLICT,
                           title=DUPLICATE_TEAM_TITLE
                           )

    def delete_team(self, team_name:  str) -> bool:
        """
        Delete a team

        Args:
            team_name (str): Name of team to be deleted

        Returns:
            bool if the deletion was successful
        """
        self.repository.delete(team_name)
        return True

    def get_all(self) -> List[Team]:
        """
        Get all current teams

        Args:
            None

        Returns:
            A list of all teams in the repository
        """
        return self.repository.get_all()

    def get(self, team_name: str) -> Team:
        """
        Get a team

        Args:
            team_name (str): Name of team to be found

        Returns:
            Team if a team is found
            None if no team is found
        """
        return self.repository.get(team_name)
