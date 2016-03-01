from . import OxmlElement
from .xmlchemy import BaseOxmlElement, ZeroOrMore


class CT_Hdr(BaseOxmlElement):
    """
    ``<w:hdr>``, the container element for the header content
    """
    p = ZeroOrMore('w:p', successors=())

    @classmethod
    def new(cls):
        header_elm = OxmlElement('w:hdr')
        return header_elm


class CT_Ftr(BaseOxmlElement):
    """
    ``<w:hdr>``, the container element for the header content
    """
    p = ZeroOrMore('w:p', successors=())

    @classmethod
    def new(cls):
        header_elm = OxmlElement('w:ftr')
        return header_elm
