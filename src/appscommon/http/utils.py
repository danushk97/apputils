from typing import Any

from appscommon.http.schemas import SuccessResponseSchema


def send_success_response(data: Any) -> dict:
    return SuccessResponseSchema(
        data=data
    ).dict()
