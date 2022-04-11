"""
This module holds the class which is responsible for handling errors
"""

import traceback
import logging
import sys
import functools

from marshmallow.exceptions import ValidationError
from apputils.status_code import StatusCode
from apputils.exception import AppException
from apputils.error_message import ErrorMessage


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
            response_dict (dict): {
                'error': {}
            }
            status_code (HttpStatusCode)
        """
        self.__log_error(f'[ERROR] {error.message}')
        response_dict = {
            'error': {
                'errors': error.errors,
                'code': error.status_code,
                'message': error.message
            }
        }
        return response_dict, error.status_code

    def generic_error_handler(self, error: Exception) -> tuple:
        """
        Handles the Exception.

        Args:
            error (Exception)

        Returns:
            response_dict (dict): {
                'errror_codes': []
            }
            status_code (HttpStatusCode)
        """
        self.__log_error(f'[ERROR] {error}')
        response_dict = {
            'error': {
                'code': 500,
                'message': ErrorMessage.INTERNAL_SERVER_ERROR
            }
        }

        return response_dict, StatusCode.INTERNAL_SERVER_ERROR

    def page_not_found_handler(self, error: Exception) -> tuple:
        """
        Handles the Page not found error.

        Args:
            error (Exception)

        Returns:
            response (Response)
        """
        return "404 page not found", StatusCode.PAGE_NOT_FOUND

    def method_not_allowed_handler(self, error: Exception) -> tuple:
        """
        Handles the Page not found error.

        Args:
            error (Exception)

        Returns:
            response_dict (dict): {
                'errror_codes': []
            }
            status_code (HttpStatusCode)
        """
        self.__log_error(f'[ERROR] {error}')
        response_dict = {
            'error': {
                'code': StatusCode.METHOD_NOT_ALLOWED,
                'message': ErrorMessage.METHOD_NOT_ALLOWED
            }
        }

        return response_dict, StatusCode.METHOD_NOT_ALLOWED

    def validation_error_handler(self, error: ValidationError):
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
        self.__log_error(f'[ERROR] {error.messages}')
        errors = []

        def extract_message(messages):
            for field, message in messages.items():
                if isinstance(message, list):
                    errors.extend(
                        [
                            {
                                'field': field,
                                'message': value
                            }
                            for value in message
                        ]
                    )

                if isinstance(message, dict):
                    extract_message(message)

        extract_message(error.messages)

        response_dict = {
            'error': {
                'errors': errors,
                'message': 'Payload contains missing or invalid data.',
                'code': 400
            }
        }

        return response_dict, StatusCode.BAD_REQUEST

    @staticmethod
    def __log_error(log_message: str='') -> None:
        """
        logs error message and stack trace.

        Args:
            error (Exception)
            stack_trace (str)
        """
        if log_message:
            logger.error(log_message, exc_info=True)


    @staticmethod
    def handle_exception(exception_to_handle: list, exception_to_raise: AppException):
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
                    ErrorHandler.__log_error(log_message)
                    error_message = ErrorMessage.INTERNAL_SERVER_ERROR
                    status_code = StatusCode.INTERNAL_SERVER_ERROR
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
