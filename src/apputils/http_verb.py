"""
This module holds the enum class for which is used to define HTTP verbs.
"""

from apputils.read_only import ReadOnly


class HttpVerb(ReadOnly):
    GET = 'GET'
    POST = 'POST'
    PUT = 'PUT'
    DELETE = 'DELETE'
