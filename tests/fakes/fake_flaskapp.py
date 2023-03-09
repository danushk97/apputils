class FakeFlask:
    def __init__(self) -> None:
        self.blueprints = []
        self.error_handler = {}

    def register_blueprint(self, *args):
        self.blueprints.append(args[0].name)

    def register_error_handler(self, key, value):
        self.error_handler[key] = value
