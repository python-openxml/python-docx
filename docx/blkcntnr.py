# encoding: utf-8

"""
Block item container, used by body, cell, header, etc. Block level items are
things like paragraph and table, although there are a few other specialized
ones like structured document tags.
"""

from __future__ import absolute_import, print_function

from .shared import Parented


class BlockItemContainer(Parented):
    """
    Base class for proxy objects that can contain block items, such as _Body,
    _Cell, header, footer, footnote, endnote, comment, and text box objects.
    Provides the shared functionality to add a block item like a paragraph or
    table.
    """
    def __init__(self, element, parent):
        super(BlockItemContainer, self).__init__(parent)
        self._element = element
