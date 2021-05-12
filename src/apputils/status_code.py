"""
This module holds the enum class for status code.
"""

from apputils.read_only import ReadOnly

class StatusCode(ReadOnly):
    """
    Holds the status code info.
    """
    OK = 200
    BAD_REQUEST = 400
    PAGE_NOT_FOUND = 404
    INTERNAL_SERVER_ERROR = 500
    METHOD_NOT_ALLOWED = 405
    UNAUTHORIZED = 401
    RESOURCE_NOT_FOUND = 204
