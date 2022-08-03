import pytest
from unittest.mock import MagicMock, patch

from api.models.team import Team
from api.routes.exceptions import ApiException
from api.services.team_service import TeamService


class TestsTeamService:
    def test_create_team_should_return_team(self):
        mock_dynamo_db = MagicMock()
        mock_dynamo_db.get.return_value = None
        service = TeamService(mock_dynamo_db)
        test_team_name = "dps1"

        new_team = service.create_team(test_team_name)

        assert type(new_team) is Team
        assert new_team.name == "dps1"

    def test_create_team_should_give_an_error_for_duplicate_team(self):
        existing_team = Team(name='existing_team')
        mock_dynamo_db = MagicMock()
        mock_dynamo_db.get.return_value = existing_team

        service = TeamService(mock_dynamo_db)

        with pytest.raises(ApiException):
            service.create_team('existing_team')
