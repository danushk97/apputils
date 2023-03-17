from http import HTTPStatus
from werkzeug.exceptions import HTTPException

from tests.fakes.fake_request import FakeRequest
from tests.fakes.fake_validationerror import FakeValidationError

from appscommon.flaskutils.http.middleware.filters import error_filter
from appscommon.exception import AppException


filters_module_path = 'appscommon.flaskutils.http.middleware.filters'


def test_error_filter_given_source_fn_raises_validation_error_then_raises_invalid_params_error(monkeypatch):
    monkeypatch.setattr(f'{filters_module_path}.request', FakeRequest)
    monkeypatch.setattr(f'{filters_module_path}.ValidationError', FakeValidationError)

    class FakeResponse:
        status_code = 422
        json = [{'loc': 'fake_field'}]

    def src_fun():
        http_ex = HTTPException(response=FakeResponse)
        raise http_ex

    exc_dict, status = error_filter(src_fun)()
    assert exc_dict == {
        'detail': 'Your request params did not validate',
        'invalid_params': [{'field': 'fake_field', 'msg': 'unknown error.'}],
        'status': 'failure',
        'title': 'Validation error',
        'type': 'about:blank',
    }
    assert status == HTTPStatus.BAD_REQUEST



def test_error_filter_given_source_fn_raises_any_error_then_raises_app_error(monkeypatch):
    monkeypatch.setattr(f'{filters_module_path}.request', FakeRequest)

    def src_fun(*args):
        raise Exception()

    exc_dict, status = error_filter(src_fun)()
    assert exc_dict == {
        'detail': 'Internal server error',
        'status': 'failure',
        'title': 'Internal server error',
        'type': 'about:blank'
    }
    assert status == HTTPStatus.INTERNAL_SERVER_ERROR


def test_error_filter_given_source_fn_raises_app_error_then_raises_app_error(monkeypatch):
    monkeypatch.setattr(f'{filters_module_path}.request', FakeRequest)

    def src_fun(*args):
        raise AppException(detail='fake error', status=HTTPStatus.BAD_REQUEST)

    exc_dict, status = error_filter(src_fun)()
    assert exc_dict == {
        'detail': 'fake error',
        'status': 'failure',
        'title': 'Internal server error',
        'type': 'about:blank'
    }
    assert status == HTTPStatus.BAD_REQUEST


def test_error_filter_given_source_fn_returns_value_then_returns(monkeypatch):
    monkeypatch.setattr(f'{filters_module_path}.request', FakeRequest)

    def src_fun():
        return {}

    data = error_filter(src_fun)()
    assert data == {}
