import importlib
import inspect
from logging import getLogger
from os import abort
from typing import Callable, Dict

from appscommon.exception.handler import ErrorHandler
from flask import Flask


_logger = getLogger(__name__)


def ensure_configs(config):
    """
    Aborts application start up if there is any missing configuration.
    """
    _logger.info('Valdating configs...')
    missing_configs = []
    for key, value in inspect.getmembers(config):
        if not key.startswith('_') and (value is None or str(value).strip() == ''):
            missing_configs.append(key)

    if missing_configs:
        _logger.critical(f'Aborting process due to missing configs: {missing_configs}')
        abort(1)

    _logger.info('Config validation was successful.')


def inject_dependencies(definitions: Dict[str, Callable], dependencies: dict):
    _logger.info('Injecting dependencies....')
    injected_definitions = {}

    for key, value in definitions.items():
        injections = {}
        for param in inspect.signature(value).parameters:
            if param in dependencies:
                injections[param] = dependencies[param]

        injected_definitions[key] = lambda *args, injections=injections: value(*args, **injections)
    
    return injected_definitions


def register_blueprints(flask_app: Flask, route_modules: list):
    _logger.info('Registering routes/blueprints....')
    for module, blueprint_attr in route_modules:
        module = importlib.import_module(module)
        blueprint = getattr(module, blueprint_attr)
        flask_app.register_blueprint(blueprint)  # registering routes.


def register_http_error_handlers(flask_app: Flask) -> None:
    """
    Registers routes with the app instance.

    Args:
        flask_app (Flask): Instance of flask_app.
    """
    _logger.info('Registering http error handlers for flask app...')
    flask_app.register_error_handler(404, ErrorHandler.page_not_found_handler)
    flask_app.register_error_handler(405, ErrorHandler.method_not_allowed_handler)
