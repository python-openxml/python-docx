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

    def __getitem__(self, idx):
        """
        Enables list-style access by index.
        """
        tabs = self._pPr.tabs
        if tabs is None:
            raise IndexError('TabStops object is empty')
        tab = tabs.tab_lst[idx]
        return TabStop(tab)

    def __iter__(self):
        """
        Generate a TabStop object for each of the w:tab elements, in XML
        document order.
        """
        tabs = self._pPr.tabs
        if tabs is not None:
            for tab in tabs.tab_lst:
                yield TabStop(tab)

    def __len__(self):
        tabs = self._pPr.tabs
        if tabs is None:
            return 0
        return len(tabs.tab_lst)


class TabStop(ElementProxy):
    """
    An individual tab stop applying to a paragraph or style. Each of these is
    a member of a set held in a |TabStops| object.
    """

    __slots__ = ('_tab')

    def __init__(self, element):
        super(TabStop, self).__init__(element, None)
        self._tab = element

    @property
    def alignment(self):
        """
        A member of :ref:`WdTabAlignment` specifying the alignment setting
        for this tab stop.
        """
        return self._tab.val

    @property
    def leader(self):
        """
        A member of :ref:`WdTabLeader` specifying a repeating character used
        as a "leader", filling in the space spanned by this tab. Assigning
        |None| produces the same result as assigning `WD_TAB_LEADER.SPACES`.
        """
        return self._tab.leader

    @property
    def position(self):
        """
        The distance (in EMU) of this tab stop from the inside edge of the
        paragraph. May be positive or negative.
        """
        return self._tab.pos

    @position.setter
    def position(self, value):
        tab = self._tab
        tabs = tab.getparent()
        self._tab = tabs.insert_tab_in_order(value, tab.val, tab.leader)
        tabs.remove(tab)
