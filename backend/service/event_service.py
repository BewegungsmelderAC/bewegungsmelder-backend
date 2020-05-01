#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging

from sqlalchemy import func

# we need all imports because otherwise Event won't know about them
from backend.adapter.wordpress.location import Location
from backend.adapter.wordpress.group import Group
from backend.adapter.wordpress.metadata import Metadata
from backend.adapter.wordpress.event import Event
from datetime import date
from datetime import datetime

from app_config import db
from backend.service.group_service import group_to_compact_dict
from backend.service.location_service import location_to_compact_dict


def construct_filter_statement(items: list, col: db.Column):
    condition = False
    if len(items) > 0:
        for i in range(0, len(items)):
            condition = db.or_(condition, col == items[i])
    else:
        condition = True
    return condition


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
        "category": event.category
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
        "category": event.category,
        "recurrence": event.recurrence,
        "all_day": event.all_day,
        "content": event.content,
        "slug": event.slug,
        "image": event.get_image(),
    }


def get_events_by_filter(from_dt: datetime, page: int, count: int, group_ids: list, location_ids: list, categories: list) -> list:

    location_condition = construct_filter_statement(location_ids, Event.location_id)
    group_condition = construct_filter_statement(group_ids, Event.group_id)
    categories_condition = construct_filter_statement(categories, Event.category)

    # construct complete filter
    events = Event.query.filter(db.and_(Event.end >= from_dt), group_condition, location_condition,
                                categories_condition, db.or_(Event.recurrence == 0,
                                                             Event.recurrence == None)).paginate(page=page,
                                                                                                 per_page=count)
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
