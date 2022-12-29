import importlib
import inspect
from logging import getLogger
from os import abort
from typing import Callable, Dict

from appscommon.exception import AppException
from appscommon.exception.handler import ErrorHandler
from flask import Flask


logger = getLogger(__name__)


def ensure_configs(config):
    """
    Aborts application start up if there is any missing configuration.
    """
    logger.info('Valdating configs...')
    missing_configs = []
    for key, value in inspect.getmembers(config):
        if not key.startswith('_') and (value is None or str(value).strip() == ''):
            missing_configs.append(key)

    if missing_configs:
        logger.critical(f'Aborting process due to missing configs: {missing_configs}')
        abort(1)

    logger.info('Config validation was successful.')


def inject_dependencies(definitions: Dict[str, Callable], dependencies: dict):
    injected_definitions = {}

    for key, value in definitions.items():
        injections = {}
        for param in inspect.signature(value).parameters:
            if param in dependencies:
                injections[param] = dependencies[param]

        injected_definitions[key] = lambda *args, injections=injections: value(*args, **injections)
    
    return injected_definitions


def register_blueprints(app: Flask, blueprints: list):
    for module, blueprint_attr in blueprints:
        module = importlib.import_module(module)
        blueprint = getattr(module, blueprint_attr)
        app.register_blueprint(blueprint)


def register_error_handlers(app: Flask) -> None:
    """
    Registers routes with the app instance.

    Args:
        app (Flask): Instance of app.
    """
    app.register_error_handler(404, ErrorHandler.page_not_found_handler)
    app.register_error_handler(405, ErrorHandler.method_not_allowed_handler)
    app.register_error_handler(AppException, ErrorHandler.app_error_handler)
    app.register_error_handler(Exception, ErrorHandler.generic_error_handler)
