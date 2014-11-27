# encoding: utf-8

"""
The |ListParagraph| object and related proxy classes.
"""

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

import random
from .text import Paragraph


class ListParagraph(object):
    """
    Proxy object for controlling a set of ``<w:p>`` grouped together in a list.
    """
    def __init__(self, parent, numId=0, style=None, level=0):
        self._parent = parent
        self.numId = numId
        self.level = level
        self.style = style

    def add_item(self, text=None, style=None):
        """
        Add a paragraph item to the current list, having text set to *text* and
        a paragraph style *style*
        """
        item = self._parent.add_paragraph(text, style=style)
        item.level = self.level
        item.numId = self.numId
        return item

    def add_list(self, style=None):
        """
        Add a list indented one level below the current one, having a paragraph
        style *style*. Note that the document will only be altered once the
        first item has been added to the list.
        """
        return ListParagraph(
            self._parent,
            numId=self._parent.generate_numId(),
            style=style if style is not None else self.style,
            level=self.level+1,
        )

    @property
    def items(self):
        """
        Sequence of |Paragraph| instances corresponding to the item elements
        in this list paragraph.
        """
        return [paragraph for paragraph in self._parent.paragraphs
                if paragraph.numId == self.numId]
