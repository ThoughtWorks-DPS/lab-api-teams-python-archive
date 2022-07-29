from lib2to3.pytree import Base
from uuid import UUID
from pydantic import BaseModel, Field

from api.models.examples import EXAMPLE_TEAM_NAME

class Team(BaseModel):
    id: UUID = Field(..., example='b615579e-8ea5-4ca8-b9d1-7261bb48ead5')
    name: str = Field(..., example=EXAMPLE_TEAM_NAME)