from . import OxmlElement
from .xmlchemy import BaseOxmlElement, ZeroOrMore


class CT_Ftr(BaseOxmlElement):
    """
    ``<w:ftr>``, the container element for the ftr content
    """
    p = ZeroOrMore('w:p', successors=())

    @classmethod
    def new(cls):
        ftr_elm = OxmlElement('w:ftr')
        return ftr_elm
