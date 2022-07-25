"""
platform starter kit teams api

v1/teams            # list all teams
v1/teams/{team_id}  # get team by id
"""
from datetime import datetime
from fastapi import APIRouter, status
from ..config import settings

route = APIRouter()

@route.get("/{teamid}",
           summary="Return Team info by id.",
           tags=["teams"],
           status_code=status.HTTP_200_OK
           )
async def get_teams_teamid():
    """
    Returns 200 if service is running.
    """
    return {
      "status": "ok"
    }
