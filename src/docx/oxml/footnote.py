"""Custom element classes related to footnote (CT_FtnEnd, CT_Footnotes)."""

from __future__ import annotations

from typing import TYPE_CHECKING, Callable, List

from docx.oxml.ns import qn
from docx.oxml.parser import OxmlElement
from docx.oxml.simpletypes import ST_DecimalNumber
from docx.oxml.xmlchemy import BaseOxmlElement, OneOrMore, RequiredAttribute, ZeroOrMore

if TYPE_CHECKING:
    from docx.oxml.text.paragraph import CT_P


class CT_FtnEnd(BaseOxmlElement):
    """``<w:footnote>`` element, containing the properties for a specific footnote"""

    id = RequiredAttribute("w:id", ST_DecimalNumber)
    p = ZeroOrMore("w:p")

    def add_footnote_before(self, footnote_reference_id: int) -> CT_FtnEnd:
        """Create a ``<w:footnote>`` element with `footnote_reference_id`
        and insert it before the current element."""
        new_footnote = OxmlElement("w:footnote")
        new_footnote.id = footnote_reference_id
        self.addprevious(new_footnote)
        return new_footnote

    @property
    def paragraphs(self) -> List[CT_P]:
        """Returns a list of paragraphs |CT_P|."""

        paragraphs = []
        for child in self:
            if child.tag == qn("w:p"):
                paragraphs.append(child)
        return paragraphs


class CT_Footnotes(BaseOxmlElement):
    """``<w:footnotes>`` element, containing a sequence of footnote (w:footnote) elements"""

    add_footnote_sequence: Callable[[], CT_FtnEnd]

    footnote_sequence = OneOrMore("w:footnote")

    def add_footnote(self, footnote_reference_id: int) -> CT_FtnEnd:
        """Create a ``<w:footnote>`` element with `footnote_reference_id`."""
        new_f = self.add_footnote_sequence()
        new_f.id = footnote_reference_id
        return new_f

    def get_by_id(self, id: int) -> CT_FtnEnd | None:
        found = self.xpath(f'w:footnote[@w:id="{id}"]')
        if not found:
            return None
        return found[0]
