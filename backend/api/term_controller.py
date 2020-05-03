#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from regex import fullmatch

from backend.service.term_service import get_terms_by_type
from flask import abort


def get_all_event_terms(text: str=""):
    valid_text = fullmatch(r"[\p{L} ]*", text)
    if valid_text is None:
        abort(400, "Input search string invalid, only letters and spaces allowed")
    terms = get_terms_by_type("event-categories", text=text)
    if len(terms) == 0:
        abort(404, "No terms found")
    else:
        return terms


def get_all_group_terms(text: str=""):
    valid_text = fullmatch(r"[\p{L} ]*", text)
    if valid_text is None:
        abort(400, "Input search string invalid, only letters and spaces allowed")
    terms = get_terms_by_type("bp_group_type", text=text)
    if len(terms) == 0:
        abort(404, "No terms found")
    else:
        return terms