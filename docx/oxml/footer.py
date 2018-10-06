# encoding: utf-8

"""
Custom element classes that correspond to the footer part, e.g.
<w:hdr>.
"""

from . import OxmlElement
from .xmlchemy import BaseOxmlElement, ZeroOrMore


class CT_Footer(BaseOxmlElement):
    """
    ``<w:ftr>``, the container element for the footer part.
    """

    p = ZeroOrMore('w:p', successors=())

    @classmethod
    def new(cls):
        footer_elm = OxmlElement('w:ftr')
        return footer_elm
