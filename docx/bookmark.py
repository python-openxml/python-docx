# encoding: utf-8

"""Objects related to bookmarks."""

from __future__ import absolute_import, division, print_function, unicode_literals

from itertools import chain

from docx.compat import Sequence
from docx.oxml.ns import qn
from docx.shared import lazyproperty


class Bookmarks(Sequence):
    """Sequence of |Bookmark| objects.

    This object has mixed semantics. As a sequence, it supports indexed access
    (including slices), `len()`, and iteration (which will perform significantly
    better than repeated indexed access). It also supports some `dict` semantics on
    bookmark name. Specifically, the `in` operator can be used to detect the presence of
    a bookmark by name (e.g. `if name in bookmarks`) and it has a `get()` method that
    allows a bookmark to be retrieved by name.
    """

    def __init__(self, document_part):
        self._document_part = document_part

    def __contains__(self, name):
        """Supports `in` operator to test for presence of bookmark by `name`."""
        for bookmark in self:
            if bookmark.name == name:
                return True
        return False

    def __getitem__(self, idx):
        """Supports indexed and sliced access."""
        bookmark_pairs = self._finder.bookmark_pairs
        if isinstance(idx, slice):
            return [_Bookmark(pair) for pair in bookmark_pairs[idx]]
        return _Bookmark(bookmark_pairs[idx])

    def __iter__(self):
        """Supports iteration."""
        return (_Bookmark(pair) for pair in self._finder.bookmark_pairs)

    def __len__(self):
        return len(self._finder.bookmark_pairs)

    def get(self, name):
        """Get bookmark based on its name.

        Raises `KeyError` if no bookmark with `name` is present in collection.
        """
        for bookmark in self:
            if bookmark.name == name:
                return bookmark
        raise KeyError("Requested bookmark not found.")

    @property
    def next_id(self):
        """Return the next available int bookmark-id, unique in document-wide scope."""
        bookmark_ids = tuple(bookmark.id for bookmark in self)
        if not bookmark_ids:
            return 1
        return max(bookmark_ids) + 1

    @lazyproperty
    def _finder(self):
        """_DocumentBookmarkFinder instance for this document."""
        return _DocumentBookmarkFinder(self._document_part)


class _Bookmark(object):
    """Proxy for a (w:bookmarkStart, w:bookmarkEnd) element pair."""

    def __init__(self, bookmark_pair):
        self._bookmarkStart, self._bookmarkEnd = bookmark_pair

    def close(self, bookmarkEnd):
        """Return self after setting end marker to `bookmarkEnd`.

        Raises ValueError if this bookmark is already closed or if `id` attribute of
        `bookmarkEnd` does not match that of the `bookmarkStart` element.
        """
        if self._bookmarkEnd is not None:
            raise ValueError("bookmark already closed")
        if bookmarkEnd.id != self._bookmarkStart.id:
            raise ValueError("end id does not match start id")
        self._bookmarkEnd = bookmarkEnd
        return self

    @property
    def id(self):
        """Provides access to the bookmark id."""
        return self._bookmarkStart.id

    @property
    def is_closed(self):
        """True if this bookmark has both a start and end element."""
        return self._bookmarkEnd is not None

    @property
    def name(self):
        """Provides access to the bookmark name."""
        return self._bookmarkStart.name


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
            chain(
                *(
                    _PartBookmarkFinder.iter_start_end_pairs(part)
                    for part in self._document_part.iter_story_parts()
                )
            )
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
        for idx, bookmarkStart in self._iter_starts():
            bookmarkEnd = self._matching_end(bookmarkStart, idx)
            # ---skip open pairs---
            if bookmarkEnd is None:
                continue
            # ---skip duplicate names---
            if self._name_already_used(bookmarkStart.name):
                continue
            yield (bookmarkStart, bookmarkEnd)

    @lazyproperty
    def _all_starts_and_ends(self):
        """list of all `w:bookmarkStart` and `w:bookmarkEnd` elements in part.

        Elements appear in document order.
        """
        return self._part.element.xpath("//w:bookmarkStart|//w:bookmarkEnd")

    def _iter_starts(self):
        """Generate (idx, bookmarkStart) elements in story.

        The *idx* value indicates the location of the bookmarkStart element
        among all the bookmarkStart and bookmarkEnd elements in the story.
        """
        for idx, element in enumerate(self._all_starts_and_ends):
            if element.tag == qn("w:bookmarkStart"):
                yield idx, element

    def _matching_end(self, bookmarkStart, idx):
        """Return the `w:bookmarkEnd` element corresponding to *bookmarkStart*.

        Returns None if no `w:bookmarkEnd` with matching id value is found. *idx* is the
        offset of *bookmarkStart* in the sequence of start and end elements in this
        story.
        """
        for element in self._all_starts_and_ends[idx + 1 :]:
            # ---skip bookmark starts---
            if element.tag == qn("w:bookmarkStart"):
                continue
            bookmarkEnd = element
            if bookmarkEnd.id == bookmarkStart.id:
                return bookmarkEnd
        return None

    def _name_already_used(self, name):
        """Return True if bookmark *name* was already encountered, False otherwise."""
        names_so_far = self._names_so_far
        if name in names_so_far:
            return True
        names_so_far.add(name)
        return False

    @lazyproperty
    def _names_so_far(self):
        """set composed to track bookmark names encountered in document traversal."""
        return set()
