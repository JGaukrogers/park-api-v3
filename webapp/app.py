"""
Copyright 2023 binary butterfly GmbH
Use of this source code is governed by an MIT-style license that can be found in the LICENSE.txt.
"""

import os

from flask import request
from flask_sqlalchemy.track_modifications import models_committed

from webapp.admin_rest_api import AdminRestApi
from webapp.cli import register_cli_to_app
from webapp.common.config import BaseConfig, ConfigLoader
from webapp.common.error_handling import ErrorDispatcher
from webapp.common.flask_app import App
from webapp.common.rest import RestApiErrorHandler
from webapp.dependencies import dependencies
from webapp.event_receiver import event_receivers
from webapp.extensions import celery, db, migrate, openapi
from webapp.public_rest_api import PublicRestApi

__all__ = ['launch']


def launch(testing: bool = False) -> App:
    app = App(
        BaseConfig.PROJECT_NAME,
        instance_path=BaseConfig.INSTANCE_FOLDER_PATH,
        instance_relative_config=True,
        template_folder=os.path.join(BaseConfig.PROJECT_ROOT, 'templates'),
    )
    configure_app(app, testing=testing)
    configure_blueprints(app)
    configure_extensions(app)
    configure_logging(app)
    configure_error_handlers(app)
    configure_events(app)

    return app


def configure_app(app: App, testing: bool = False) -> None:
    # Load config from YAML file
    config_loader = ConfigLoader()
    config_loader.configure_app(app, testing)


def configure_extensions(app: App) -> None:
    db.init_app(app)
    migrate.init_app(app, db)
    celery.init_app(app)
    openapi.init_app(app)
    dependencies.get_config_helper().init_app(app)


def configure_blueprints(app: App) -> None:
    app.register_blueprint(AdminRestApi())
    app.register_blueprint(PublicRestApi())

    register_cli_to_app(app)


def configure_events(app: App):
    # connect any model change to event update service
    models_committed.connect(
        receiver=lambda sender, changes: dependencies.get_sqlalchemy_service().handle_model_changes(changes),
        sender=app,
        weak=False,
    )

    dependencies.get_event_helper().register_receivers(event_receivers)

    # trigger publishing recorded events
    @app.teardown_appcontext
    def teardown_appcontext(exception: BaseException | None):
        dependencies.get_event_helper().publish_events()


def configure_logging(app: App) -> None:
    if not os.path.exists(app.config['LOG_DIR']):
        os.makedirs(app.config['LOG_DIR'])


def configure_error_handlers(app: App):
    # ErrorDispatcher: Class that passes errors either to RestApiErrorHandler (returning JSON responses).
    error_handler_kwargs = {
        'logger': dependencies.get_logger(),
        'db_session': dependencies.get_db_session(),
        'debug': bool(app.config['DEBUG']),
    }
    error_dispatcher = ErrorDispatcher(RestApiErrorHandler(**error_handler_kwargs))

    @app.errorhandler(Exception)
    def handle_exception(error: Exception):
        return error_dispatcher.dispatch_error(error, request)
