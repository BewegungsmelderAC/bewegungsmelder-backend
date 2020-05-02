#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from backend.service.term_service import get_terms_by_type
from flask import abort


def get_all_event_terms():
    terms = get_terms_by_type("event-categories")
    if len(terms) == 0:
        abort(404, "No terms found")
    else:
        return terms


def get_all_group_terms():
    terms = get_terms_by_type("bp_group_type")
    if len(terms) == 0:
        abort(404, "No terms found")
    else:
        return terms