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

    @property
    def contains_page_break(self) -> bool:
        """True when the text of this hyperlink is broken across page boundaries.

        This is not uncommon and can happen for example when the hyperlink text is
        multiple words and occurs in the last line of a page. Theoretically, a hyperlink
        can contain more than one page break but that would be extremely uncommon in
        practice. Still, this value should be understood to mean that "one-or-more"
        rendered page breaks are present.
        """
        return bool(self._hyperlink.lastRenderedPageBreaks)
