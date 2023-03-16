from  http import HTTPStatus

from appscommon.exception.handler import ErrorHandler


def test_page_not_found_handler():
    data = ErrorHandler.page_not_found_handler(Exception())
    assert data[0] == '404 page not found'
    assert data[1] == HTTPStatus.NOT_FOUND


def test_method_not_allowed_handler():
    data = ErrorHandler.method_not_allowed_handler(Exception())
    assert data[0] == {
        'type': 'about:blank',
        'title': 'Invalid HTTP method',
        'detail': 'The mehtod is not allowed for this URL',
        'status': 'failure'
    }
    assert data[1] == HTTPStatus.METHOD_NOT_ALLOWED
