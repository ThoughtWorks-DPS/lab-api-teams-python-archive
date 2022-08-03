"""
Team Repository

Abstracts dynamodb interactions so that other areas of the API
don't need to be aware of the implementation
"""

from typing import List
import logging
import boto3

from api.config import settings
from api.models.team import Team

class TeamRepository:
    """
    Abstraction over DynamoDB for interacting with Team information
    Can take an aws resource for test mocking
    """
    def __init__(self, aws_resource=''):

        self.logger = logging.getLogger(settings.logger)
        if aws_resource == '':
            dynamodb = boto3.resource('dynamodb', endpoint_url=settings.dynamodb_url)
            self.table = dynamodb.Table(settings.dynamodb_table_name)
        else:
            self.table = aws_resource

    def put(self, team: Team):
        """
        Create or update a team

        Args:
            team: an object represetnation of the team

        Returns:
            Nothing
        """
        self.table.put_item(Item=team.dict())

    def delete(self, table_name: str, resource: Team):
        """
        Delete a team

        Args:
            table_name: the name of the table to operate on, always 'team'
            team: an object represetnation of the team

        Returns:
            Nothing
        """
        self.table.delete_item(TableName=table_name, Key=resource.dict())

    def get(self, team_name: str) -> Team:
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
