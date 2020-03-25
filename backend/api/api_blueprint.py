#!/usr/bin/env python3
# -*- coding: utf-8 -*-


#  standard imports
import logging
# third party imports
from flask import Blueprint, Response
from prometheus_client import generate_latest, Counter
# custom imports
from backend.utility import ApiResponse, ApiResponseStatus

APIBlueprint = Blueprint('api', __name__)
requests_metrics = Counter('requests_total', 'HTTP Requests', ['endpoint', 'method'])


@APIBlueprint.route('/events', methods=['GET'])  # get all
def get_zeppelin_instances():
    result = ApiResponse()
    result.status = ApiResponseStatus.NOT_FOUND
    requests_metrics.labels(endpoint='/api/events', method="GET").inc()
    return result.to_json(), result.status.value


@APIBlueprint.route('/metrics', methods=['GET'])
def metrics():
    return Response(generate_latest())