"""
This module holds the class which is responsible for handling errors.
"""

from logging import getLogger
from http import HTTPStatus

from appscommon.exception import AppException
from appscommon.exception.message import ErrorMessage


_logger = getLogger(__name__)


class ErrorHandler:
    """
    Holds the HTTP error handler functions.
    """
    @staticmethod
    def page_not_found_handler(error: Exception) -> tuple:
        """
        Handles the Page not found error.

        Args:
            error (Exception):

        Returns:
            response_content (str), status (HttpStatus):
        """
        _logger.error(error)
        return '404 page not found', HTTPStatus.NOT_FOUND

    @staticmethod
    def method_not_allowed_handler(error: Exception) -> tuple:
        """
        Handles the Page not found error.

        Args:
            error (Exception):

        Returns:
            response_dict (common.schemas.ErrorResponseSchema), status (HttpStatus):
        """
        exc = AppException(
            title=ErrorMessage.INVALID_HTTP_METHOD,
            detail=ErrorMessage.METHOD_NOT_ALLOWED,
            status=HTTPStatus.METHOD_NOT_ALLOWED,
            cause=error
        )
        _logger.error(exc)
        return exc.dict(), HTTPStatus.METHOD_NOT_ALLOWED
