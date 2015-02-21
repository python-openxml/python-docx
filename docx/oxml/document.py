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
    body = ZeroOrOne('w:body')

    @property
    def sectPr_lst(self):
        """
        Return a list containing a reference to each ``<w:sectPr>`` element
        in the document, in the order encountered.
        """
        return self.xpath('.//w:sectPr')


class CT_Body(BaseOxmlElement):
    """
    ``<w:body>``, the container element for the main document story in
    ``document.xml``.
    """
    p = ZeroOrMore('w:p', successors=('w:sectPr',))
    tbl = ZeroOrMore('w:tbl', successors=('w:sectPr',))
    sectPr = ZeroOrOne('w:sectPr', successors=())

    def add_section_break(self):
        """
        Return the current ``<w:sectPr>`` element after adding a clone of it
        in a new ``<w:p>`` element appended to the block content elements.
        Note that the "current" ``<w:sectPr>`` will always be the sentinel
        sectPr in this case since we're always working at the end of the
        block content.
        """
        sentinel_sectPr = self.get_or_add_sectPr()
        cloned_sectPr = sentinel_sectPr.clone()
        p = self.add_p()
        p.set_sectPr(cloned_sectPr)
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
