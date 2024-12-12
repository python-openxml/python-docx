"""Custom element classes related to hyperlinks (CT_Hyperlink)."""

from __future__ import annotations

from typing import TYPE_CHECKING, List

from docx.oxml.simpletypes import ST_OnOff, ST_String, XsdString
from docx.oxml.text.run import CT_R
from docx.oxml.xmlchemy import (
    BaseOxmlElement,
    OptionalAttribute,
    ZeroOrMore,
)

if TYPE_CHECKING:
    from docx.oxml.text.pagebreak import CT_LastRenderedPageBreak


class CT_Hyperlink(BaseOxmlElement):
    """`<w:hyperlink>` element, containing the text and address for a hyperlink."""

    r_lst: List[CT_R]

    rId: str | None = OptionalAttribute("r:id", XsdString)  # pyright: ignore[reportAssignmentType]
    anchor: str | None = OptionalAttribute(  # pyright: ignore[reportAssignmentType]
        "w:anchor", ST_String
    )
    history: bool = OptionalAttribute(  # pyright: ignore[reportAssignmentType]
        "w:history", ST_OnOff, default=True
    )

    r = ZeroOrMore("w:r")

    @property
    def lastRenderedPageBreaks(self) -> List[CT_LastRenderedPageBreak]:
        """All `w:lastRenderedPageBreak` descendants of this hyperlink."""
        return self.xpath("./w:r/w:lastRenderedPageBreak")

    @property
    def text(self) -> str:  # pyright: ignore[reportIncompatibleMethodOverride]
        """The textual content of this hyperlink.

        `CT_Hyperlink` stores the hyperlink-text as one or more `w:r` children.
        """
        return "".join(r.text for r in self.xpath("w:r"))
