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
        mock_team_service.get_teams.return_value = kwargs.get("get_teams")
        mock_team_service.get_team.return_value = kwargs.get("get_team")
        mock_team_service.update_team.return_value = kwargs.get("update_team")
        mock_team_service.create_team_namespace.return_value = kwargs.get("create_team_namespace")
        return mock_team_service

    return return_stubbed_team_service

class TestTeamsRoutes:
    def test_create_team_returns_201(self):
        team = Team(name='dps1')
        api.dependency_overrides[get_team_service] = mock_return_team_service(create_team=team)
        response = test_client.post('/v1/teams', json=team.dict())

        assert response.status_code == 201
        assert response.json()["name"] == team.name
