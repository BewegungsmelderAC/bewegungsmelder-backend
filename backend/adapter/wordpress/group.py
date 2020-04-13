#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# created by Alwin Ebermann (alwin@alwin.net.au)

from app_config import db


class Group(db.Model):
    __tablename__ = 'wp_bp_groups'
    slug = db.Column('slug', db.String)
    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column('name', db.String(255))
    description = db.Column('description', db.String)
    date_created = db.Column('date_created', db.DateTime())
