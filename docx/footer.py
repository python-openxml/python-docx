# encoding: utf-8

"""
|Footer| and closely related objects
"""

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

from docx.blkcntnr import BlockItemContainer


class Footer(BlockItemContainer):
    """
    WordprocessingML (WML) footer. Not intended to be constructed directly.
    """

    __slots__ = ('_part', '__body')

    def __init__(self, element, part):
        super(Footer, self).__init__(element, part)
        self._part = part
        self.__body = None

    @property
    def core_properties(self):
        """
        A |CoreProperties| object providing read/write access to the core
        properties of this footer.
        """
        return self._part.core_properties

    @property
    def styles(self):
        """
        A |Styles| object providing access to the styles in this footer.
        """
        return self._part.styles

    @property
    def inline_shapes(self):
        """
        An |InlineShapes| object providing access to the inline shapes in
        this footer. An inline shape is a graphical object, such as
        a picture, contained in a run of text and behaving like a character
        glyph, being flowed like other text in a paragraph.
        """
        return self._part.inline_shapes
