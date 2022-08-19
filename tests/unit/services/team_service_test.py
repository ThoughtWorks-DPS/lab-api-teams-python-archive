import pytest
from unittest.mock import MagicMock

from api.models.team import Team
from api.routes.exceptions import ApiException
from api.services.team_service import TeamService
from tests.util.builders import TeamBuilder


class TestsTeamService:
    def test_create_team_should_return_team(self):
        mock_team_repository = MagicMock()
        mock_team_repository.get.return_value = None
        service = TeamService(mock_team_repository)
        test_team_name = "dps1"

        new_team = service.create_team(test_team_name)

        assert isinstance(new_team, Team)
        assert new_team.name == "dps1"

    def test_create_team_should_give_an_error_for_duplicate_team(self):
        existing_team = Team(name='existing_team')
        mock_team_repository = MagicMock()
        mock_team_repository.delete_item.return_value = existing_team

        service = TeamService(mock_team_repository)

        with pytest.raises(ApiException):
            service.create_team('existing_team')

    def test_delete_team_should_remove_from_repository(self):
        existing_team_name = 'existing_team'
        mock_team_repository = MagicMock()
        mock_team_repository.delete.return_value = True

        service = TeamService(mock_team_repository)

        result = service.delete_team(existing_team_name)

        mock_team_repository.delete.assert_called_with(existing_team_name)
        assert result

    def test_get_all_should_query_the_repository_and_return_teams(self):
        mock_team_repository = MagicMock()
        team1 = TeamBuilder().with_name('dps1').build()
        team2 = TeamBuilder().with_name('dps1').build()
        mock_team_repository.get_all.return_value = [team1, team2]
        service = TeamService(mock_team_repository)

        teams = service.get_all()

        assert len(teams) == 2
        assert team1 in teams
        assert isinstance(teams[0], Team)
        assert team2 in teams
