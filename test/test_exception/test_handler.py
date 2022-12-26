from  http import HTTPStatus

from common.exception.handler import ErrorHandler
from common.exception import AppException


error_handler_module_path = 'user_accounts.common.error_handler'
error_handler = ErrorHandler()


def test_app_error_handler():
    exception = AppException(
        title='error', 
        detail='error', 
        status=HTTPStatus.BAD_REQUEST
    )
    data = error_handler.app_error_handler(exception)
    assert data[0] == exception.dict()
    assert data[1] == 400


def test_generic_error_handler():
    data = error_handler.generic_error_handler(Exception)
    exc = AppException(cause=Exception)
    assert data[0] == exc.dict()
    assert data[1] == 500


def test_page_not_found_handler():
    data = error_handler.page_not_found_handler(Exception)
    assert data[0] == '404 page not found'
    assert data[1] == 404


def test_method_not_allowed_handler():
    data = error_handler.method_not_allowed_handler(Exception)
    assert data[0] == {
        'type': 'about:blank', 
        'title': 'Invalid HTTP method', 
        'detail': 'The mehtod is not allowed for this URL', 
        'status': 405
    }
    assert data[1] == 405
