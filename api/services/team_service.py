from fastapi import status

from api.models.team import Team
from api.repositories.team_repository import TeamRepository
from api.routes.exceptions import ApiException

DUPLICATE_TEAM_TITLE = 'Team already exists'
DUPLICATE_TEAM_ERROR_DETAIL = 'Team %s already exists'

class TeamService():
    def __init__(self, team_repository = TeamRepository()) -> None:
        self.repository = team_repository

    def create_team(self, team_name: str) -> Team:
        if self.repository.get(team_name) is None:
            new_team = Team(name=team_name)
            self.repository.put(new_team)
            return new_team
        else:
            raise ApiException(detail=DUPLICATE_TEAM_ERROR_DETAIL.format(team_name),
                                status_code=status.HTTP_409_CONFLICT,
                                title=DUPLICATE_TEAM_TITLE
             )
