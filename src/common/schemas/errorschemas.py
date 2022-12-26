from typing import List, Optional

from pydantic import BaseModel


class InvalidParams(BaseModel):
    field: str
    reason: str


class ErrorResponseSchema(BaseModel):
    type: str
    title: str
    detail: str
    invalid_params: Optional[List[InvalidParams]]
    status: int
    