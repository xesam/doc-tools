import re

from app.pages import RangePageCollection

RE_SPLITS = re.compile(',|，|\s+')


def _clean_paginations(paginations: str):
    return [pagination for pagination in RE_SPLITS.split(paginations) if len(pagination.strip()) != 0]


def _parse_page(pagination: str):
    pages = [int(i) for i in pagination.split('-')]
    pages.sort()
    return RangePageCollection(pages[0], pages[-1])


def parse_pages(paginations: str):
    return [_parse_page(i) for i in _clean_paginations(paginations)]


def parse_starts(paginations: str):
    starts = [int(i) for i in _clean_paginations(paginations)]
    return sorted(starts)
