#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from backend.adapter.wordpress.term import Term


def term_to_dict(term: Term):
    return {"name": term.name,
            "slug": term.slug}


def get_terms_by_type(type: str, text: str):
    text_condition = Term.name.like("%{}%".format(text)) if text != "" else True
    terms = Term.query.filter(Term.type == type, text_condition).all()
    terms_dicts = []
    for term in terms:
        terms_dicts.append(term_to_dict(term))
    return terms_dicts

