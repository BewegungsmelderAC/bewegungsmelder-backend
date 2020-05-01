#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from app_config import db


class Post(db.Model):
    __tablename__ = 'wp_posts'
    id = db.Column('ID', db.Integer, primary_key=True)
    content = db.Column('post_content', db.String)
    status = db.Column('post_status', db.String)
    parent = db.Column('post_parent', db.Integer)
    guid = db.Column('guid', db.String)
    type = db.Column('post_type', db.String)
