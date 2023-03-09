from appscommon.exception import AppException, InvalidParamsException


def test_app_exception_dict_returns_valid_dict():
    value = AppException().dict()
    assert value == {
        'detail': 'Internal server error',
        'status': 'failure',
        'title': 'Internal server error',
        'type': 'about:blank'
    }


def test_app_exception_str_returns_valid_str():
    value = AppException()
    assert str(value) == '<AppException> Internal server error'


def test_invalidparam_exception_dict_returns_valid_dict():
    value = InvalidParamsException(invalid_params=['invalid_param_1']).dict()
    assert value == {
        'detail': 'Your request params did not validate',
        'invalid_params': ['invalid_param_1'],
        'status': 'failure',
        'title': 'Validation error',
        'type': 'about:blank'
    }
