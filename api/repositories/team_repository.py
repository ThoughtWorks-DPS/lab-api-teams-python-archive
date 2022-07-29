import boto3

from api.config import settings
from api.models.team import Team

class TeamRepository:
    def __init__(self, aws_resource=''):
        if aws_resource == '':
            dynamodb = boto3.resource('dynamodb', endpoint_url=settings.dynamodb_url)
            self.table = dynamodb.Table(settings.dynamodb_table_name)
        else:
            self.table = aws_resource

    def put(self, resource: Team):
        self.table.put_item(Item=resource.dict())

    def delete(self, tableName, resource: Team):
        self.table.delete_item(TableName=tableName, Key=resource.dict())

    def get(self, resource_id: str) -> Team:
        response = self.table.get_item(Key={'id': resource_id})
        if 'Item' in response:
            return Team(**response['Item'])
        return None

    def get_all(self):
        response = self.table.scan()
        return [Team(**team) for team in response['Items']]