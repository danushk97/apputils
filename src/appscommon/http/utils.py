from flask import has_request_context, request, g
from typing import Any
from uuid import uuid4

from appscommon.http.schemas import SuccessResponseSchema


def get_flask_request_id():
    if not has_request_context():
        return ''
    
    request_id = g.get('request_id')
    if request_id:
        return request_id
        
    g.request_id = request.headers.get('x-request-id') or uuid4() 
    
    return g.get('request_id')


def send_success_response(data: Any) -> dict:
    return SuccessResponseSchema(
        data=data
    ).dict()
