#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from app_config import db


class FullEvent(db.Model):
    __tablename__ = 'events_all'
    id = db.Column('event_id', db.Integer, primary_key=True)
    veranstaltungsart = db.Column('veranstaltungsart', db.String)
    image = db.Column('event_image', db.String)
