#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime
from regex import fullmatch

from backend.service.event_service import get_event, get_events_by_day, get_events_by_filter, get_event_by_slug, \
    get_types
from flask import abort


def get_single_event(event_id: int):
    event = get_event(event_id)
    if event == {}:
        abort(404, "Event not found for Id: {}".format(event_id))
    else:
        return event


def get_single_event_by_slug(event_slug: str):
    event = get_event_by_slug(event_slug)
    if event == {}:
        abort(404, "Event not found for slug: {}".format(event_slug))
    else:
        return event


def get_day_events(date: str):
    try:
        real_day = datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        abort(400, "Could not convert date, please use YYYY-MM-DD")
    else:
        events = get_events_by_day(real_day.date())
        if not events:
            abort(404, "No events found for that day")
        else:
            return events


def get_filtered_events(page: int, per_page: int, from_datetime: str = "", group_ids: str = "", location_ids: str = "",
                        types: str = "", terms: str = "", text: str = "", backwards: bool = False):
    valid_text = fullmatch(r"[\p{L} ]*", text)
    if valid_text is None:
        abort(400, "Input search string invalid, only letters and spaces allowed")
    group_ids = group_ids.split(",")  # split ids
    group_ids = [int(x) for x in group_ids if x]  # remove empty elements
    location_ids = location_ids.split(",")  # split ids
    location_ids = [int(x) for x in location_ids if x]  # remove empty elements
    event_types = types.split(";")  # split ids
    event_types = [x for x in event_types if x]  # remove empty elements
    terms = terms.split(",")  # split ids
    terms = [x for x in terms if x]  # remove empty elements
    if from_datetime == "":
        from_dt = datetime.now()
    else:
        try:
            from_dt = datetime.fromisoformat(from_datetime.replace("Z", "+00:00"))
        except ValueError:
            abort(400, "Incorrect from_datetime")
            return
    events = get_events_by_filter(from_dt=from_dt, page=page, count=per_page, group_ids=group_ids,
                                  location_ids=location_ids, event_types=event_types, terms=terms, text=text, backwards=backwards)
    if not events:
        abort(404, "No events found for selected filter")
    else:
        return events


def get_event_types():
    return get_types()