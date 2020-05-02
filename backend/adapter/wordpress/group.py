#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# created by Alwin Ebermann (alwin@alwin.net.au)
import logging

import requests
from sqlalchemy.ext.associationproxy import association_proxy

import config
from app_config import db
from .metadata import Metadata
from .post import Post
from .term import Term
from .term import association_table


class Group(db.Model):
    __tablename__ = 'wp_bp_groups'
    slug = db.Column('slug', db.String)
    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column('name', db.String(255))
    description = db.Column('description', db.String)
    date_created = db.Column('date_created', db.DateTime())
    post_id_item = db.relationship("Metadata", primaryjoin="and_(Metadata.meta_value==Group.id, "
                                                           "Metadata.meta_key=='group_id')",
                                   foreign_keys=id,
                                   backref="group", viewonly=True)  # this is the full line of the metadata table
    post_id = association_proxy('post_id_item', 'post_id')
    terms = db.relationship("Term",
                            secondary=association_table,
                            backref="groups")
    contact_email = ""
    contact_name = ""
    website = ""
    meetup_description = ""
    telephone = ""
    avatar_url = ""
    cover_url = "https://www.incimages.com/uploaded_files/image/970x450/getty_509107562_2000133320009280346_351827.jpg"

    def get_all_metadata(self):
        metadata = Metadata.query.filter(Metadata.post_id == self.post_id).all()
        meta = {}
        for metaentry in metadata:
            if not metaentry.meta_key.startswith("_") and metaentry.meta_value != "":
                if metaentry.meta_key == "telefon":
                    self.telephone = metaentry.meta_value
                elif metaentry.meta_key == "name":
                    self.contact_name = metaentry.meta_value
                elif metaentry.meta_key == "email":
                    self.contact_email = metaentry.meta_value
                elif metaentry.meta_key == "internetseite":
                    self.website = metaentry.meta_value
                elif metaentry.meta_key == "treffen":
                    self.meetup_description = metaentry.meta_value
                else:
                    meta[metaentry.meta_key] = metaentry.meta_value
                # add more metadata here if necessary
        return meta

    def get_avatar(self):
        if self.avatar_url == "":
            r = requests.get("{}/wp-json/buddypress/v1/groups/{}/avatar".format(config.BEWEGUNGSMELDER_BASE, self.id))
            if r.ok:
                self.avatar_url = r.json()[0]["thumb"]
            else:
                logging.warning("Error retrieving avatar for group " + self.name + "error is " + r.text)
        return self.avatar_url

    def get_cover(self):
        logging.warning("Cover URL not available due do missing BuddyPress support")
        return self.cover_url
