#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import abort
from regex import fullmatch

from backend.service.group_service import get_group_by_id, get_groups_by_filter, get_group_by_slug


def get_single_group(group_id: int = None):
    if group_id is None:
        abort(400, "Invalid group id")
    else:
        group = get_group_by_id(group_id)
        if group == {}:
            abort(404, "Group not found")
        else:
            return group


def get_single_group_by_slug(group_slug: str):
    group = get_group_by_slug(group_slug)
    if group == {}:
        abort(404, "Group not found")
    else:
        return group


def get_filtered_groups(page: int, per_page: int, terms: str = "", text: str = ""):
    valid_text = fullmatch(r"[\p{L} ]*", text)
    if valid_text is None:
        abort(400, "Input search string invalid, only letters and spaces allowed")
    terms = terms.split(",")  # split ids
    terms = [x for x in terms if x]  # remove empty elements
    groups = get_groups_by_filter(page=page, count=per_page, terms=terms, text=text)
    if not groups:
        abort(404, "No groups found for selected filter")
    else:
        return groups