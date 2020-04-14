#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from backend.adapter.wordpress.location import Location


def location_to_compact_dict(location: Location) -> dict:
    return {"name": location.name,
            "id": location.id}
