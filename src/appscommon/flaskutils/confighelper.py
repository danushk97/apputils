import importlib
import inspect
from logging import getLogger
from os import abort
from typing import Callable, Dict, Type

from appscommon.exception.handler import ErrorHandler
from flask import Flask


_logger = getLogger(__name__)


def ensure_configs(config: Type) -> None:
    """
    Aborts application start up if there is any empty config values. It should be called at the application startup.

    Args:
        config (Type): A class with attributes which represents the app config.
    """
    _logger.info('Valdating configs...')
    missing_configs = []
    for key, value in inspect.getmembers(config):
        if not key.startswith('_') and (value is None or str(value).strip() == ''):
            missing_configs.append(key)

    if missing_configs:
        _logger.critical(f'Aborting process due to missing configs: {missing_configs}')
        abort()

    _logger.info('Config validation was successful.')


def inject_dependencies(dependents: Dict[str, Callable], providers: dict) -> dict:
    """
    Injects dependencies.

    Args:
        dependents (dict): Key can be any string which uniquely identifies the dependant and the value must be
                           any callable.
        providers (dict): Key should be name of the dependency and value should be the actual value which `dependents`
                          depend upon.

    Returns:
        (dict): injected dependents.
    """
    _logger.info('Injecting dependencies....')
    rescued_dependents = {}

    for key, dependent in dependents.items():
        injections = {}
        for param in inspect.signature(dependent).parameters:
            if param in providers:
                injections[param] = providers[param]

        rescued_dependents[key] = lambda *args, injections=injections, value=dependent: value(*args, **injections)

    return rescued_dependents


def register_blueprints(flask_app: Flask, module_paths: list) -> None:
    """
    Registers blueprints with the app instance.

    Args:
        flask_app (Flask): Instance of wsgi app.
        route_modules (list): List of tuples/lists containing module path and name of blueprint attribute.
    """
    _logger.info('Registering routes/blueprints....')
    for module, blueprint_attr in module_paths:
        module = importlib.import_module(module)
        blueprint = getattr(module, blueprint_attr)
        flask_app.register_blueprint(blueprint)  # registering routes.


def register_http_error_handlers(flask_app: Flask) -> None:
    """
    Registers error handlers.

    Args:
        flask_app (Flask): Instance of flask_app.
    """
    _logger.info('Registering http error handlers for flask app...')
    flask_app.register_error_handler(404, ErrorHandler.page_not_found_handler)
    flask_app.register_error_handler(405, ErrorHandler.method_not_allowed_handler)
