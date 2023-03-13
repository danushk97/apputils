import pytest

from appscommon.db.interfaces.unit_of_work import AbstractUnitOfWork


class UnitOfWork(AbstractUnitOfWork):
    def commit(self):
        return super().commit()

    def flush(self):
        return super().flush()

    def rollback(self):
        return super().rollback()

    def end_session(self):
        return super().end_session()


uow = UnitOfWork()


def test_abstract_unit_of_work_methods():
    for fn_name in ['flush', 'commit', 'rollback', 'end_session']:
        with pytest.raises(NotImplementedError):
            getattr(uow, fn_name)()


def test_abstract_unit_of_work_enter_returns_self():
    assert uow.__enter__() is uow


def test_abstract_unit_of_work_exit_raise_not_implemented_error():
    with pytest.raises(NotImplementedError):
        uow.__exit__()
