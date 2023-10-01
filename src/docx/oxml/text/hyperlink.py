"""Custom element classes related to hyperlinks (CT_Hyperlink)."""

from __future__ import annotations

from docx.oxml.xmlchemy import BaseOxmlElement


class CT_Hyperlink(BaseOxmlElement):
    """`<w:hyperlink>` element, containing the text and address for a hyperlink."""
