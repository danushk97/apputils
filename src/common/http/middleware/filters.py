from logging import getLogger
from typing import Callable

from common.exception import AppException, InvalidParamsException
from pydantic import ValidationError


logger = getLogger(__name__)


def error_filter(source: Callable) -> Callable:
    def wrapper(*args, **kwargs):
        try:
            return source(*args, **kwargs)
        except ValidationError as v_err:
            errors = [{"field": err.pop("loc"), **err} for err in v_err.errors()]
            raise InvalidParamsException(invalid_params=errors)
        except Exception as e:
            if isinstance(e, AppException):
                raise e
            raise AppException(cause=e)

    return wrapper
