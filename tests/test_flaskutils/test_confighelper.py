import os
import sys

from tests.fakes.fake_flaskapp import FakeFlask

from appscommon.flaskutils import confighelper
from appscommon.exception.handler import ErrorHandler


def test_ensure_confgis_given_config_class_with_missing_config_then_aborts(monkeypatch, caplog):
    monkeypatch.setattr('appscommon.flaskutils.confighelper.abort', lambda: None)
    confighelper.ensure_configs({'DB_URL': ''})
    assert 'Aborting process due to missing configs: [\'DB_URL\']' in caplog.text


def test_ensure_confgis_given_config_class_with_valid_configs_then_returns_none():
    assert confighelper.ensure_configs({
        'DB_URL': 'postgres://localhost:5432@user:password/BNY'
    }) is None


def test_inject_dependencies_given_valid_input_then_returns_injected_dependents():
    dependents = {
        'service': lambda non_dependent_value, dependent_value: (non_dependent_value, dependent_value)
    }
    providers = {
        'dependent_value': 'injected_value'
    }
    injected_dependents = confighelper.inject_dependencies(dependents, providers)
    assert injected_dependents['service'](1) == (1, 'injected_value')


def test_register_blueprints_given_valid_input_then_registers_blueprints():
    fake_flask_app = FakeFlask()
    sys.path.append(os.path.dirname(os.path.dirname(__file__)))
    assert confighelper.register_blueprints(
        fake_flask_app,
        [('fakes.fake_blueprint', 'fake_blueprint')]
    ) is None
    assert 'fake' in fake_flask_app.blueprints


def test_register_error_handlers_given_valid_input_then_registers_error_handlers():
    fake_flask_app = FakeFlask()
    assert confighelper.register_http_error_handlers(fake_flask_app) is None
    assert fake_flask_app.error_handler[405] == ErrorHandler.method_not_allowed_handler
    assert fake_flask_app.error_handler[404] == ErrorHandler.page_not_found_handler
