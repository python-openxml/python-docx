# encoding: utf-8

"""Objects related to bookmarks."""

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

from itertools import chain

from docx.shared import lazyproperty


class Bookmarks(object):
    """Sequence of |Bookmark| objects."""

    def __init__(self, document_part):
        self._document_part = document_part

    def __len__(self):
        return len(self._finder.bookmark_pairs)

    @lazyproperty
    def _finder(self):
        """_DocumentBookmarkFinder instance for this document."""
        return _DocumentBookmarkFinder(self._document_part)


class _DocumentBookmarkFinder(object):
    """Provides access to bookmark oxml elements in an overall document."""

    def __init__(self, document_part):
        self._document_part = document_part

    @property
    def bookmark_pairs(self):
        """List of (bookmarkStart, bookmarkEnd) element pairs for document.

        The return value is a list of two-tuples (pairs) each containing
        a start and its matching end element.

        All story parts of the document are searched, including the main
        document story, headers, footers, footnotes, and endnotes. The order
        of part searching is not guaranteed, but bookmarks appear in document
        order within a particular part. Only well-formed bookmarks appear.
        Any open bookmarks (start but no end), reversed bookmarks (end before
        start), or duplicate (name same as prior bookmark) bookmarks are
        ignored.
        """
        return list(
            chain(*(
                _PartBookmarkFinder.iter_start_end_pairs(part)
                for part in self._document_part.iter_story_parts()
            ))
        )


class _PartBookmarkFinder(object):
    """Provides access to bookmark oxml elements in a story part."""

    def __init__(self, part):
        self._part = part

    @classmethod
    def iter_start_end_pairs(cls, part):
        """Generate each (bookmarkStart, bookmarkEnd) in *part*."""
        return cls(part)._iter_start_end_pairs()

    def _iter_start_end_pairs(self):
        """Generate each (bookmarkStart, bookmarkEnd) in this part."""
        raise NotImplementedError
