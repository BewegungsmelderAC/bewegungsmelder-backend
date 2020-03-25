#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Contains all customizable settings in form of environment variables.
Some of the settings have default values that are used if the env variable is not set.
These are defined in this file as well.
Caution: If there is no default value for a setting, then the system will crash if that env variable
is not set. This is to ensure all important settings are configured.
The settings are grouped by topic:
1. Required settings (Application will not start, if these are not set)
2. General settings
"""
import os


# -------------------------------------------------------------------------------
# 1. Required settings
# -------------------------------------------------------------------------------
WP_DATABASE_HOST = os.environ['BM_WP_DATABASE_HOST']
WP_DATABASE_USER = os.environ['BM_WP_DATABASE_USER']
WP_DATABASE_PASSWORD = os.environ['BM_WP_DATABASE_PASSWORD']
WP_DATABASE_NAME = os.environ['BM_WP_DATABASE_NAME']


# -------------------------------------------------------------------------------
# 2. General settings
# -------------------------------------------------------------------------------

LOGGING_LEVEL = os.getenv('BM_LOGGING_LEVEL', 'INFO')
STATIC_FOLDER = os.getenv('BM_STATIC_FOLDER_PATH', './../bewegungsmelder-web/dist/files')
TEMPLATE_FOLDER = os.getenv('BM_TEMPLATE_FOLDER_PATH', './../bewegungsmelder-web/dist')