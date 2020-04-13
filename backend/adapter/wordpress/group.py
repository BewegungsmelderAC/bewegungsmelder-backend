#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# created by Alwin Ebermann (alwin@alwin.net.au)

from sqlalchemy import Column, String, Integer
from app_config import db


class Group(db.Model):
    __tablename__ = 'wp_bp_groups'
    slug = Column('slug', String)
    id = Column('id', Integer, primary_key=True)
    name = Column('name', String(255))
    description = Column('description', String)
