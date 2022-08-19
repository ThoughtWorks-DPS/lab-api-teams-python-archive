from unittest.mock import MagicMock
from fastapi.testclient import TestClient
from api.dependencies import get_team_service

from api.main import api
from api.models.team import Team

test_client = TestClient(api)

def mock_return_team_service(**kwargs):
    def return_stubbed_team_service():
        mock_team_service = MagicMock()
        mock_team_service.create_team.return_value = kwargs.get("create_team")
        mock_team_service.delete_team.return_value = kwargs.get("delete_team")
        mock_team_service.get_all.return_value = kwargs.get("get_all")
        return mock_team_service

    return return_stubbed_team_service

class TestTeamsRoutes:
    def test_create_team_returns_201(self):
        team = Team(name='dps1')
        api.dependency_overrides[get_team_service] = mock_return_team_service(create_team=team)
        response = test_client.post('/v1/teams', json=team.dict())

        assert response.status_code == 201
        assert response.json()["name"] == team.name

    def test_delete_team_returns_204(self):
        team = Team(name='dps1')
        api.dependency_overrides[get_team_service] = mock_return_team_service(delete_team=True)
        response = test_client.delete(f'/v1/teams/{team.name}')

        assert response.status_code == 204

    def test_root_lists_all_teams(self):
        team1 = Team(name='dps1')
        team2 = Team(name='dps2')

        api.dependency_overrides[get_team_service] = mock_return_team_service(get_all=[team1, team2])
        response = test_client.get('/v1/teams/')

        found_teams = response.json()
        assert len(found_teams) == 2
        assert team1 in found_teams
        assert team2 in found_teams
