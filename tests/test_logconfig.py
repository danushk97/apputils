import logging

from tests.fakes.fake_requextcontext import FakeGlobal


logger = logging.getLogger(__name__)


def test_logger_given_no_requst_contex_then_logs_without_request_id(caplog):
    logger.info('test')
    assert 'test' in caplog.text


def test_logger_given_requst_contex_then_logs_with_request_id(caplog, monkeypatch):
    monkeypatch.setattr('appscommon.logconfig.g', FakeGlobal())
    logger.info('test')
    assert 'test' in caplog.text
