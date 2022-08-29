"""
Track example naming for models
"""

from json_logging import datetime

from api.models.sns import MessageIn, SyncMessage


EXAMPLE_TEAM_NAME = "team_name"
EXAMPLE_MESSAGE = MessageIn(
            Type="Notification",
            MessageId="1234-1515",
            TopicArn="example-arn",
            Message=SyncMessage(Sync='my_team'),
            Timestamp=datetime.now(),
            SignatureVersion="1",
            Signature = "my-signature",
            SigningCertURL="http://example.com",
            UnsubscribeURL="http://unsubscribe.com"

        )
