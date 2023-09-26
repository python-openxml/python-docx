"""Custom element classes related to paragraphs (CT_P)."""

from __future__ import annotations

from typing import TYPE_CHECKING, Callable, List

from docx.oxml.xmlchemy import BaseOxmlElement, OxmlElement, ZeroOrMore, ZeroOrOne

if TYPE_CHECKING:
    from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
    from docx.oxml.text.parfmt import CT_PPr
    from docx.oxml.text.run import CT_R


class CT_P(BaseOxmlElement):
    """`<w:p>` element, containing the properties and text for a paragraph."""

    get_or_add_pPr: Callable[[], CT_PPr]
    r_lst: List[CT_R]

    pPr: CT_PPr | None = ZeroOrOne("w:pPr")  # pyright: ignore[reportGeneralTypeIssues]
    r = ZeroOrMore("w:r")

    def add_p_before(self) -> CT_P:
        """Return a new `<w:p>` element inserted directly prior to this one."""
        new_p = OxmlElement("w:p")
        self.addprevious(new_p)
        return new_p

    @property
    def alignment(self) -> WD_PARAGRAPH_ALIGNMENT | None:
        """The value of the `<w:jc>` grandchild element or |None| if not present."""
        pPr = self.pPr
        if pPr is None:
            return None
        return pPr.jc_val

    @alignment.setter
    def alignment(self, value: WD_PARAGRAPH_ALIGNMENT):
        pPr = self.get_or_add_pPr()
        pPr.jc_val = value

    def clear_content(self):
        """Remove all child elements, except the `<w:pPr>` element if present."""
        for child in self.xpath("./*[not(self::w:pPr)]"):
            self.remove(child)

    def set_sectPr(self, sectPr):
        """Unconditionally replace or add `sectPr` as grandchild in correct sequence."""
        pPr = self.get_or_add_pPr()
        pPr._remove_sectPr()
        pPr._insert_sectPr(sectPr)

    @property
    def style(self) -> str | None:
        """String contained in `w:val` attribute of `./w:pPr/w:pStyle` grandchild.

        |None| if not present.
        """
        pPr = self.pPr
        if pPr is None:
            return None
        return pPr.style

    @style.setter
    def style(self, style):
        pPr = self.get_or_add_pPr()
        pPr.style = style

    def _insert_pPr(self, pPr: CT_PPr) -> CT_PPr:
        self.insert(0, pPr)
        return pPr
