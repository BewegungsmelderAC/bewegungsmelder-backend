#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from app_config import db


class Option(db.Model):
    __tablename__="wp_options"
    id = db.Column('option_id', db.Integer, primary_key=True)
    name = db.Column('option_name', db.String)
    value = db.Column('option_value', db.String)
    autoload = db.Column('autoload', db.String) # no idea what this is about
