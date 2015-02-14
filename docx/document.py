# encoding: utf-8

"""
|Document| and closely related objects
"""

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

from .shared import ElementProxy


class Document(ElementProxy):
    """
    WordprocessingML (WML) document.
    """

    __slots__ = ('_part',)

    def __init__(self, element, part):
        super(Document, self).__init__(element)
        self._part = part
