import re
from pdfs.pages import RangePageCollection


def parse_page(pagination: str):
    pages = [int(i) for i in pagination.split('-')]
    return RangePageCollection(pages[0], pages[-1])


def parse_pages(paginations: str):
    pages = [parse_page(i) for i in paginations.split(',')]
    return pages


def parse_starts(paginations: str):
    return [int(i) for i in paginations.split(',')]
