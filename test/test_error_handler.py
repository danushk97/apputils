import pytest

from marshmallow import ValidationError
from apputils.error_handler import ErrorHandler
from apputils.exception import AppException
from apputils.status_code import StatusCode


error_handler_module_path = 'user_accounts.common.error_handler'
error_handler = ErrorHandler()


def test_app_error_handler():
    exception = AppException(message='error', status_code=StatusCode.BAD_REQUEST)
    data = error_handler.app_error_handler(exception)
    assert data[0] == {'error': {'message': 'error', 'errors': [], 'code': 400}}
    assert data[1] == 400


def test_generic_error_handler():
    data = error_handler.generic_error_handler(Exception)
    assert data[0] == {'error': {'message': 'Internal server error', 'code': 500}}
    assert data[1] == 500


def test_page_not_found_handler():
    data = error_handler.page_not_found_handler(Exception)
    assert data[0] == '404 page not found'
    assert data[1] == 404


def test_method_not_allowed_handler():
    data = error_handler.method_not_allowed_handler(Exception)
    assert data[0] == {'error': {'message': 'The mehtod is not allowed for this URL', 'code': 405}}
    assert data[1] == 405


def test_validation_error_handler():
    data = error_handler.validation_error_handler(
        ValidationError({'attr': ['attr is required'], 'address': {'value': ['value is required']}})
    )
    assert data[0] == {
        'error': {
            'code': 400,
            'errors': [
                {
                    'field': 'attr',
                    'message': 'attr is required'
                },
                {
                    'field': 'value',
                    'message': 'value is required'
                }
            ],
            'message': 'Payload contains missing or invalid data.'
        }
    }
    assert data[1] == 400


def test_handle_exception():
    @ErrorHandler.handle_exception([Exception], AppException)
    def mock_function(self):
        raise Exception

    with pytest.raises(AppException) as exc_info:
        mock_function("value")

    assert exc_info.value.message == 'Internal server error'
    assert exc_info.value.status_code == 500


def test_handle_app_exception():
    @ErrorHandler.handle_exception([ValidationError], AppException)
    def mock_function(self):
        raise AppException(message='custom error_message', status_code=400)

    with pytest.raises(AppException) as exc_info:
        mock_function("value")

    assert exc_info.value.message == 'custom error_message'
    assert exc_info.value.status_code == 400


def test_handle_validation_exception():
    @ErrorHandler.handle_exception([AppException], AppException)
    def mock_function(self):
        raise AppException(message='custom error_message', status_code=400)

    with pytest.raises(AppException) as exc_info:
        mock_function("value")

    assert exc_info.value.message == 'custom error_message'
    assert exc_info.value.status_code == 400
