from __future__ import annotations
from typing import Dict
import json

from json_logging import datetime
from api.models.team import Team
from api.models.sns import MessageIn, SyncMessage
from api.services.notification_service import NOTIFICATION, NotificationService


class TeamBuilder:

    def __init__(self) -> None:
        self.name = 'my_team'

    def with_name(self, name: str):
        self.name = name
        return self

    def build(self) -> Team:
        return Team(name=self.name)


class SyncMessageBuilder:
    def __init__(self) -> None:
        self.team_name = 'my_team'

    def with_team_name(self, team_name: str) -> SyncMessageBuilder:
        self.team_name = team_name
        return self

    def build(self) -> SyncMessage:
        return SyncMessage(Sync=self.team_name)


class MessageBuilder:
    def __init__(self) -> None:
        self.message_type = NOTIFICATION
        self.message_id = '1234'
        self.topic_arn = 'my-arn'
        self.message = SyncMessageBuilder().build()
        self.time_stamp = datetime.now()
        self.signature_version = '1'
        self.signature = 'my-signature'
        self.signing_cert_url = 'http://example.com'
        self.unsubscribe_url = 'http://unsubscribe.com'

    def with_message_type(self, message_type: str) -> MessageBuilder:
        self.message_type = message_type
        return self

    def with_sync_message(self, message: SyncMessage) -> MessageBuilder:
        self.message = message
        return self

    def build(self) -> MessageIn:
        return MessageIn(
                Type=self.message_type,
                MessageId=self.message_id,
                TopicArn=self.topic_arn,
                Message=self.message,
                Timestamp=self.time_stamp,
                SignatureVersion=self.signature_version,
                Signature=self.signature,
                SigningCertURL=self.signing_cert_url,
                UnsubscribeURL=self.unsubscribe_url
                )
