class FakeValidationError(Exception):
    def __init__(self, errors) -> None:
        self.__errors = errors

    def errors(self):
        return self.__errors
