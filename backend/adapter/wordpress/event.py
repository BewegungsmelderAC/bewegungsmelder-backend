#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re

from sqlalchemy.ext.associationproxy import association_proxy
from phpserialize import loads

from config import BEWEGUNGSMELDER_BASE
from .metadata import Metadata
from .post import Post
from .full_event import FullEvent
from .term import association_table

from app_config import db


class Event(db.Model):
    __tablename__ = 'wp_em_events'
    name = db.Column('event_name', db.String)
    slug = db.Column('event_slug', db.String)
    event_id = db.Column('event_id', db.Integer, primary_key=True)
    full_event = db.relationship("FullEvent", primaryjoin="Event.event_id == FullEvent.id", foreign_keys=event_id, viewonly=True)
    post_id = db.Column('post_id', db.Integer)
    start = db.Column('event_start', db.DateTime())
    end = db.Column('event_end', db.DateTime())
    all_day = db.Column('event_all_day', db.Boolean)
    content = db.Column('post_content', db.String)
    location_id = db.Column('location_id', db.Integer, db.ForeignKey('wp_em_locations.location_id'))
    location = db.relationship("Location", primaryjoin="Event.location_id == Location.id", foreign_keys=location_id,
                               viewonly=True)
    # because location_id is not a ForeignKey, we need primaryjoin
    group_id = db.Column('group_id', db.Integer, db.ForeignKey('wp_bp_groups.id'))
    group = db.relationship("Group", primaryjoin="Event.group_id == Group.id", foreign_keys=group_id, viewonly=True)
    event_type = association_proxy('full_event', 'veranstaltungsart')
    recurrence = db.Column("recurrence", db.Integer)
    recurrence_id = db.Column("recurrence_id", db.Integer)
    recurrence_parent = db.relationship("Event", primaryjoin="Event.recurrence_id == Event.event_id", remote_side=[event_id],
                                        foreign_keys=recurrence_id, backref="recurrence_children")
    visibility = db.Column("event_status", db.Integer)  # 0 means not visible, None and 1 mean visible
    telephone = ""
    contact_email = ""
    accessible = "Nein"
    website = ""
    terms = db.relationship("Term", secondary=association_table, viewonly=True)
    terms_slugs = association_proxy('terms', 'slug')

    def get_full_image(self):
        if "group-avatars" not in self.full_event.image:
            return BEWEGUNGSMELDER_BASE + self.full_event.image
        else:
            # this is non-standard behaviour - the website does not show this picture in the event details
            return self.group.get_avatar()

    def get_thumbnail_image(self):
        if "group-avatars" not in self.full_event.image:
            thumb = re.sub(r"(\.[a-zA-Z]*$)", r"-150x150\g<1>", self.full_event.image)
            return BEWEGUNGSMELDER_BASE + thumb
        else:
            return self.group.get_avatar()

    def get_all_metadata(self):
        metadata = Metadata.query.filter(Metadata.post_id == self.post_id).all()
        meta = {}
        for metaentry in metadata:
            if not metaentry.meta_key.startswith("_") and metaentry.meta_value != "":
                if metaentry.meta_key == "Kontakt-Telefon":
                    self.telephone = metaentry.meta_value
                elif metaentry.meta_key == "Barrierefrei":
                    self.accessible = metaentry.meta_value
                elif metaentry.meta_key == "Kontakt-Email":
                    self.contact_email = metaentry.meta_value
                elif metaentry.meta_key == "Veranstaltungsart":
                    continue
                elif metaentry.meta_key == "weiterführende Links 1":
                    self.website = metaentry.meta_value
                else:
                    meta[metaentry.meta_key] = metaentry.meta_value
                # add more metadata here if necessary
        return meta
