#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from backend.adapter.wordpress.location import Location
from backend.adapter.wordpress.group import Group
from backend.adapter.wordpress.event import Event
from backend.utility import construct_filter_statement, unescape_db_to_plain


def group_to_full_dict(group: Group) -> dict:
    return {"metadata": group.get_all_metadata(),  # this also populates the fields read from the metadata table
            "name": unescape_db_to_plain(group.name),
            "id": group.id,
            "description": unescape_db_to_plain(group.description),
            "slug": group.slug,
            "created": group.date_created,
            "contact_email": group.contact_email,
            "contact_name": group.contact_name,
            "meetup_description": group.meetup_description,
            "website": group.website,
            "telephone": group.telephone,
            "avatar": group.get_avatar(),
            "cover": group.cover_url,  # don't forget, there is no real cover image yet
            "terms": [{"name": x.name, "slug": x.slug} for x in group.terms]}


def group_to_compact_dict(group: Group) -> dict:
    return {"name": unescape_db_to_plain(group.name), "slug": group.slug, "id": group.id}


def get_group_by_id(group_id: int) -> dict:
    group = Group.query.get(group_id)
    if group is None:
        return {}
    else:
        return group_to_full_dict(group)


def get_group_by_slug(slug: str) -> dict:
    group = Group.query.filter(Group.slug == slug).one_or_none()
    if group is None:
        return {}
    else:
        return group_to_full_dict(group)


def get_groups_by_filter(page: int, count: int, terms: list, text: str) -> list:
    terms_condition = construct_filter_statement(terms, Group.terms_slugs)
    text_condition = Group.name.like("%{}%".format(text)) if text != "" else True
    groups = Group.query.filter(terms_condition, text_condition)\
        .order_by(Group.name.asc()).paginate(page=page, per_page=count)
    groups_dict = []
    for group in groups.items:
        groups_dict.append(group_to_compact_dict(group))
    return groups_dict
