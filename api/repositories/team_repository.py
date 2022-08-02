from typing import List
import boto3, logging

from api.config import settings
from api.models.team import Team

class TeamRepository:
    def __init__(self, aws_resource=''):
        self.logger = logging.getLogger(settings.logger)
        if aws_resource == '':
            dynamodb = boto3.resource('dynamodb', endpoint_url=settings.dynamodb_url)
            self.table = dynamodb.Table(settings.dynamodb_table_name)
        else:
            self.table = aws_resource

    def put(self, resource: Team) -> bool:
        self.table.put_item(Item=resource.dict())

    def delete(self, table_name: str, resource: Team):
        self.table.delete_item(TableName=table_name, Key=resource.dict())

    def get(self, team_name: str) -> Team:
        response = self.table.get_item(Key={'name': team_name})
        if 'Item' in response:
            return Team(**response['Item'])
        return None

    def get_all(self) -> List[Team]:
        response = self.table.scan()
        return [Team(**team) for team in response['Items']]