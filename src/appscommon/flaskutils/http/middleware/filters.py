from functools import wraps
from logging import getLogger
from time import perf_counter
from typing import Callable

from appscommon.exception import AppException, InvalidParamsException
from flask import request
from pydantic import ValidationError


_logger = getLogger(__name__)


def error_filter(source: Callable) -> Callable:
    @wraps(source)  # Helps to retain the metadata of the actual source function.
    def wrapper(*args, **kwargs):
        tic = perf_counter()
        _logger.info(f'Starting to process {request.path}.')
        try:
            data = source(*args, **kwargs)
        except ValidationError as v_err:
            errors = [{'field': err.pop('loc'), **err} for err in v_err.errors()]
            exc = InvalidParamsException(invalid_params=errors)
            _logger.error(exc, exc_info=True)

            return exc.dict(), exc.status
        except Exception as err:
            if isinstance(err, AppException):
                exc = err
            else:
                exc = AppException(cause=err)

            _logger.error(exc, exc_info=True)

            return exc.dict(), exc.status
        finally:
            toc = perf_counter()
            _logger.info(f'Completed processing {request.path} in {toc - tic:.3f} seconds.')

        return data

    return wrapper
