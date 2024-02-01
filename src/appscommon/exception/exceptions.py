"""
This module holds the exception classes.
"""

from http import HTTPStatus

from appscommon.exception.message import ErrorMessage
from appscommon.enums import ResponseStatusEnum


class AppException(Exception):
    """
    Base Exception class which should be inherited any other app exception
    classes.

    Attributes:
        type (str): A URI reference that identifies the problem type.When this
                    member is not present, its value is assumed to be
                    "about:blank".
        title (str): A short, human-readable summary of the problem type.
        detail (str): A human-readable explanation specific to this occurrence
                      of the problem.
        status (int): The HTTP status code.
    """
    def __init__(
        self,
        type: str = 'about:blank',
        title: str = ErrorMessage.INTERNAL_SERVER_ERROR,
        detail: str = ErrorMessage.INTERNAL_SERVER_ERROR,
        status: int = HTTPStatus.INTERNAL_SERVER_ERROR,
        log_message: str = None
    ) -> None:
        """
        Intansiates the class.
        """
        self.type = type
        self.title = title
        self.detail = detail
        self.status = status
        self._log_message = log_message

    def dict(self) -> dict:
        return {
            'type': self.type,
            'title': self.title,
            'detail': self.detail,
            'status': ResponseStatusEnum.FAILURE.value
        }

    def __str__(self) -> str:
        message = f'<{type(self).__name__}> {self._log_message or self.detail}'
        if self.__cause__:
            message += f' [CAUSE]: {self.__cause__}'

        return message


class InvalidParamsException(AppException):
    """
    This class represents invalid params exception which should be raised
    whenever a request parameters did not validate.

    Args:
        invalid_params (list): A list of dict containing invalid field/param
        name and a reason.
    """
    def __init__(
        self,
        invalid_params: list,
        type: str = 'about:blank',
        title: str = ErrorMessage.VALIDATION_ERROR,
        detail: str = ErrorMessage.REQUEST_PARAMS_DID_NOT_VALIDATE,
        status: int = HTTPStatus.BAD_REQUEST
    ) -> None:
        super().__init__(type, title, detail, status, invalid_params)
        self.invalid_params = invalid_params

    def dict(self) -> dict:
        return {
            **super().dict(),
            'invalid_params': self.invalid_params
        }
