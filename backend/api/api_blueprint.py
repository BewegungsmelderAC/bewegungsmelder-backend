#!/usr/bin/env python3
# -*- coding: utf-8 -*-


#  standard imports
import logging
# third party imports
from flask import Blueprint, Response
from prometheus_client import generate_latest, Counter
# custom imports
from backend.utility import ApiResponse, ApiResponseStatus
from backend.service.event_service import get_event, get_events_by_day
from datetime import datetime

APIBlueprint = Blueprint('api', __name__)
requests_metrics = Counter('requests_total', 'HTTP Requests', ['endpoint', 'method'])


@APIBlueprint.route('/event', methods=['GET'])  # get all
def get_events():
    result = ApiResponse()
    result.status = ApiResponseStatus.NOT_FOUND
    requests_metrics.labels(endpoint='/api/event', method="GET").inc()
    return result.to_json(), result.status.value


@APIBlueprint.route('/event/<event_id>', methods=['GET'])  # get single event by id
def get_single_event(event_id):
    result = ApiResponse()
    event = get_event(event_id)
    if event == {}:
        result.status = ApiResponseStatus.NOT_FOUND
        requests_metrics.labels(endpoint='/api/event/{}'.format(event_id), method="GET").inc()
    else:
        result.data = event
        result.status = ApiResponseStatus.SUCCESS
    return result.to_json(), result.status.value


@APIBlueprint.route('/event/by-day/<day>', methods=['GET'])  # get all events of one day
def get_day_events(day: str):
    result = ApiResponse()
    try:
        real_day = datetime.strptime(day, "%d-%m-%Y")
    except ValueError:
        result.status = ApiResponseStatus.CONFLICT
        result.error_message = "Could not convert date, please use DD-MM-YYYY"
        requests_metrics.labels(endpoint='/api/event/by-day/{}'.format(day), method="GET").inc()
        return result.to_json(), result.status.value
    events=get_events_by_day(real_day.date())
    if not events:
        result.status = ApiResponseStatus.NOT_FOUND
        result.error_message = "No events found for that day"
        requests_metrics.labels(endpoint='/api/event/by-day/{}'.format(day), method="GET").inc()
    else:
        result.data = events
        result.status = ApiResponseStatus.SUCCESS
    return result.to_json(), result.status.value


@APIBlueprint.route('/metrics', methods=['GET'])
def metrics():
    return Response(generate_latest())