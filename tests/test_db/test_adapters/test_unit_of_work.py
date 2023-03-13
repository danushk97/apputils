from appscommon.db.adapters.unit_of_work import UnitOfWork

from tests.fakes.fake_session import FakeSession


def test_unit_of_work_given_proper_input_then_rollbacks_and_closes_session_on_exit():
    uow = UnitOfWork(FakeSession)
    with uow as transaction:
        transaction.flush()
        transaction.commit()

    assert uow._session.calls == [
        "flush",
        "commit",
        "rollback",
        "close"
    ]
