"""
platform starter kit teams api

v1/teams/{team_id}  # get team by id
"""
import logging
from fastapi import APIRouter, Depends, status

from api.dependencies import get_team_service
from ..config import settings
from ..models.team import Team, TeamReponse, team_responses

route = APIRouter()

@route.get("/{teamid}",
           summary="Return team info by id.",
           tags=["teams"],
           status_code=status.HTTP_200_OK
           )
async def get_teams_teamid(teamid: str):
    """
    Returns 200 if service is running.
    """
    return {
      "status": "ok",
      "teamid": teamid
    }

@route.post("",
            summary="Create a new team.",
            tags=["teams"],
            status_code=status.HTTP_201_CREATED,
            responses={**team_responses},
            response_model=TeamReponse)
async def create_team(team: Team, team_service=Depends(get_team_service)):
    """
    Returns 201 if successfully created
    Returns 409 if team already exists with that name
    """
    logger = logging.getLogger(settings.logger)
    logger.debug('Team Name: %s', team)
    created_team: Team = team_service.create_team(team.name)
    return TeamReponse(name=created_team.name)
