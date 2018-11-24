# encoding: utf-8

"""
|Header| and |Footer| objects
"""

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

from .blkcntnr import BlockItemContainer
from .shared import Parented, lazyproperty


class _HeaderFooter(Parented):

    __slots__ = '_type'

    def __init__(self, parent, type):
        super(_HeaderFooter, self).__init__(parent)
        self._type = type

    @lazyproperty
    def body(self):
        """

        :return: body of this part
        """
        rel = self._parent.sectPr.get_header_reference_of_type(self._type)
        if rel is None:
            return None
        part = self.part.get_related_part(rel.rId)
        return _HeaderFooterBody(part.element, self)

    @property
    def is_linked_to_previous(self):
        """

        :return: True when is linked otherwise false
        """
        return True if self._parent.sectPr.get_header_reference_of_type(self._type) is None else False


class Header(_HeaderFooter):

    def __init__(self, parent, type):
        super(Header, self).__init__(parent, type)


class Footer(_HeaderFooter):

    def __init__(self, parent, type):
        super(Footer, self).__init__(parent, type)


class _HeaderFooterBody(BlockItemContainer):
    """
    Proxy for ``<w:hdr>``, ``<w:ftr>`` element in this header and footer, having primarily a
    container role.
    """
    def __init__(self, elm, parent):
        super(_HeaderFooterBody, self).__init__(elm, parent)

    def clear_content(self):
        """
        Return this |_HeaderFooterBody| instance after clearing it of all content.
        Section properties for the main document story, if present, are
        preserved.
        """
        return self._element.clear_content()
