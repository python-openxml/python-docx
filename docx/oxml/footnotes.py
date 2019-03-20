"""
Custom element classes related to the footnotes part
"""


from . import OxmlElement
from .simpletypes import ST_DecimalNumber, ST_String
from ..text.paragraph import Paragraph
from ..text.run import Run
from ..opc.constants import NAMESPACE
from .xmlchemy import (
    BaseOxmlElement, OneAndOnlyOne, RequiredAttribute, ZeroOrMore, ZeroOrOne
)


class CT_Footnotes(BaseOxmlElement):
    """
    A ``<w:footnotes>`` element, a container for Footnotes properties 
    """

    footnote = ZeroOrMore ('w:footnote', successors=('w:footnotes',))

    @property
    def _next_id(self):
        ids = self.xpath('./w:footnote/@w:id')

        return int(ids[-1]) + 1
    
    def add_footnote(self):
        _next_id = self._next_id
        footnote = CT_Footnote.new(_next_id)
        footnote = self._insert_footnote(footnote)
        return footnote

    def get_footnote_by_id(self, _id):
        namesapce = NAMESPACE().WML_MAIN
        for fn in self.findall('.//w:footnote', {'w':namesapce}):
            if fn._id == _id:
                return fn
        return None

class CT_Footnote(BaseOxmlElement):
    """
    A ``<w:footnote>`` element, a container for Footnote properties 
    """
    _id = RequiredAttribute('w:id', ST_DecimalNumber)
    p = ZeroOrOne('w:p', successors=('w:footnote',))

    @classmethod
    def new(cls, _id):
        footnote = OxmlElement('w:footnote')
        footnote._id = _id
        
        return footnote
    
    def _add_p(self, text):
        _p = OxmlElement('w:p')
        _p.footnote_style()
        
        _r = _p.add_r()
        _r.footnote_style()
        _r = _p.add_r()
        _r.add_footnoteRef()
        
        run = Run(_r, self)
        run.text = text
        
        self._insert_p(_p)
        return _p
    
    @property
    def paragraph(self):
        return Paragraph(self.p, self)
    
class CT_FNR(BaseOxmlElement):
    _id = RequiredAttribute('w:id', ST_DecimalNumber)

    @classmethod
    def new (cls, _id):
        footnoteReference = OxmlElement('w:footnoteReference')
        footnoteReference._id = _id
        return footnoteReference

class CT_FootnoteRef (BaseOxmlElement):

    @classmethod
    def new (cls):
        ref = OxmlElement('w:footnoteRef')
        return ref