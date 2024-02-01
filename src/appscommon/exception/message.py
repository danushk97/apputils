from appscommon.readonly import ReadOnly


class ErrorMessage(ReadOnly):
    INTERNAL_SERVER_ERROR = 'Internal server error'
    INVALID_HTTP_METHOD = 'Invalid HTTP method'

    METHOD_NOT_ALLOWED = 'The mehtod is not allowed for this URL'

    REQUEST_PARAMS_DID_NOT_VALIDATE = 'Your request params did not validate'

    VALIDATION_ERROR = 'Validation error'
