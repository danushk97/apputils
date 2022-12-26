"""
This module holds the class which is responsible for handling errors
"""

import traceback
from http import HTTPStatus
import logging
import sys
import functools

from pydantic.errors import PydanticValueError


from common.exception import AppException
from common.exception.message import ErrorMessage


logger = logging.getLogger(__name__)


class ErrorHandler:
    """
    Responsible to handle errors.
    """
    def app_error_handler(self, error: AppException) -> tuple:
        """
        Handles the AppException and also Exceptions which are derived from
        AppException.

        Args:
            error (AppException)

        Returns:
            response_dict (common.schemas.ErrorResponseSchema), status (HttpStatus):
        """
        logger.error(error, exc_info=True)
        return error.dict(), error.status

    def generic_error_handler(self, error: Exception) -> tuple:
        """
        Handles the Exception.

        Args:
            error (Exception)

        Returns:
            response_dict (common.schemas.ErrorResponseSchema), status (HttpStatus):
        """
        logger.error(error, exc_info=True)
        exc = AppException(cause=error)  
        return exc.dict(), exc.status

    def page_not_found_handler(self, error: Exception) -> tuple:
        """
        Handles the Page not found error.

        Args:
            error (Exception)

        Returns:
            response_content (str), status (HttpStatus):
        """
        logger.error(error, exc_info=True)
        return "404 page not found", HTTPStatus.NOT_FOUND

    def method_not_allowed_handler(self, error: Exception) -> tuple:
        """
        Handles the Page not found error.

        Args:
            error (Exception)

        Returns:
            response_dict (common.schemas.ErrorResponseSchema), status (HttpStatus):
        """
        exc = AppException(
            title=ErrorMessage.INVALID_HTTP_METHOD,
            detail=ErrorMessage.METHOD_NOT_ALLOWED,
            status=HTTPStatus.METHOD_NOT_ALLOWED,
            cause=error
        )
        logger.error(exc, exc_info=True)
        return exc.dict(), HTTPStatus.METHOD_NOT_ALLOWED

    def validation_error_handler(self, error: PydanticValueError):
        """
        Handles marshmallow validation error.

        Args:
            error (ValidationError)

        Returns:
            response_dict (dict): {
                'errror_codes': []
            }
            status_code (HttpStatusCode)
        """
        # TODO: needs update.
        raise error

    @staticmethod
    def handle_exception(exception_to_handle: list, exception_to_raise: AppException):
        # TODO: needs update.
        def actual_decorator(function):
            @functools.wraps(function)
            def wrapper(self, *args, **kwargs):
                try:
                    return function(self, *args, **kwargs)
                except tuple(exception_to_handle) as error:
                    e_type, _, tb = sys.exc_info()
                    log_message = (
                        f'[ERROR] Caught an exception, [error]: {e_type} '
                        f'[line number]: {tb.tb_lineno} '
                        f'[function_name]: {function.__name__}'
                        f'[module_name]: {function.__module__}')
                    logger.error(log_message, exc_info=True)
                    error_message = ErrorMessage.INTERNAL_SERVER_ERROR
                    status_code = HTTPStatus.INTERNAL_SERVER_ERROR
                    errors = []

                    if isinstance(error, AppException):
                        error_message = error.message
                        status_code = error.status_code
                        errors=[]

                    if exception_to_raise:
                        raise exception_to_raise(
                            message=error_message,
                            errors=errors,
                            status_code=status_code
                        )

            return wrapper

        return actual_decorator
