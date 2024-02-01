"""
This module contains schemas.
"""

from typing import Any, List, Optional

from appscommon.enums import ResponseStatusEnum
from pydantic import BaseModel


class InvalidParamsSchema(BaseModel):
    field: str
    reason: str


class ErrorResponseSchema(BaseModel):
    type: str
    title: str
    detail: str
    invalid_params: Optional[List[InvalidParamsSchema]]
    status: ResponseStatusEnum = ResponseStatusEnum.FAILURE.value


class SuccessResponseSchema(BaseModel):
    data: Any
    status: ResponseStatusEnum = ResponseStatusEnum.SUCCESS.value
