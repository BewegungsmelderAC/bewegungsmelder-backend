#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from app_config import db
from html import unescape

def construct_filter_statement(items: list, col: db.Column):
    condition = False
    if len(items) > 0:
        for i in range(0, len(items)):
            condition = db.or_(condition, col == items[i])
    else:
        condition = True
    return condition


def unescape_db_to_plain(text: str) -> str:
    return unescape(text).replace("\\","")