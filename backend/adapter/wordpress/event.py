#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from sqlalchemy.ext.associationproxy import association_proxy

from app_config import db


class Event(db.Model):
    __tablename__ = 'wp_em_events'
    name = db.Column('event_name', db.String)
    slug = db.Column('event_slug', db.String)
    id = db.Column('event_id', db.Integer, primary_key=True)
    post_id = db.Column('post_id', db.Integer)
    start = db.Column('event_start', db.DateTime())
    end = db.Column('event_end', db.DateTime())
    all_day = db.Column('event_all_day', db.Boolean)
    content = db.Column('post_content', db.String)
    location_id = db.Column('location_id', db.Integer, db.ForeignKey('wp_em_locations.location_id'))
    location = db.relationship("Location", primaryjoin="Event.location_id == Location.id", foreign_keys=location_id,
                               backref="events")
    # because location_id is not a ForeignKey, we need primaryjoin
    group_id = db.Column('group_id', db.Integer, db.ForeignKey('wp_bp_groups.id'))
    group = db.relationship("Group", primaryjoin="Event.group_id == Group.id", foreign_keys=group_id,
                            backref="events")
    category_item = db.relationship("Metadata", primaryjoin="and_(Event.post_id == Metadata.post_id, "
                                                       "Metadata.meta_key=='Veranstaltungsart')", foreign_keys=post_id,
                               backref="events", viewonly=True) # this is the full line of the metadata table
    category = association_proxy('category_item', 'meta_value') # this is only the meta_value from the category entry
    recurrence = db.Column("recurrence", db.Integer)
    # event category missing
