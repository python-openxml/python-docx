"""Custom element classes for native Word footnotes."""

from __future__ import annotations

from typing import TYPE_CHECKING, Callable, cast

from docx.oxml.ns import nsdecls
from docx.oxml.parser import parse_xml
from docx.oxml.simpletypes import ST_DecimalNumber, ST_String
from docx.oxml.xmlchemy import BaseOxmlElement, OptionalAttribute, RequiredAttribute, ZeroOrMore

if TYPE_CHECKING:
    from docx.oxml.table import CT_Tbl
    from docx.oxml.text.paragraph import CT_P


class CT_Footnotes(BaseOxmlElement):
    """Root of a footnotes part, including its special separator entries."""

    footnote_lst: list[CT_Footnote]
    footnote = ZeroOrMore("w:footnote")


class CT_Footnote(BaseOxmlElement):
    """A footnote containing paragraphs and tables."""

    id: int = RequiredAttribute("w:id", ST_DecimalNumber)  # pyright: ignore[reportAssignmentType]
    type: str | None = OptionalAttribute("w:type", ST_String)  # pyright: ignore[reportAssignmentType]
    p = ZeroOrMore("w:p", successors=())
    tbl = ZeroOrMore("w:tbl", successors=())
    add_p: Callable[[], CT_P]
    p_lst: list[CT_P]
    tbl_lst: list[CT_Tbl]
    _insert_tbl: Callable[[CT_Tbl], CT_Tbl]

    @property
    def inner_content_elements(self) -> list[CT_P | CT_Tbl]:
        """Paragraphs and tables in document order."""
        return self.xpath("./w:p | ./w:tbl")

    @classmethod
    def new(cls, footnote_id: int) -> CT_Footnote:
        """A detached note with its native number marker and initial space."""
        return cast(
            "CT_Footnote",
            parse_xml(
                f'<w:footnote {nsdecls("w")} w:id="{footnote_id}">'
                '<w:p><w:pPr><w:pStyle w:val="FootnoteText"/></w:pPr>'
                '<w:r><w:rPr><w:rStyle w:val="FootnoteReference"/></w:rPr>'
                '<w:footnoteRef/></w:r><w:r><w:t xml:space="preserve"> </w:t></w:r>'
                "</w:p></w:footnote>"
            ),
        )
