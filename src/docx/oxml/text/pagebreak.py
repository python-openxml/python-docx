"""Custom element class for rendered page-break (CT_LastRenderedPageBreak)."""

from __future__ import annotations

from docx.oxml.xmlchemy import BaseOxmlElement


class CT_LastRenderedPageBreak(BaseOxmlElement):
    """`<w:lastRenderedPageBreak>` element, indicating page break inserted by renderer.

    A rendered page-break is one inserted by the renderer when it runs out of room on a
    page. It is an empty element (no attrs or children) and is a child of CT_R, peer to
    CT_Text.

    NOTE: this complex-type name does not exist in the schema, where
    `w:lastRenderedPageBreak` maps to `CT_Empty`. This name was added to give it
    distinguished behavior. CT_Empty is used for many elements.
    """
