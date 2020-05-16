#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from backend.adapter.wordpress.term import Term


def term_to_dict(term: Term):
    return {"name": term.name,
            "slug": term.slug}


def get_terms_by_type(type: str, text: str, page: int, per_page:int):
    text_condition = Term.name.like("%{}%".format(text)) if text != "" else True
    terms = Term.query.filter(Term.type == type, text_condition).order_by(Term.name.asc()).paginate(page=page, per_page=per_page)
    terms_dicts = []
    for term in terms.items:
        terms_dicts.append(term_to_dict(term))
    return terms_dicts

