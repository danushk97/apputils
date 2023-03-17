from functools import wraps
from logging import getLogger
from time import perf_counter
from flask import request
from typing import Callable
from http import HTTPStatus
from werkzeug.exceptions import HTTPException

from appscommon.exception import AppException, InvalidParamsException
from pydantic import ValidationError


_logger = getLogger(__name__)


def error_filter(source: Callable) -> Callable:
    @wraps(source)  # Helps to retain the metadata of the actual source function.
    def wrapper(*args, **kwargs):
        tic = perf_counter()
        _logger.info(f'Starting to process {request.path}.')
        try:
            data = source(*args, **kwargs)
        except Exception as err:
            if isinstance(err, AppException):
                exc = err
            elif isinstance(err, HTTPException) and hasattr(err, 'response') and \
                    err.response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY:
                errors = [
                    {'field': err.pop('loc'), 'msg': err.pop('msg', 'unknown error.')}
                    for err in err.response.json
                ]
                exc = InvalidParamsException(invalid_params=errors)
                _logger.error(exc, exc_info=True)

                return exc.dict(), exc.status
            else:
                exc = AppException()
                exc.__cause__ = err

            _logger.error(exc, exc_info=True)

            return exc.dict(), exc.status
        finally:
            toc = perf_counter()
            _logger.info(f'Completed processing {request.path} in {toc - tic:.3f} seconds.')

        return data

    return wrapper
