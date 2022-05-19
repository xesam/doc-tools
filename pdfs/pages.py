class Pages():
    """页码是从 1 开始的"""
    pass


class RangePages(Pages):
    def __init__(self, first_page: int, last_page: int):
        self._first_page = first_page
        self._last_page = last_page

    def __iter__(self):
        return iter(range(self._first_page, self._last_page + 1))

    def __repr__(self):
        return f'{self._first_page}-{self._last_page}'


class OddPages(Pages):
    def __init__(self, pages_count):
        self._pages_count = pages_count

    def __iter__(self):
        return iter(range(1, self._pages_count + 1, 2))


class EvenPages(Pages):
    def __init__(self, pages_count):
        self._pages_count = pages_count

    def __iter__(self):
        return iter(range(2, self._pages_count + 1, 2))


def parse_fragments(page_count, *fragment_starts):
    fragment_ends = list(fragment_starts)[1:] + [page_count + 1]
    return [RangePages(start, end - 1) for start, end in zip(fragment_starts, fragment_ends)]
