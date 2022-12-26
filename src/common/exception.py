"""
This module holds the exception classes.
"""

from apputils.status_code import StatusCode
from apputils.error_message import ErrorMessage


class AppException(Exception):
    """
    Base Exception class which should be inherited any other app exception
    classes.

    Attributes:
        error_codes (list): List of error_codes.
        status_code (int): Http status_code.
    """
    def __init__(self, message:str='', errors=None, status_code:int=StatusCode.INTERNAL_SERVER_ERROR) -> None:
        """
        Intansiates the class.
        """
        super().__init__(self)
        self.message = message or ErrorMessage.INTERNAL_SERVER_ERROR
        self.errors = errors or []
        self.status_code = status_code
