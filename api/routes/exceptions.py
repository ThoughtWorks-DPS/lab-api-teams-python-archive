from typing import List, Optional


class InvalidParams:
    def __init__(self, field, code, message):
        self.field = field
        self.code = code
        self.message = message

class ApiException(Exception):
    def __init__(
            self,
            status_code,
            title,
            detail,
            invalid_params: Optional[List[InvalidParams]] = [InvalidParams(None, None, None)]
    ):
        self.status_code = status_code
        self.title = title
        self.detail = detail
        self.invalid_params = invalid_params