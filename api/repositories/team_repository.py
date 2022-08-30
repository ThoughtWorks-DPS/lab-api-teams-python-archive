"""
Team Repository

Abstracts dynamodb interactions so that other areas of the API
don't need to be aware of the implementation
"""

from typing import List, Union
import boto3
from mypy_boto3_dynamodb.service_resource import Table

from api.config import settings
from api.models.team import Team

class TeamRepository:
    """
    Abstraction over DynamoDB for interacting with Team information
    Can take an aws resource for test mocking
    """
    def __init__(self, dynamo_db_table: Union[Table, None]=None):
        if dynamo_db_table is None:
            dynamodb = boto3.resource('dynamodb', endpoint_url=settings.aws_endpoint)
            self.table = dynamodb.Table(settings.dynamodb_table_name)
            self.table_name = settings.dynamodb_table_name
        else:
            self.table = dynamo_db_table
            self.table_name = dynamo_db_table.name

    def put(self, team: Team):
        """
        Create or update a team

        Args:
            team: an object represetnation of the team

        Returns:
            Nothing
        """
        self.table.put_item(Item=team.dict())

    def delete(self, team_name: str):
        """
        Delete a team

        Args:
            team_name (str): an object represetnation of the team

        Returns:
            Nothing
        """
        self.table.delete_item(TableName=self.table_name, Key={'name': team_name})

    def get(self, team_name: str) -> Union[Team, None]:
        """
        Get team information

        Args:
            team_name: the name of the team to get

        Returns:
            Team: A team object pulled from dynamodb
            None: No team was found
        """
        response = self.table.get_item(Key={'name': team_name})
        if 'Item' in response:
            return Team(**response['Item'])
        return None

    def get_all(self) -> List[Team]:
        """
        Get all the teams from the table

        Returns:
            List[Team]: A list of Team objects pulled from dynamodb
        """
        response = self.table.scan()
        return [Team(**team) for team in response['Items']]
