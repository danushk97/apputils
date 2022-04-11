from apputils.read_only import ReadOnly


class ErrorMessage(ReadOnly):
    INTERNAL_SERVER_ERROR = 'Internal server error'
    METHOD_NOT_ALLOWED = 'The mehtod is not allowed for this URL'
