"""
Track example naming for models
"""

from json_logging import datetime

from api.models.sns import MessageIn


EXAMPLE_TEAM_NAME = "team-name"
EXAMPLE_MESSAGE = MessageIn(
            Type="Notification",
            MessageId="1234-1515",
            TopicArn="example-arn",
            Message="This is a sample",
            Timestamp=datetime.now(),
            SignatureVersion="1",
            Signature = "asdf",
            SigningCertURL="http://example.com",
            UnsubscribeURL="http://unsubscribe.com"

        )
