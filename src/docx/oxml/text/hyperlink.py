"""Custom element classes related to hyperlinks (CT_Hyperlink)."""

from __future__ import annotations

from typing import List

from docx.oxml.simpletypes import ST_OnOff, XsdString
from docx.oxml.text.run import CT_R
from docx.oxml.xmlchemy import (
    BaseOxmlElement,
    OptionalAttribute,
    RequiredAttribute,
    ZeroOrMore,
)


class CT_Hyperlink(BaseOxmlElement):
    """`<w:hyperlink>` element, containing the text and address for a hyperlink."""

    r_lst: List[CT_R]

    rId = RequiredAttribute("r:id", XsdString)
    history = OptionalAttribute("w:history", ST_OnOff, default=True)

    r = ZeroOrMore("w:r")
