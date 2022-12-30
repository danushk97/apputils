import logging
import sys

from appscommon.http.utils import get_flask_request_id
from flask import has_request_context, g


class CustomAdapter(logging.LoggerAdapter):
    """
    This example adapter expects the passed in dict-like object to have a
    'connid' key, whose value in brackets is prepended to the log message.
    """
    def process(self, msg, kwargs):
        return '[%s] %s' % (self.extra['request_id'], msg), kwargs
         

def init():
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s.%(msecs)03d %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s",
        datefmt="%d/%b/%Y %H:%M:%S",
        stream=sys.stdout
    )


class Logging:
    def __init__(self, name: str) -> None:
        self.name = name
        self._logger = CustomAdapter(logging.getLogger(self.name), {'request_id': get_flask_request_id()})

    @property
    def logger(self):
        if not has_request_context():
            return self._logger
        
        g_logger = g.get('logger')
        if g_logger:
            return g_logger

        g.logger = CustomAdapter(logging.getLogger(self.name), {'request_id': get_flask_request_id()})

        return g.get("logger")
