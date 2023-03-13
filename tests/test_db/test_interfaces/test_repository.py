import pytest

from appscommon.db.interfaces.repository import AbstractRepository

from tests.fakes.fake_session import FakeSession


class Repository(AbstractRepository):
    def __init__(self) -> None:
        self._session = FakeSession()

    def add(self, entity):
        return super().add(entity)

    def get(self, id):
        return super().get(id)

    def list(self):
        return super().list()


def test_abstract_repository():
    repo = Repository()
    assert repo.add('fake_entity') is None

    with pytest.raises(NotImplementedError):
        repo.get('fake_id')

    with pytest.raises(NotImplementedError):
        repo.list()
