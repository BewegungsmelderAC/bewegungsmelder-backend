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
# custom imports
import config
import app_config


logging.getLogger().setLevel(config.LOGGING_LEVEL)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(config.LOGGING_LEVEL)
handler.setFormatter(logging.Formatter(
    '%(asctime)s - %(name)s - level=%(levelname)s - %(message)s')
)
logging.getLogger().addHandler(handler)
logging.info("Connecting to db at {}".format(config.DATABASE_URI))
connex_app = app_config.app
connex_app.add_api("swagger.yml")

if __name__ == '__main__':
    # run our standalone gevent server
    connex_app.run(port=8080, server='gevent')
