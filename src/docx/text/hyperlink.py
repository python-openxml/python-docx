"""Hyperlink-related proxy objects for python-docx, Hyperlink in particular.

A hyperlink occurs in a paragraph, at the same level as a Run, and a hyperlink itself
contains runs, which is where the visible text of the hyperlink is stored. So it's kind
of in-between, less than a paragraph and more than a run. So it gets its own module.
"""

from __future__ import annotations

from docx import types as t
from docx.oxml.text.hyperlink import CT_Hyperlink
from docx.shared import Parented


class Hyperlink(Parented):
    """Proxy object wrapping a `<w:hyperlink>` element.

    A hyperlink occurs as a child of a paragraph, at the same level as a Run. A
    hyperlink itself contains runs, which is where the visible text of the hyperlink is
    stored.
    """

    def __init__(self, hyperlink: CT_Hyperlink, parent: t.StoryChild):
        super().__init__(parent)
        self._parent = parent
        self._hyperlink = self._element = hyperlink

    @property
    def address(self) -> str:
        """The "URL" of the hyperlink (but not necessarily a web link).

        While commonly a web link like "https://google.com" the hyperlink address can
        take a variety of forms including "internal links" to bookmarked locations
        within the document.
        """
        return self._parent.part.rels[self._hyperlink.rId].target_ref
