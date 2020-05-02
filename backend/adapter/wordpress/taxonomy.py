#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from app_config import db


class Taxonomy(db.Model):
    __tablename__ = 'wp_term_taxonomy'
    id = db.Column('term_taxonomy_id', db.Integer, primary_key=True)
    term_id = db.Column('term_id', db.Integer)
    taxonomy = db.Column('taxonomy', db.String)
    description = db.Column('description', db.String)  # not in use
    parent = db.Column('parent', db.Integer)  # not in use
    count = db.Column('count', db.Integer)
