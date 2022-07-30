from pydantic import BaseModel, Field

from api.models.examples import EXAMPLE_TEAM_NAME

class Team(BaseModel):
    name: str = Field(..., example=EXAMPLE_TEAM_NAME)