#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import abort
from backend.service.location_service import get_location, get_locations_by_filter


def get_single_location(location_id: int = None):
    if location_id is None:
        abort(400, "Invalid group id")
    else:
        location = get_location(location_id)
        if location == {}:
            abort(404, "Location not found")
        else:
            return location


def get_filtered_locations(page: int, per_page: int):
    locations = get_locations_by_filter(page=page, count=per_page)
    if not locations:
        abort(404, "No locations found for selected filter")
    else:
        return locations