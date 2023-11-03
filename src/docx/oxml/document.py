"""Custom element classes that correspond to the document part, e.g. <w:document>."""

from __future__ import annotations

from typing import TYPE_CHECKING, Callable, List

from docx.oxml.section import CT_SectPr
from docx.oxml.xmlchemy import BaseOxmlElement, ZeroOrMore, ZeroOrOne

if TYPE_CHECKING:
    from docx.oxml.table import CT_Tbl
    from docx.oxml.text.paragraph import CT_P


class CT_Document(BaseOxmlElement):
    """``<w:document>`` element, the root element of a document.xml file."""

    body = ZeroOrOne("w:body")

    @property
    def sectPr_lst(self) -> List[CT_SectPr]:
        """All `w:sectPr` elements directly accessible from document element.

        Note this does not include a `sectPr` child in a paragraphs wrapped in
        revision marks or other intervening layer, perhaps `w:sdt` or customXml
        elements.

        `w:sectPr` elements appear in document order. The last one is always
        `w:body/w:sectPr`, all preceding are `w:p/w:pPr/w:sectPr`.
        """
        xpath = "./w:body/w:p/w:pPr/w:sectPr | ./w:body/w:sectPr"
        return self.xpath(xpath)


class CT_Body(BaseOxmlElement):
    """`w:body`, the container element for the main document story in `document.xml`."""

    add_p: Callable[[], CT_P]
    get_or_add_sectPr: Callable[[], CT_SectPr]
    p_lst: List[CT_P]
    tbl_lst: List[CT_Tbl]

    _insert_tbl: Callable[[CT_Tbl], CT_Tbl]

    p = ZeroOrMore("w:p", successors=("w:sectPr",))
    tbl = ZeroOrMore("w:tbl", successors=("w:sectPr",))
    sectPr: CT_SectPr | None = ZeroOrOne(  # pyright: ignore[reportGeneralTypeIssues]
        "w:sectPr", successors=()
    )

    def add_section_break(self) -> CT_SectPr:
        """Return `w:sectPr` element for new section added at end of document.

        The last `w:sectPr` becomes the second-to-last, with the new `w:sectPr` being an
        exact clone of the previous one, except that all header and footer references
        are removed (and are therefore now "inherited" from the prior section).

        A copy of the previously-last `w:sectPr` will now appear in a new `w:p` at the
        end of the document. The returned `w:sectPr` is the sentinel `w:sectPr` for the
        document (and as implemented, `is` the prior sentinel `w:sectPr` with headers
        and footers removed).
        """
        # ---get the sectPr at file-end, which controls last section (sections[-1])---
        sentinel_sectPr = self.get_or_add_sectPr()
        # ---add exact copy to new `w:p` element; that is now second-to last section---
        self.add_p().set_sectPr(sentinel_sectPr.clone())
        # ---remove any header or footer references from "new" last section---
        for hdrftr_ref in sentinel_sectPr.xpath("w:headerReference|w:footerReference"):
            sentinel_sectPr.remove(hdrftr_ref)
        # ---the sentinel `w:sectPr` now controls the new last section---
        return sentinel_sectPr

    def clear_content(self):
        """Remove all content child elements from this <w:body> element.

        Leave the <w:sectPr> element if it is present.
        """
        for content_elm in self.xpath("./*[not(self::w:sectPr)]"):
            self.remove(content_elm)

    @property
    def inner_content_elements(self) -> List[CT_P | CT_Tbl]:
        """Generate all `w:p` and `w:tbl` elements in this document-body.

        Elements appear in document order. Elements shaded by nesting in a `w:ins` or
        other "wrapper" element will not be included.
        """
        return self.xpath("./w:p | ./w:tbl")
