# encoding: utf-8

"""Objects related to bookmarks."""

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)


class Bookmarks(object):
    """Sequence of |Bookmark| objects."""

    def __init__(self, document_part):
        self._document_part = document_part
