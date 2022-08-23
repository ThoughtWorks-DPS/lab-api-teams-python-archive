"""
Base models for teams
"""
from pydantic import BaseModel, Field

from api.models.examples import EXAMPLE_TEAM_NAME


# pylint: disable=too-few-public-methods,missing-class-docstring
class Team(BaseModel):
    name: str = Field(..., example=EXAMPLE_TEAM_NAME)


# pylint: disable=too-few-public-methods,missing-class-docstring
class TeamResponse(BaseModel):
    name: str = Field(..., exmaple=EXAMPLE_TEAM_NAME)


team_responses = {
    409: {"description": "Team name already exists"}
}
