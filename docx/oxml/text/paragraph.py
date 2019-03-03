# encoding: utf-8

"""
Custom element classes related to paragraphs (CT_P).
"""

from ..ns import qn
from ..xmlchemy import BaseOxmlElement, OxmlElement, ZeroOrMore, ZeroOrOne


class CT_P(BaseOxmlElement):
    """
    ``<w:p>`` element, containing the properties and text for a paragraph.
    """
    pPr = ZeroOrOne('w:pPr')
    r = ZeroOrMore('w:r')

    def _insert_pPr(self, pPr):
        self.insert(0, pPr)
        return pPr

    def add_p_before(self):
        """
        Return a new ``<w:p>`` element inserted directly prior to this one.
        """
        new_p = OxmlElement('w:p')
        self.addprevious(new_p)
        return new_p
    
    def link_comment(self, _id, rangeStart=0, rangeEnd=0):
        rStart = OxmlElement('w:commentRangeStart')
        rStart._id = _id
        rEnd = OxmlElement('w:commentRangeEnd')
        rEnd._id = _id
        if rangeStart == 0 and rangeEnd == 0:
            self.insert(0,rStart)
            self.append(rEnd)
        else:
            self.insert(rangeStart,rStart)
            if rangeEnd == len(self.getchildren() ) - 1 :
                self.append(rEnd)
            else:
                self.insert(rangeEnd+1, rEnd)

    def add_comm(self, author, comment_part, initials, dtime, comment_text, rangeStart, rangeEnd):
        
        comment = comment_part.add_comment(author, initials, dtime)
        comment._add_p(comment_text)
        _r = self.add_r()
        _r.add_comment_reference(comment._id)
        self.link_comment(comment._id, rangeStart= rangeStart, rangeEnd=rangeEnd)

        return comment

    def add_fn(self, text, footnotes_part):
        footnote = footnotes_part.add_footnote()
        footnote._add_p(' '+text)
        _r = self.add_r()
        _r.add_footnote_reference(footnote._id)
        
        return footnote

    def footnote_style(self):
        pPr = self.get_or_add_pPr()
        rstyle = pPr.get_or_add_pStyle()
        rstyle.val = 'FootnoteText'

        return self

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
            if child.tag == qn('w:pPr'):
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
    
    @property
    def comment_id(self):
        _id = self.xpath('./w:commentRangeStart/@w:id')    
        if len(_id) > 1 or len(_id) == 0:
            return None
        else:
            return int(_id[0])
        
    @property
    def footnote_ids(self):
        _id = self.xpath('./w:r/w:footnoteReference/@w:id')
        if  len(_id) == 0 :
            return None
        else:
            return _id 

        
    @style.setter
    def style(self, style):
        pPr = self.get_or_add_pPr()
        pPr.style = style
