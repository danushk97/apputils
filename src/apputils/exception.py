"""
This module holds the exception classes.
"""

from apputils.status_code import StatusCode
from apputils.error_codes.generic_error_codes import GenericErrorCodes


class AppException(Exception):
    """
    Base Exception class which should be inherited any other app exception
    classes.

    Attributes:
        error_codes (list): List of error_codes.
        status_code (int): Http status_code.
    """
    def __init__(self, error_codes:list=[],
                 status_code:int=StatusCode.INTERNAL_SERVER_ERROR) -> None:
        """
        Intansiates the class.
        """
        super().__init__(self)
        self.error_codes = [GenericErrorCodes.jsonify(error_code)
                            for error_code in error_codes] or \
                           [GenericErrorCodes.jsonify(
                               GenericErrorCodes.INTERNAL_SERVER_ERROR)]
        self.status_code = status_code
