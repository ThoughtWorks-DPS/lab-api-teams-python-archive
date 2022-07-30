import os
from moto import mock_dynamodb
import boto3, json, pytest
from api.models.team import Team


from api.repositories.team_repository import TeamRepository


class TestTeamRepository:

    @pytest.fixture
    def mock_aws_creds(self):
        """Mocked AWS Credentials for moto."""
        os.environ["AWS_ACCESS_KEY_ID"] = "testing"
        os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
        os.environ["AWS_SECURITY_TOKEN"] = "testing"
        os.environ["AWS_SESSION_TOKEN"] = "testing"

    @pytest.fixture
    def mock_dynamodb(self, mock_aws_creds):
        with mock_dynamodb():
            conn = boto3.resource('dynamodb')
            yield conn

    @pytest.fixture
    def mock_dynamo_table(self, mock_dynamodb):

        with open('dynamodb_table_schema.json') as schema_file:
            dynamodb_table_schema = schema_file.read()

        schema = json.loads(dynamodb_table_schema)
        table = mock_dynamodb.create_table(
            TableName='teams',
            **schema
        )
        yield table
        table.delete()

    def test_put_team(self, mock_dynamo_table):
        repository = TeamRepository(mock_dynamo_table)
        test_team = Team(name="Patrick")

        repository.put(test_team)

        found_team = mock_dynamo_table.get_item(Key={'name': test_team.name})['Item']['name']
        assert found_team is not None
        assert test_team.name == found_team