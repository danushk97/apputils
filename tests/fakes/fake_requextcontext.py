class FakeGlobal:
    def get(self, key):
        return getattr(self, key)


def fake_has_request_context():
    return True
