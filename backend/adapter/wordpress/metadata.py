#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from app_config import db


class Metadata(db.Model):
    __tablename__ = 'wp_postmeta'
    id = db.Column('meta_id', db.Integer, primary_key=True)
    post_id = db.Column('post_id', db.Integer)
    meta_key = db.Column('meta_key', db.String)
    meta_value = db.Column('meta_value', db.String)


    def to_dict(self):
        return {self.meta_key: self.meta_value}
