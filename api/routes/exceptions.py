"""
Module for tracking exceptions
"""
from typing import List, Optional

from fastapi import HTTPException, status
from fastapi.exceptions import RequestValidationError
from starlette.requests import Request
from starlette.responses import JSONResponse

from api.shared import logger


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

def custom_validation_exception_handler(request: Request, exc: RequestValidationError):
    invalid_params_list = []
    for param in exc.errors():
        invalid_params_list.append({
            "field": ".".join(param['loc']),
            "message": param['msg'],
            "code": param['type']
        })
    print(exc.errors())
    logger.debug(invalid_params_list)

    return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, content={
        "title": "Invalid data provided",
        "detail": "Field is invalid and not accepted",
        "invalid_params": invalid_params_list
    })
