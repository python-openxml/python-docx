# encoding: utf-8

"""
|Document| and closely related objects
"""

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

from .blkcntnr import BlockItemContainer
from .shared import ElementProxy


class Document(ElementProxy):
    """
    WordprocessingML (WML) document.
    """

    __slots__ = ('_part', '__body')

    def __init__(self, element, part):
        super(Document, self).__init__(element)
        self._part = part
        self.__body = None

    @property
    def part(self):
        """
        The |DocumentPart| object of this document.
        """
        return self._part

    @property
    def _body(self):
        """
        The |_Body| instance containing the content for this document.
        """
        if self.__body is None:
            self.__body = _Body(self._element.body, self)
        return self.__body


class _Body(BlockItemContainer):
    """
    Proxy for ``<w:body>`` element in this document, having primarily a
    container role.
    """
    def __init__(self, body_elm, parent):
        super(_Body, self).__init__(body_elm, parent)
        self._body = body_elm
