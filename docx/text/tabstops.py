# encoding: utf-8

"""
Tabstop-related proxy types.
"""

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

from ..shared import ElementProxy


class TabStops(ElementProxy):
    """
    A sequence providing access to the tab stops of a paragraph or paragraph
    style. Supports iteration, indexed access, del, and len(). It is accesed
    using the `tab_stops` property of ParagraphFormat; it is not intended to
    be constructed directly.
    """

    __slots__ = ('_pPr')

    def __init__(self, element):
        super(TabStops, self).__init__(element, None)
        self._pPr = element


class TabStop(ElementProxy):
    """
    An individual tab stop applying to a paragraph or style. Each of these is
    a member of a set held in a |TabStops| object.
    """

    __slots__ = ('_tab')

    def __init__(self, element):
        super(TabStop, self).__init__(element, None)
        self._tab = element
