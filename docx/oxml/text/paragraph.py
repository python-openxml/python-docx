# encoding: utf-8

"""
Custom element classes related to paragraphs (CT_P).
"""

from docx.oxml.ns import qn
from docx.oxml.xmlchemy import BaseOxmlElement, OxmlElement, ZeroOrMore, ZeroOrOne


class CT_P(BaseOxmlElement):
    """
    ``<w:p>`` element, containing the properties and text for a paragraph.
    """

    bookmarkEnd = ZeroOrMore("w:bookmarkEnd")
    bookmarkStart = ZeroOrMore("w:bookmarkStart")
    pPr = ZeroOrOne("w:pPr")
    r = ZeroOrMore("w:r")

    def add_bookmarkStart(self, name, bookmark_id):
        """Return `w:bookmarkStart` element added at the end of this header or footer.

        The newly added `w:bookmarkStart` element is identified by both `name` and
        `bookmark_id`. It is the caller's responsibility to determine that both `name`
        and `bookmark_id` are unique, document-wide.
        """
        bookmarkStart = self._add_bookmarkStart()
        bookmarkStart.name = name
        bookmarkStart.id = bookmark_id
        return bookmarkStart

    def _insert_pPr(self, pPr):
        self.insert(0, pPr)
        return pPr

    def add_p_before(self):
        """
        Return a new ``<w:p>`` element inserted directly prior to this one.
        """
        new_p = OxmlElement("w:p")
        self.addprevious(new_p)
        return new_p

    @property
    def alignment(self):
        """
        The value of the ``<w:jc>`` grandchild element or |None| if not
        present.
        """
        pPr = self.pPr
        if pPr is None:
            return None
        return pPr.jc_val

    @alignment.setter
    def alignment(self, value):
        pPr = self.get_or_add_pPr()
        pPr.jc_val = value

    def clear_content(self):
        """
        Remove all child elements, except the ``<w:pPr>`` element if present.
        """
        for child in self[:]:
            if child.tag == qn("w:pPr"):
                continue
            self.remove(child)

    def set_sectPr(self, sectPr):
        """
        Unconditionally replace or add *sectPr* as a grandchild in the
        correct sequence.
        """
        pPr = self.get_or_add_pPr()
        pPr._remove_sectPr()
        pPr._insert_sectPr(sectPr)

    @property
    def style(self):
        """
        String contained in w:val attribute of ./w:pPr/w:pStyle grandchild,
        or |None| if not present.
        """
        pPr = self.pPr
        if pPr is None:
            return None
        return pPr.style

    @style.setter
    def style(self, style):
        pPr = self.get_or_add_pPr()
        pPr.style = style
