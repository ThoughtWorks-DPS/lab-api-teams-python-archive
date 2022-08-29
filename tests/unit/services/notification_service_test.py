
from unittest.mock import MagicMock
from api.services.notification_service import NOTIFICATION, NotificationService
from tests.util.builders import MessageBuilder, SyncMessageBuilder


def test_should_call_team_service_sync_all_teams_for_notifications_to_sync_all():
    mock_team_service = MagicMock()
    service = NotificationService(mock_team_service)

    service.handle(MessageBuilder().with_message_type(NOTIFICATION)
            .with_sync_message(SyncMessageBuilder().with_team_name('ALL').build())
            .build())

    mock_team_service.sync_all.assert_called()

def test_should_call_team_service_sync_with_team_name():
    mock_team_service = MagicMock()
    service = NotificationService(mock_team_service)

    service.handle(MessageBuilder().with_message_type(NOTIFICATION)
            .with_sync_message(SyncMessageBuilder().with_team_name('Team').build())
            .build())

    mock_team_service.sync.assert_called_with('Team')
