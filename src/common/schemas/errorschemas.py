from typing import List, Optional

from pydantic import BaseModel


class InvalidParamsSchema(BaseModel):
    field: str
    reason: str


class ErrorResponseSchema(BaseModel):
    type: str
    title: str
    detail: str
    invalid_params: Optional[List[InvalidParamsSchema]]
    status: int
    