"""
Module for tracking exceptions
"""
from typing import List, Optional

from fastapi import HTTPException


# pylint: disable=too-few-public-methods
class InvalidParams:
    """Object for managing incorrect parameters"""
    def __init__(self, field, code, message):
        self.field = field
        self.code = code
        self.message = message

# pylint: disable=too-few-public-methods
class ApiException(HTTPException):
    """Exception for an error that will be returned by the API"""
    def __init__(
            self,
            status_code,
            title,
            detail,
            invalid_params: Optional[List[InvalidParams]] = None
    ):
        self.title = title
        self.invalid_params = invalid_params
        super().__init__(status_code=status_code, detail=detail)
