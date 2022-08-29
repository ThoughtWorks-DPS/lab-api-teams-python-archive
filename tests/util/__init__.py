"""
Utility functions for making testing easier
"""
from unittest.mock import MagicMock


def mock_return_team_service(**kwargs):
    """
    Mock the team service and respond with whatever input for the given keyword function name
    """
    def return_stubbed_team_service():
        mock_team_service = MagicMock()
        mock_team_service.create_team.return_value = kwargs.get("create_team")
        mock_team_service.delete_team.return_value = kwargs.get("delete_team")
        mock_team_service.get_all.return_value = kwargs.get("get_all")
        mock_team_service.get.return_value = kwargs.get("get")
        return mock_team_service

    return return_stubbed_team_service

def mock_return_notification_service(**kwargs):
    """
    Mock the notification service to handle messages easier in tests
    """
    def return_stubbed_notification_service():
        mock_notification_service = MagicMock()
        mock_notification_service.handle.return_value = kwargs.get("handle")
        return mock_notification_service

    return return_stubbed_notification_service
