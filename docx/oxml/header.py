# encoding: utf-8

"""
Custom element classes that correspond to the header part, e.g.
<w:hdr>.
"""

from . import OxmlElement
from .xmlchemy import BaseOxmlElement, ZeroOrMore


class CT_Header(BaseOxmlElement):
    """
    ``<w:hdr>``, the container element for the header part.
    """

    @classmethod
    def new(cls):
        header_elm = OxmlElement('w:hdr')
        return header_elm
