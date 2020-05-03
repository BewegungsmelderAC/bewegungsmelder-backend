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
from backend.utility import construct_filter_statement


def event_to_compact_dict(event: Event) -> dict:
    logging.debug("processing event {} from {} to {}".format(event.name, event.start, event.end))
    location = location_to_compact_dict(event.location) if event.location is not None else {}
    group = group_to_compact_dict(event.group) if event.group is not None else {}
    return {
        "name": event.name,
        "slug": event.slug,
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
        "metadata": event.get_all_metadata(),  # this also populates the fields read from the metadata table
        "name": event.name,
        "id": event.id,
        "location": location,
        "group": group,
        "start": event.start,
        "end": event.end,
        "category": event.category,
        "all_day": event.all_day,
        "content": event.content,
        "slug": event.slug,
        "image": event.get_image(),
        "telephone": event.telephone,
        "accessible": event.accessible,
        "contact_email": event.contact_email,
        "website": event.website,
        "terms": [{"name": x.name, "slug": x.slug} for x in event.terms]
    }


def get_events_by_filter(from_dt: datetime, page: int, count: int, group_ids: list, location_ids: list,
                         categories: list, terms: list, text: str) -> list:
    text_condition = Event.name.like("%{}%".format(text)) if text != "" else True
    location_condition = construct_filter_statement(location_ids, Event.location_id)
    group_condition = construct_filter_statement(group_ids, Event.group_id)
    categories_condition = construct_filter_statement(categories, Event.category)
    terms_condition = construct_filter_statement(terms, Event.terms_slugs)
    # construct complete filter
    events = Event.query.filter(db.and_(Event.end >= from_dt, group_condition, location_condition, terms_condition,
                                categories_condition, Event.event_status != 0, db.or_(Event.recurrence == 0,
                                Event.recurrence == None), text_condition)).paginate(page=page, per_page=count)
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


def get_event_by_slug(slug: str) -> dict:
    event = Event.query.filter(Event.slug == slug).one_or_none()
    if event is None:
        return {}
    data = event_to_full_dict(event)
    return data


def get_events_by_day(day: date) -> list:
    logging.debug("Getting events for day {}".format(day))
    events = Event.query.filter(db.and_(Event.event_status != 0,
                                        func.date(Event.start) <= day,
                                        func.date(Event.end) >= day, db.or_(Event.recurrence == 0,
                                                                            Event.recurrence == None))).all()
    logging.debug("Retrieved {} events".format(len(events)))
    events_dict = []
    for event in events:
        events_dict.append(event_to_compact_dict(event))
    return events_dict
