#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Entry point for the Flask Application.
Tasks:
1. Configure logging
2. Create application object and enable CORS
3. Validate and apply configuration
4. Register the API through flask blueprints
5. Register error handlers and their corresponding Prometheus metrics
"""

#  standard import
import sys
import logging
# third party imports
from flask_cors import CORS
from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy
from prometheus_client import Counter
# custom imports
import config

http_error_metric = Counter('http_errors_total', 'HTTP Errors', ['type'])
db = SQLAlchemy()


def create_app():
    logging.getLogger().setLevel(config.LOGGING_LEVEL)
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(config.LOGGING_LEVEL)
    handler.setFormatter(logging.Formatter(
        '%(asctime)s - %(name)s - level=%(levelname)s - %(message)s')
    )
    logging.getLogger().addHandler(handler)
    logging.info('Configured logging to stdout.')
    logging.info('Starting Flask application...')
    app = FlaskAPI(__name__,
                   static_folder=config.STATIC_FOLDER,
                   template_folder=config.TEMPLATE_FOLDER,
                   instance_relative_config=True)
    app.config['SQLALCHEMY_DATABASE_URI'] = config.DATABASE_URI
    logging.info("Connecting to db at {}".format(config.DATABASE_URI))
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    logging.info('Flask application started.')
    logging.info('Validating configuration...')
    try:
        app.config.from_object(config)
    except KeyError as e:
        logging.error(e)
        sys.exit(-1)
    logging.info('Config is valid...')
    logging.info('Configuring CORS...')
    CORS(app)
    logging.info('CORS configured.')
    logging.info('Configuring RequestID...')
    logging.info('RequestID configured.')
    logging.info('Registering application blueprints...')
    from backend.api import APIBlueprint
    app.register_blueprint(APIBlueprint)
    logging.info('Application blueprints registered.')
    logging.info('Registering error handlers and metrics...')

    @APIBlueprint.errorhandler(500)
    def handle_500(error):
        logging.error('{}'.format(error))
        http_error_metric.labels(type='500').inc()
        return str(error), 500

    @app.errorhandler(404)
    def handle_404(error):
        logging.warning('{}'.format(error))
        http_error_metric.labels(type='404').inc()
        return str(error), 404

    @app.errorhandler(401)
    def handle_401(error):
        logging.warning('{}'.format(error))
        http_error_metric.labels(type='401').inc()
        return str(error), 401

    @app.errorhandler(405)
    def handle_405(error):
        logging.warning('{}'.format(error))
        http_error_metric.labels(type='405').inc()
        return str(error), 405
    logging.info('Error handlers and metrics registered.')

    return app
