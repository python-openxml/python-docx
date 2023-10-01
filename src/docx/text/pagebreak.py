"""Proxy objects related to rendered page-breaks."""

from __future__ import annotations

from docx import types as t
from docx.oxml.text.pagebreak import CT_LastRenderedPageBreak
from docx.shared import Parented


class RenderedPageBreak(Parented):
    """A page-break inserted by Word during page-layout for print or display purposes.

    This usually does not correspond to a "hard" page-break inserted by the document
    author, rather just that Word ran out of room on one page and needed to start
    another. The position of these can change depending on the printer and page-size, as
    well as margins, etc. They also will change in response to edits, but not until Word
    loads and saves the document.

    Note these are never inserted by `python-docx` because it has no rendering function.
    These are generally only useful for text-extraction of existing documents when
    `python-docx` is being used solely as a document "reader".
    """

    def __init__(
        self, lastRenderedPageBreak: CT_LastRenderedPageBreak, parent: t.StoryChild
    ):
        super().__init__(parent)
        self._element = lastRenderedPageBreak
        self._lastRenderedPageBreak = lastRenderedPageBreak
