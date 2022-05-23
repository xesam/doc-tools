import re

from pdfs.pages import RangePageCollection

RE_SPLITS = re.compile(',|，|\s+')


def clean_paginations(paginations: str):
    return [pagination for pagination in RE_SPLITS.split(paginations) if len(pagination.strip()) != 0]


def parse_page(pagination: str):
    pages = [int(i) for i in pagination.split('-')]
    return RangePageCollection(pages[0], pages[-1])


def parse_pages(paginations: str):
    pages = [parse_page(i) for i in clean_paginations(paginations)]
    return pages


def parse_starts(paginations: str):
    return [int(i) for i in clean_paginations(paginations)]
