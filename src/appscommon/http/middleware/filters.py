from typing import Callable
from functools import wraps

from appscommon.exception import AppException, InvalidParamsException
from pydantic import ValidationError


def error_filter(source: Callable) -> Callable:
    @wraps(source)
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
