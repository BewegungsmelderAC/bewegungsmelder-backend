#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from app import db


class Location(db.Model):
    __tablename__ = 'wp_em_locations'
    id = db.Column('location_id', db.Integer, primary_key=True)
    name = db.Column('location_name', db.String)
    address = db.Column('location_address', db.String)
    town = db.Column('location_town', db.String)
