#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from app import db


class Event(db.Model):
    __tablename__ = 'wp_em_events'
    name = db.Column('event_name', db.String)
    url = db.Column('event_slug', db.String)
    id = db.Column('event_id', db.Integer, primary_key=True)
    start = db.Column('event_start', db.DateTime())
    end = db.Column('event_end', db.DateTime())
    all_day = db.Column('event_all_day', db.Boolean)
    content = db.Column('post_content', db.String)
    location_id = db.Column('location_id', db.ForeignKey('location.location_id'))
    location = db.relationship("Location", primaryjoin="Event.location_id == Location.id", foreign_keys=location_id,
                               backref="events")
    # because location_id is not a ForeignKey, we need primaryjoin
    group_id = db.Column('group_id', db.String(), db.ForeignKey('group.id'))
    group = db.relationship("Group", primaryjoin="Event.group_id == Group.id", foreign_keys=group_id,
                            backref="events")
    recurrence = db.Column("recurrence", db.Integer)
    # event category missing
