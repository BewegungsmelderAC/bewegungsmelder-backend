#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os

try:
    DATABASE_URI = os.environ['BM_WP_DATABASE_URI']
except KeyError:
    WP_DATABASE_HOST = os.environ['BM_WP_DATABASE_HOST']
    WP_DATABASE_USER = os.environ['BM_WP_DATABASE_USER']
    WP_DATABASE_PASSWORD = os.environ['BM_WP_DATABASE_PASSWORD']
    WP_DATABASE_NAME = os.environ['BM_WP_DATABASE_NAME']
    DATABASE_URI = "mysql://{}:{}@{}/{}".format(WP_DATABASE_USER, WP_DATABASE_PASSWORD, WP_DATABASE_HOST, WP_DATABASE_NAME)

# -------------------------------------------------------------------------------
# 2. General settings
# -------------------------------------------------------------------------------

LOGGING_LEVEL = os.getenv('BM_LOGGING_LEVEL', 'INFO')
STATIC_FOLDER = os.getenv('BM_STATIC_FOLDER_PATH', './../bewegungsmelder-web/dist/files')
TEMPLATE_FOLDER = os.getenv('BM_TEMPLATE_FOLDER_PATH', './../bewegungsmelder-web/dist')