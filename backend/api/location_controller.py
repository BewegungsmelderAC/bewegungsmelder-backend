#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import abort
from regex import fullmatch

from backend.service.location_service import get_location, get_locations_by_filter, get_location_by_slug


def get_single_location(location_id: int = None):
    if location_id is None:
        abort(400, "Invalid group id")
    else:
        location = get_location(location_id)
        if location == {}:
            abort(404, "Location not found")
        else:
            return location


def get_single_location_by_slug(location_slug: str):
    location = get_location_by_slug(location_slug)
    if location == {}:
        abort(404, "Location not found")
    else:
        return location


def get_filtered_locations(page: int, per_page: int, text: str = ""):
    valid_text = fullmatch(r"[\p{L} ]*", text)
    if valid_text is None:
        abort(400, "Input search string invalid, only letters and spaces allowed")
    locations = get_locations_by_filter(page=page, count=per_page, text=text)
    if not locations:
        abort(404, "No locations found for selected filter")
    else:
        return locations
