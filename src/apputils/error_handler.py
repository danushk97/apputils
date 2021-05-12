"""
This module holds the class which is responsible for handling errors
"""

import traceback
import logging
import sys
import functools

from apputils.status_code import StatusCode
from apputils.exception import AppException
from apputils.error_codes.generic_error_codes import GenericErrorCodes


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
                'errror_codes': []
            }
            status_code (HttpStatusCode)
        """
        self.__log_error(f'[ERROR] {error.error_codes}')
        response_dict = {
            'error_codes': error.error_codes
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
        self.__log_error(f'[ERROR] {error}', stack_trace=traceback.format_exc())
        response_dict = {
            'error_codes': [GenericErrorCodes.jsonify(
                GenericErrorCodes.INTERNAL_SERVER_ERROR
            )]
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
        self.__log_error(f'[ERROR] {error}', stack_trace=traceback.format_exc())
        response_dict = {
            'error_codes': [GenericErrorCodes.jsonify(
                GenericErrorCodes.METHOD_NOT_ALLOWED
            )]
        }

        return response_dict, StatusCode.METHOD_NOT_ALLOWED

    @staticmethod
    def __log_error(log_message: str='', stack_trace: str='') -> None:
        """
        logs error message and stack trace.

        Args:
            error (Exception)
            stack_trace (str)
        """
        if log_message:
            logger.error(log_message)

        if stack_trace:
            logger.error(f'[STACK_TRACE] {stack_trace}')

    @staticmethod
    def handle_exception(exception_to_handle: list,
                         exception_to_raise: AppException):
        def actual_decorator(function):
            @functools.wraps(function)
            def wrapper(self, *args, **kwargs):
                try:
                    return function(self, *args, **kwargs)
                except tuple(exception_to_handle):
                    e_type, _, tb = sys.exc_info()
                    log_message = (
                        f'[ERROR] Caught an exception, [error]: {e_type} '
                        f'[line number]: {tb.tb_lineno} '
                        f'[function_name]: {function.__name__}'
                        f'[module_name]: {function.__module__}')
                    stack_trace = str(traceback.format_exc())
                    ErrorHandler.__log_error(log_message, stack_trace)
                    raise exception_to_raise()

            return wrapper

        return actual_decorator
