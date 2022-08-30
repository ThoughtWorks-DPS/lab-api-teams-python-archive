
from unittest.mock import MagicMock, call
from api.services.notification_service import NOTIFICATION, NotificationService
from tests.util.builders import MessageBuilder, SyncMessageBuilder, TeamBuilder


def test_sync_all_should_list_teams_and_notify_for_each():
    team1 = TeamBuilder().with_name('first_team').build()
    team2 = TeamBuilder().with_name('second_team').build()
    mock_team_service = MagicMock()
    mock_team_service.get_all.return_value = [team1, team2]
    mock_notification_client = MagicMock()
    service = NotificationService(team_service=mock_team_service,
                                  notification_client=mock_notification_client)
    sync_all_notification = MessageBuilder().with_message_type(NOTIFICATION).with_sync_message(
                                                SyncMessageBuilder()
                                                .with_team_name('ALL').build()
                                                ).build()
    service.handle(sync_all_notification)

    mock_notification_client.publish.assert_has_calls([call(team1), call(team2)], any_order=True)


def test_should_call_team_service_sync_with_team_name():
    mock_team_service = MagicMock()
    mock_sns_client = MagicMock()
    service = NotificationService(team_service=mock_team_service,
                                  notification_client=mock_sns_client)

    service.handle(MessageBuilder().with_message_type(NOTIFICATION)
            .with_sync_message(SyncMessageBuilder().with_team_name('Team').build())
            .build())

    mock_team_service.sync.assert_called_with('Team')
