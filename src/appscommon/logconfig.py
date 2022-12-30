import logging
import sys
from uuid import uuid4

from flask import has_request_context, g, request


class RequestFormatter(logging.Formatter):
    def format(self, record):
        record.request_id = self.get_flask_request_id()

        return super().format(record)
    
    def get_flask_request_id(self):
        if not has_request_context():
            return ''

        request_id = g.get('request_id')
        if request_id:
            return request_id

        g.request_id = request.headers.get('x-request-id') or uuid4() 

        return g.get('request_id')


def init():
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(RequestFormatter(
        "%(asctime)s.%(msecs)03d %(levelname)s %(request_id)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s"
    ))
    logging.basicConfig(
        level=logging.DEBUG,
        datefmt="%d/%b/%Y %H:%M:%S",
        handlers=[handler]
    )
