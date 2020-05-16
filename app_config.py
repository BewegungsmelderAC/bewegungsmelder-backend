#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import os
import connexion
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

import config

basedir = os.path.abspath(os.path.dirname(__file__))
app = connexion.App(__name__, specification_dir=basedir)
CORS(app.app)

application = app.app

application.config['SQLALCHEMY_DATABASE_URI'] = config.DATABASE_URI
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(application)