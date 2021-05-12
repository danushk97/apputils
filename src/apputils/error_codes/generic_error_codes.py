"""
This module holds a class which defines generic error codes.
"""

from apputils.error_codes.error_codes import ErrorCodes


class GenericErrorCodes(ErrorCodes):
    """
    Holds the generic error codes.
    """
    INTERNAL_SERVER_ERROR = (5000, 'Internal server error')
    METHOD_NOT_ALLOWED = (5001, 'The mehtod is not allowed for this URL')
