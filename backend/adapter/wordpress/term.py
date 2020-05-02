#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from app_config import db

association_table = db.Table('wp_term_relationships', db.Model.metadata,
                             db.Column('object_id', db.Integer, db.ForeignKey('wp_em_events.post_id'), db.ForeignKey('wp_bp_groups.id')),
                             db.Column('term_taxonomy_id', db.Integer, db.ForeignKey('wp_terms.term_id')),
                             )

class Term(db.Model):
    __tablename__ = 'wp_terms'
    id = db.Column('term_id', db.Integer, primary_key=True)
    name = db.Column('name', db.String)
    slug = db.Column('slug', db.String)
    term_group = db.Column('term_group', db.Integer)  # this is unused and here only for completeness
