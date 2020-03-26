#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging

from sqlalchemy import and_, func

from backend.adapter.wordpress.location import Location
from backend.adapter.wordpress.group import Group
from backend.adapter.wordpress.event import Event
from datetime import date

from app import db


def event_to_dict(event: Event) -> dict:
    logging.debug("processing event {} from {} to {}".format(event.name, event.start, event.end))
    location = {"name": event.location.name,
                "id": event.location_id,
                "address": event.location.address,
                "town": event.location.town} if event.location is not None else {}
    group = {
        "name": event.group.name,
        "id": event.group_id,
    } if event.group is not None else {}
    return {
        "name": event.name,
        "id": event.id,
        "location": location,
        "group": group,
        "start": event.start,
        "end": event.end
    }


def get_event(id: int) -> dict:
    event = Event.query.get(id)
    if event is None:
        return {}
    data = event_to_dict(event)
    return data


def get_events_by_day(day: date) -> list:
    logging.debug("Getting events for day {}".format(day))
    events = Event.query.filter(db.and_(func.date(Event.start) <= day,
                                        func.date(Event.end) >= day, db.or_(Event.recurrence == 0,
                                                                            Event.recurrence == None))).all()
    logging.debug("Retrieved {} events".format(len(events)))
    events_dict = []
    for event in events:
        events_dict.append(event_to_dict(event))
    return events_dict
