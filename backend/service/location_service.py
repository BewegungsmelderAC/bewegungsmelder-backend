#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from backend.adapter.wordpress.location import Location


def location_to_compact_dict(location: Location) -> dict:
    return {"name": location.name,
            "id": location.id}


def location_to_full_dict(location: Location) -> dict:
    return {"name": location.name,
            "id": location.id,
            "town": location.town,
            "address": location.address,
            "slug": location.slug,
            "content": location.content}


def get_location(location_id: int) -> dict:
    location = Location.query.get(location_id)
    if location is None:
        return {}
    else:
        return location_to_full_dict(location)


def get_locations_by_filter(page: int, count:int) ->list:
    locations = Location.query.paginate(page=page, per_page=count)
    location_dicts = []
    for location in locations.items:
        location_dicts.append(location_to_compact_dict(location))
    return location_dicts
