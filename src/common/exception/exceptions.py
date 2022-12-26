"""
This module holds the exception classes.
"""

from http import HTTPStatus

from common.exception.message import ErrorMessage


class AppException(Exception):
    """
    Base Exception class which should be inherited any other app exception
    classes.

    Attributes:
        type (str): A URI reference that identifies the problem type.When this member is not present, 
                    its value is assumed to be "about:blank".
        title (str): A short, human-readable summary of the problem type.
        detail (str): A human-readable explanation specific to this occurrence of the problem.
        status (int): The HTTP status code.
    """
    def __init__(self, 
        type: str = 'about:blank', 
        title: str = ErrorMessage.INTERNAL_SERVER_ERROR, 
        detail: str = ErrorMessage.INTERNAL_SERVER_ERROR, 
        status: int = HTTPStatus.INTERNAL_SERVER_ERROR,
        cause: Exception = None,
        log_message: str = None
    ) -> None:
        """
        Intansiates the class.
        """
        self.type = type
        self.title = title
        self.detail = detail
        self.status = status
        self.cause = cause
        self._log_message = log_message
    
    def dict(self) -> dict:
        return {
            'type': self.type,
            'title': self.title,
            'detail': self.detail,
            'status': self.status
        }
    
    def __repr__(self) -> str:
        message = self._log_message or self.detail
        if self.cause:
            message += f'[CAUSE]: {self.cause}'
        
        return message



class InvalidParams(AppException):
    """
    This class represents invalid params exception which should be raised whenever a request parameters did not 
    validate.

    Args:
        invalid_params (list): A list of dict containing invalid field/param name and a reason.
    """
    def __init__(self, 
        invalid_params: list, 
        type: str = 'about:blank', 
        title: str = ErrorMessage.VALIDATION_ERROR, 
        detail: str = ErrorMessage.REQUEST_PARAMS_DID_NOT_VALIDATE, 
        status: int = HTTPStatus.BAD_REQUEST,
        cause: Exception = None
    ) -> None:
        super().__init__(type, title, detail, status, cause, invalid_params)
        self.invalid_params = invalid_params

    def dict(self) -> dict:
        data = super().dict()
        data['invalid_params'] = self.invalid_params
    