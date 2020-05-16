#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re

from sqlalchemy.ext.associationproxy import association_proxy
from phpserialize import loads

from config import BEWEGUNGSMELDER_BASE
from .metadata import Metadata
from .post import Post
from .term import association_table

from app_config import db


def get_image_thumbnail(attachment_post_id: int):
    attachment_meta: Metadata = Metadata.query.filter(db.and_(attachment_post_id == Metadata.post_id,
                                                              Metadata.meta_key == '_wp_attachment_metadata')).first()
    image_metadata = loads(bytes(attachment_meta.meta_value, 'utf-8'), decode_strings=True)
    # there's a lot of interesting stuff in image_metadata
    # construct path
    base = BEWEGUNGSMELDER_BASE + "/wp-content/uploads/"
    month_folder = re.match(r"[0-9]{4}/[0-9]{2}/", image_metadata["file"])[0]
    return base + month_folder + image_metadata["sizes"]["thumbnail"]["file"]


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
                               viewonly=True)
    # because location_id is not a ForeignKey, we need primaryjoin
    group_id = db.Column('group_id', db.Integer, db.ForeignKey('wp_bp_groups.id'))
    group = db.relationship("Group", primaryjoin="Event.group_id == Group.id", foreign_keys=group_id,
                            viewonly=True)
    event_type_item = db.relationship("Metadata", primaryjoin="and_(Event.post_id == Metadata.post_id, "
                                                              "Metadata.meta_key=='Veranstaltungsart')",
                                      foreign_keys=post_id,
                                      viewonly=True)  # this is the full line of the metadata table
    event_type = association_proxy('event_type_item',
                                   'meta_value')  # this is only the meta_value from the category entry
    recurrence = db.Column("recurrence", db.Integer)
    recurrence_id = db.Column("recurrence_id", db.Integer)
    recurrence_parent = db.relationship("Event", primaryjoin="Event.recurrence_id == Event.id", remote_side=[id],
                                        foreign_keys=recurrence_id, backref="recurrence_children")
    visibility = db.Column("event_status", db.Integer)  # 0 means not visible, None and 1 mean visible
    telephone = ""
    contact_email = ""
    accessible = "Nein"
    website = ""
    terms = db.relationship("Term", secondary=association_table, viewonly=True)
    terms_slugs = association_proxy('terms', 'slug')

    def get_full_image(self):
        attachment: Post = Post.query.filter(db.and_(Post.parent == self.post_id, Post.type == "attachment")).first()
        if attachment is not None:
            return attachment.guid
        elif self.recurrence_id != 0 and self.recurrence_parent is not None:
            attachment: Post = Post.query.filter(
                db.and_(Post.parent == self.recurrence_parent.post_id, Post.type == "attachment")).first()
            if attachment is not None:
                return attachment.guid
        else:
            # this is non-standard behaviour - the website does not show this picture in the event details
            return self.group.get_avatar()
        return None

    def get_thumbnail_image(self):
        attachment: Post = Post.query.filter(db.and_(Post.parent == self.post_id, Post.type == "attachment")).first()
        if attachment is not None:
            # this is a normal image
            return get_image_thumbnail(attachment.id)
        elif self.recurrence_id != 0 and self.recurrence_parent is not None:
            # we take the image from the parent
            attachment: Post = Post.query.filter(
                db.and_(Post.parent == self.recurrence_parent.post_id, Post.type == "attachment")).first()
            if attachment is not None:
                return get_image_thumbnail(attachment.id)
        # we take the avatar image from the group
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
