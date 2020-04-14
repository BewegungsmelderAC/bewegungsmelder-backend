#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging

from sqlalchemy import func

from backend.adapter.wordpress.location import Location
from backend.adapter.wordpress.group import Group
from backend.adapter.wordpress.metadata import Metadata
from backend.adapter.wordpress.event import Event
from datetime import date
from datetime import datetime

from app_config import db
from backend.service.group_service import group_to_compact_dict
from backend.service.location_service import location_to_compact_dict


def create_filter(count: int = 30, page: int = 1, from_datetime: datetime = datetime.now()):
    # This sets defaults for values not set in the request
    return {"count": count, "page": page, "from": from_datetime}


def event_to_compact_dict(event: Event) -> dict:
    logging.debug("processing event {} from {} to {}".format(event.name, event.start, event.end))
    location = location_to_compact_dict(event.location) if event.location is not None else {}
    group = group_to_compact_dict(event.group) if event.group is not None else {}
    return {
        "name": event.name,
        "id": event.id,
        "location": location,
        "group": group,
        "start": event.start,
        "end": event.end,
        "category": event.category.meta_value if event.category is not None else "Veranstaltungsart nicht angegeben"
    }


def event_to_full_dict(event: Event) -> dict:
    logging.debug("processing event {} from {} to {}".format(event.name, event.start, event.end))
    location = location_to_compact_dict(event.location) if event.location is not None else {}
    group = group_to_compact_dict(event.group) if event.group is not None else {}
    return {
        "name": event.name,
        "id": event.id,
        "location": location,
        "group": group,
        "start": event.start,
        "end": event.end,
        "category": event.category.meta_value if event.category is not None else "Veranstaltungsart nicht angegeben",
        "recurrence": event.recurrence,
        "all_day": event.all_day,
        "content": event.content,
        "slug": event.slug
    }


def get_events_by_filter(from_dt: datetime, page: int, count: int, group_ids: list) -> list:

    # construct group filter
    if len(group_ids) == 0:
        group_condition = True
    else:
        group_condition = Event.group_id == int(group_ids[0])
        if len(group_ids) > 1:
            for i in range(1, len(group_ids)):
                group_condition = db.or_(group_condition, Event.group_id == int(group_ids[i]))

    # construct complete filter
    events = Event.query.filter(db.and_(Event.end >= from_dt), group_condition).paginate(page=page, per_page=count)
    events_dict = []
    for event in events.items:
        events_dict.append(event_to_compact_dict(event))
    return events_dict


def get_event(id: int) -> dict:
    event = Event.query.get(id)
    if event is None:
        return {}
    data = event_to_full_dict(event)
    return data


def get_events_by_day(day: date) -> list:
    logging.debug("Getting events for day {}".format(day))
    events = Event.query.filter(db.and_(func.date(Event.start) <= day,
                                        func.date(Event.end) >= day, db.or_(Event.recurrence == 0,
                                                                            Event.recurrence == None))).all()
    logging.debug("Retrieved {} events".format(len(events)))
    events_dict = []
    for event in events:
        events_dict.append(event_to_compact_dict(event))
    return events_dict
