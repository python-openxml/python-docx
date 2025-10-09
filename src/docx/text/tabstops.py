"""Tabstop-related proxy types."""

from docx.enum.text import WD_TAB_ALIGNMENT, WD_TAB_LEADER
from docx.shared import ElementProxy


class TabStops(ElementProxy):
    """A sequence of |TabStop| objects providing access to the tab stops of a paragraph
    or paragraph style.

    Supports iteration, indexed access, del, and len(). It is accesed using the
    :attr:`~.ParagraphFormat.tab_stops` property of ParagraphFormat; it is not intended
    to be constructed directly.
    """

    def __init__(self, element):
        super(TabStops, self).__init__(element, None)
        self._pPr = element

    def __delitem__(self, idx):
        """Remove the tab at offset `idx` in this sequence."""
        tabs = self._pPr.tabs
        try:
            tabs.remove(tabs[idx])
        except (AttributeError, IndexError):
            raise IndexError("tab index out of range")

        if len(tabs) == 0:
            self._pPr.remove(tabs)

    def __getitem__(self, idx):
        """Enables list-style access by index."""
        tabs = self._pPr.tabs
        if tabs is None:
            raise IndexError("TabStops object is empty")
        tab = tabs.tab_lst[idx]
        return TabStop(tab)

    def __iter__(self):
        """Generate a TabStop object for each of the w:tab elements, in XML document
        order."""
        tabs = self._pPr.tabs
        if tabs is not None:
            for tab in tabs.tab_lst:
                yield TabStop(tab)

    def __len__(self):
        tabs = self._pPr.tabs
        if tabs is None:
            return 0
        return len(tabs.tab_lst)

    def add_tab_stop(self, position, alignment=WD_TAB_ALIGNMENT.LEFT, leader=WD_TAB_LEADER.SPACES):
        """Add a new tab stop at `position`, a |Length| object specifying the location
        of the tab stop relative to the paragraph edge.

        A negative `position` value is valid and appears in hanging indentation. Tab
        alignment defaults to left, but may be specified by passing a member of the
        :ref:`WdTabAlignment` enumeration as `alignment`. An optional leader character
        can be specified by passing a member of the :ref:`WdTabLeader` enumeration as
        `leader`.
        """
        tabs = self._pPr.get_or_add_tabs()
        tab = tabs.insert_tab_in_order(position, alignment, leader)
        return TabStop(tab)

    def clear_all(self):
        """Remove all custom tab stops."""
        self._pPr._remove_tabs()


class TabStop(ElementProxy):
    """An individual tab stop applying to a paragraph or style.

    Accessed using list semantics on its containing |TabStops| object.
    """

    def __init__(self, element):
        super(TabStop, self).__init__(element, None)
        self._tab = element

    @property
    def alignment(self):
        """A member of :ref:`WdTabAlignment` specifying the alignment setting for this
        tab stop.

        Read/write.
        """
        return self._tab.val

    @alignment.setter
    def alignment(self, value):
        self._tab.val = value

    @property
    def leader(self):
        """A member of :ref:`WdTabLeader` specifying a repeating character used as a
        "leader", filling in the space spanned by this tab.

        Assigning |None| produces the same result as assigning `WD_TAB_LEADER.SPACES`.
        Read/write.
        """
        return self._tab.leader

    @leader.setter
    def leader(self, value):
        self._tab.leader = value

    @property
    def position(self):
        """A |Length| object representing the distance of this tab stop from the inside
        edge of the paragraph.

        May be positive or negative. Read/write.
        """
        return self._tab.pos

    @position.setter
    def position(self, value):
        tab = self._tab
        tabs = tab.getparent()
        self._tab = tabs.insert_tab_in_order(value, tab.val, tab.leader)
        tabs.remove(tab)
