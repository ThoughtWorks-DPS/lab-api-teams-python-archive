"""
platform starter kit teams api

v1/teams/{team_id}  # get team by id
"""
from fastapi import APIRouter, Depends, status

from api.dependencies import get_team_service
from api.routes.exceptions import ApiException
from api.shared import logger
from api.models.team import Team, TeamResponse, team_responses

route = APIRouter()

NO_TEAM_ERROR_DETAIL = "Team %s was not found"
TEAM_NOT_FOUND_TITLE = "Team not found"


@route.get("/{team_name}",
           summary="Return team info by id.",
           tags=["teams"],
           status_code=status.HTTP_200_OK,
           response_model=TeamResponse
           )
async def get_teams_teamid(team_name: str,
                           team_service=Depends(get_team_service)):
    """
    Returns 200 if team is found
    """
    team = team_service.get(team_name)
    if team is None:
        raise ApiException(detail=NO_TEAM_ERROR_DETAIL.format(team_name),
                           status_code=status.HTTP_404_NOT_FOUND,
                           title=TEAM_NOT_FOUND_TITLE
                           )
    return TeamResponse(**team.dict())


@route.post("",
            summary="Create a new team.",
            tags=["teams"],
            status_code=status.HTTP_201_CREATED,
            responses={**team_responses},
            response_model=TeamResponse)
async def create_team(team: Team, team_service=Depends(get_team_service)):
    """
    Returns 201 if successfully created
    Returns 409 if team already exists with that name
    """
    logger.debug('Team Name: %s', team)
    created_team: Team = team_service.create_team(team.name)
    return TeamResponse(**created_team.dict())


@route.delete("/{team_name}",
              summary="Delete a team.",
              tags=["teams"],
              status_code=status.HTTP_204_NO_CONTENT)
async def delete_team(team_name: str, team_service=Depends(get_team_service)):
    """
    Returns 204 if successfully deleted
    """
    logger.debug('Deleting team: %s', team_name)
    team_service.delete_team(team_name)
    return {}
