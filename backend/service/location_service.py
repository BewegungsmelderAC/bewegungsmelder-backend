#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from backend.adapter.wordpress.location import Location


def location_to_compact_dict(location: Location) -> dict:
    return {"name": location.name,
            "slug": location.slug}


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


def get_location_by_slug(location_slug: str) -> dict:
    location = Location.query.filter(Location.slug == location_slug).one_or_none()
    if location is None:
        return {}
    else:
        return location_to_full_dict(location)


def get_locations_by_filter(page: int, count:int, text: str) ->list:
    text_condition = Location.name.like("%{}%".format(text)) if text != "" else True
    locations = Location.query.filter(text_condition).paginate(page=page, per_page=count)
    location_dicts = []
    for location in locations.items:
        location_dicts.append(location_to_compact_dict(location))
    return location_dicts
