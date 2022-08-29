import json
from fastapi.testclient import TestClient
from api.dependencies import get_notification_service, get_team_service
from api.main import api
from api.models.examples import EXAMPLE_MESSAGE
from tests.util import mock_return_notification_service


test_client = TestClient(api)


def test_webhook_should_respond_with_200_with_valid_json():
    api.dependency_overrides[get_notification_service] = mock_return_notification_service()
    message = EXAMPLE_MESSAGE.dict()
    message['Timestamp'] = str(message['Timestamp'])
    response = test_client.post('v1/teams/webhook/listener', data=json.dumps(message),
                                headers={'content-type': 'text/plain'})
    assert response.status_code == 200


def test_webhook_should_respond_with_422_if_invalid_json():
    response = test_client.post('v1/teams/webhook/listener', json='{}',
                                headers={'content-type': 'text/plain'})
    assert response.status_code == 422
