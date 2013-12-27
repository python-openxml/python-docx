# encoding: utf-8

"""
Custom element classes that correspond to the document part, e.g.
<w:document>.
"""

from docx.oxml.shared import OxmlBaseElement, qn
from docx.oxml.table import CT_Tbl
from docx.oxml.text import CT_P


class CT_Document(OxmlBaseElement):
    """
    ``<w:document>`` element, the root element of a document.xml file.
    """
    @property
    def body(self):
        return self.find(qn('w:body'))


class CT_Body(OxmlBaseElement):
    """
    ``<w:body>``, the container element for the main document story in
    ``document.xml``.
    """
    def add_p(self):
        """
        Return a new <w:p> element that has been added at the end of any
        existing body content.
        """
        p = CT_P.new()
        return self._append_blocklevelelt(p)

    def add_tbl(self):
        """
        Return a new <w:tbl> element that has been added at the end of any
        existing body content.
        """
        tbl = CT_Tbl.new()
        return self._append_blocklevelelt(tbl)

    def clear_content(self):
        """
        Remove all content child elements from this <w:body> element. Leave
        the <w:sectPr> element if it is present.
        """
        if self._sentinel_sectPr is not None:
            content_elms = self[:-1]
        else:
            content_elms = self[:]
        for content_elm in content_elms:
            self.remove(content_elm)

    @property
    def p_lst(self):
        """
        List of <w:p> child elements.
        """
        return self.findall(qn('w:p'))

    @property
    def tbl_lst(self):
        """
        List of <w:tbl> child elements.
        """
        return self.findall(qn('w:tbl'))

    def _append_blocklevelelt(self, block_level_elt):
        """
        Return *block_level_elt* after appending it to end of
        EG_BlockLevelElts sequence.
        """
        sentinel_sectPr = self._sentinel_sectPr
        if sentinel_sectPr is not None:
            sentinel_sectPr.addprevious(block_level_elt)
        else:
            self.append(block_level_elt)
        return block_level_elt

    @property
    def _sentinel_sectPr(self):
        """
        Return ``<w:sectPr>`` element appearing as last child, or None if not
        found. Note that the ``<w:sectPr>`` element can also occur earlier in
        the body; here we're only interested in one occuring as the last
        child.
        """
        if len(self) == 0:
            sentinel_sectPr = None
        elif self[-1].tag != qn('w:sectPr'):
            sentinel_sectPr = None
        else:
            sentinel_sectPr = self[-1]
        return sentinel_sectPr
