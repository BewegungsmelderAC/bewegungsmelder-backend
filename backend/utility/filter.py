#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from app_config import db


def construct_filter_statement(items: list, col: db.Column):
    condition = False
    if len(items) > 0:
        for i in range(0, len(items)):
            condition = db.or_(condition, col == items[i])
    else:
        condition = True
    return condition
