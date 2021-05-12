from apputils.read_only import ReadOnly

class ErrorCodes(ReadOnly):
    @staticmethod
    def jsonify(error_code) -> dict:
        return {
            "error_code": error_code[0],
            "error_description": error_code[1]
        }
