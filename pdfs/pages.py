from abc import ABCMeta, abstractmethod


class PageCollection(metaclass=ABCMeta):
    """页码是从 1 开始的"""

    @abstractmethod
    def get_collection_name(self):
        pass


class RangePageCollection(PageCollection):
    def __init__(self, first_page: int, last_page: int = -1):
        self._first_page = first_page
        self._last_page = last_page if last_page != -1 else first_page

    def __iter__(self):
        return iter(range(self._first_page, self._last_page + 1))

    def __repr__(self):
        return f'RangePages:{self._first_page}-{self._last_page}'

    def get_collection_name(self):
        if self._first_page == self._last_page:
            return f'{self._first_page}'
        else:
            return f'{self._first_page}-{self._last_page}'


class OddPageCollection(PageCollection):
    def __init__(self, pages_count):
        self._pages_count = pages_count

    def __iter__(self):
        return iter([RangePageCollection(i) for i in range(1, self._pages_count + 1, 2)])

    def get_collection_name(self):
        return f'奇数页'


class EvenPageCollection(PageCollection):
    def __init__(self, pages_count):
        self._pages_count = pages_count

    def __iter__(self):
        return iter([RangePageCollection(i) for i in range(2, self._pages_count + 1, 2)])

    def get_collection_name(self):
        return f'偶数页'


class FragmentPage(PageCollection):
    def __init__(self, pages_count, fragment_starts):
        self._pages_count = pages_count
        self._fragment_starts = fragment_starts

    def __iter__(self):
        fragment_ends = list(self._fragment_starts)[1:] + [self._pages_count + 1]
        return iter([RangePageCollection(start, end - 1) for start, end in zip(self._fragment_starts, fragment_ends)])

    def get_collection_name(self):
        return f'分割集'

#
# def parse_fragments(page_count, *fragment_starts):
#     fragment_ends = list(fragment_starts)[1:] + [page_count + 1]
#     return [RangePageCollection(start, end - 1) for start, end in zip(fragment_starts, fragment_ends)]
