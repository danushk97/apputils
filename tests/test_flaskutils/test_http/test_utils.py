from appscommon.flaskutils.http.utils import send_success_response


def test_send_success_response_given_any_input_returns_wrapped_dict():
    assert send_success_response('value') == {
        'data': 'value',
        'status': 'success'
    }
