class FakeSession:
    def __init__(self) -> None:
        self.calls = []

    def add(self, _):
        self.calls.append("add")

    def flush(self):
        self.calls.append("flush")

    def commit(self):
        self.calls.append("commit")

    def rollback(self):
        self.calls.append("rollback")

    def close(self):
        self.calls.append("close")
