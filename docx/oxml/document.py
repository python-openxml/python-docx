# encoding: utf-8

"""
Custom element classes that correspond to the document part, e.g.
<w:document>.
"""

from .xmlchemy import BaseOxmlElement, ZeroOrOne, ZeroOrMore


class CT_Document(BaseOxmlElement):
    """
    ``<w:document>`` element, the root element of a document.xml file.
    """

    body = ZeroOrOne("w:body")

    @property
    def sectPr_lst(self):
        """
        Return a list containing a reference to each ``<w:sectPr>`` element
        in the document, in the order encountered.
        """
        return self.xpath(".//w:sectPr")


class CT_Body(BaseOxmlElement):
    """
    ``<w:body>``, the container element for the main document story in
    ``document.xml``.
    """

    p = ZeroOrMore("w:p", successors=("w:sectPr",))
    tbl = ZeroOrMore("w:tbl", successors=("w:sectPr",))
    sectPr = ZeroOrOne("w:sectPr", successors=())

    def add_section_break(self):
        """Return `w:sectPr` element for new section added at end of document.

        The last `w:sectPr` becomes the second-to-last, with the new `w:sectPr` being an
        exact clone of the previous one, except that all header and footer references
        are removed (and are therefore now "inherited" from the prior section).

        A copy of the previously-last `w:sectPr` will now appear in a new `w:p` at the
        end of the document. The returned `w:sectPr` is the sentinel `w:sectPr` for the
        document (and as implemented, *is* the prior sentinel `w:sectPr` with headers
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
        """
        Remove all content child elements from this <w:body> element. Leave
        the <w:sectPr> element if it is present.
        """
        if self.sectPr is not None:
            content_elms = self[:-1]
        else:
            content_elms = self[:]
        for content_elm in content_elms:
            self.remove(content_elm)
