import pytest

from apputils.error_handler import ErrorHandler
from apputils.exception import AppException
from apputils.status_code import StatusCode


error_handler_module_path = 'user_accounts.common.error_handler'
error_handler = ErrorHandler()


def test_app_error_handler():
    error_codes = [(1, 'error')]
    exception = AppException(error_codes=error_codes,
                             status_code=StatusCode.BAD_REQUEST)
    data = error_handler.app_error_handler(exception)
    assert data[0] == {'error_codes': [{'error_code': 1, 'error_description': 'error'}]}
    assert data[1] == 400


def test_generic_error_handler():
    data = error_handler.generic_error_handler(Exception)
    assert data[0] == {'error_codes': [{'error_code': 5000, 'error_description': 'Internal server error'}]}
    assert data[1] == 500


def test_page_not_found_handler():
    data = error_handler.page_not_found_handler(Exception)
    assert data[0] == '404 page not found'
    assert data[1] == 404


def test_method_not_allowed_handler():
    data = error_handler.method_not_allowed_handler(Exception)
    assert data[0] == {'error_codes': [{'error_code': 5001,
                                        'error_description': 'The mehtod is not allowed for this URL'}]}
    assert data[1] == 405


def test_handle_exception():
    @ErrorHandler.handle_exception([Exception], AppException)
    def mock_function(self):
        raise Exception

    with pytest.raises(AppException) as exc_info:
        mock_function("value")

    assert exc_info.value.error_codes == [{'error_code': 5000, 'error_description': 'Internal server error'}]
    assert exc_info.value.status_code == 500
