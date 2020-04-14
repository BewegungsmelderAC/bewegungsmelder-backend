#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import abort
from backend.service.group_service import get_group, get_groups_by_filter


def get_single_group(group_id: int = None):
    if group_id is None:
        abort(400, "Invalid group id")
    else:
        group = get_group(group_id)
        if group == {}:
            abort(404, "Group not found")
        else:
            return group


def get_filtered_groups(page: int, per_page: int):
    groups = get_groups_by_filter(page=page, count=per_page)
    if not groups:
        abort(404, "No groups found for selected filter")
    else:
        return groups