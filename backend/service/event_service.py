#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging
import re

from sqlalchemy import func

# we need all imports because otherwise Event won't know about them
from backend.adapter.wordpress.location import Location
from backend.adapter.wordpress.group import Group
from backend.adapter.wordpress.metadata import Metadata
from backend.adapter.wordpress.event import Event
from datetime import date
from datetime import datetime

from app_config import db
from backend.adapter.wordpress.option import Option
from backend.service.group_service import group_to_compact_dict
from backend.service.location_service import location_to_compact_dict
from backend.utility import construct_filter_statement, unescape_db_to_plain


def event_to_compact_dict(event: Event) -> dict:
    location = location_to_compact_dict(event.location) if event.location is not None else {}
    group = group_to_compact_dict(event.group) if event.group is not None else {}
    return {
        "name": unescape_db_to_plain(event.name),
        "slug": event.slug,
        "location": location,
        "group": group,
        "start": event.start,
        "end": event.end,
        "type": event.event_type,
        "thumbnail": event.get_thumbnail_image()
    }


def event_to_full_dict(event: Event) -> dict:
    logging.debug("processing event {} from {} to {}".format(event.name, event.start, event.end))
    location = location_to_compact_dict(event.location) if event.location is not None else {}
    group = group_to_compact_dict(event.group) if event.group is not None else {}
    return {
        "metadata": event.get_all_metadata(),  # this also populates the fields read from the metadata table
        "name": unescape_db_to_plain(event.name),
        "id": event.id,
        "location": location,
        "group": group,
        "start": event.start,
        "end": event.end,
        "type": event.event_type,
        "all_day": event.all_day,
        "content": event.content,
        "slug": event.slug,
        "image": event.get_full_image(),
        "telephone": event.telephone,
        "accessible": event.accessible,
        "contact_email": event.contact_email,
        "website": event.website,
        "terms": [{"name": x.name, "slug": x.slug} for x in event.terms]
    }


def get_events_by_filter(from_dt: datetime, page: int, count: int, group_ids: list, location_ids: list,
                         event_types: list, terms: list, text: str, backwards: bool) -> list:
    text_condition = Event.name.like("%{}%".format(text)) if text != "" else True
    location_condition = construct_filter_statement(location_ids, Event.location_id)
    group_condition = construct_filter_statement(group_ids, Event.group_id)
    type_condition = construct_filter_statement(event_types, Event.event_type)
    terms_condition = construct_filter_statement(terms, Event.terms_slugs)
    # construct complete filter
    if backwards:
        events = Event.query.filter(Event.end < from_dt, group_condition, location_condition, terms_condition,
                                    type_condition, Event.visibility != 0, db.or_(Event.recurrence == 0,
                                                                                  Event.recurrence == None),
                                    text_condition) \
            .order_by(Event.start.desc()).paginate(page=page, per_page=count)
    else:
        events = Event.query.filter(Event.end >= from_dt, group_condition, location_condition, terms_condition,
                                    type_condition, Event.visibility != 0, db.or_(Event.recurrence == 0,
                                                                                  Event.recurrence == None),
                                    text_condition) \
            .order_by(Event.start.asc()).paginate(page=page, per_page=count)
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
    events = Event.query.filter(db.and_(Event.visibility != 0,
                                        func.date(Event.start) <= day,
                                        func.date(Event.end) >= day, db.or_(Event.recurrence == 0,
                                                                            Event.recurrence == None))) \
        .order_by(Event.start.asc()).all()
    logging.debug("Retrieved {} events".format(len(events)))
    events_dict = []
    for event in events:
        events_dict.append(event_to_compact_dict(event))
    return events_dict


def get_types() -> list:
    options: Option = Option.query.filter(Option.name == "dbem_placeholders_custom").one()
    types_string = re.search(r"Veranstaltungsart}{(.*)}", options.value)
    types = types_string.groups()[0].split("|")
    return types
