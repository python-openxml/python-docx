# encoding: utf-8

"""
Custom element classes for tables
"""

from __future__ import absolute_import, print_function, unicode_literals

from . import OxmlElement
from .ns import qn
from .shared import CT_String
from .text import CT_P
from .xmlchemy import BaseOxmlElement, OneAndOnlyOne, ZeroOrMore


class CT_Row(BaseOxmlElement):
    """
    ``<w:tr>`` element
    """
    tc = ZeroOrMore('w:tc')

    def _new_tc(self):
        return CT_Tc.new()


class CT_Tbl(BaseOxmlElement):
    """
    ``<w:tbl>`` element
    """
    tblPr = OneAndOnlyOne('w:tblPr')
    tblGrid = OneAndOnlyOne('w:tblGrid')
    tr = ZeroOrMore('w:tr')

    @classmethod
    def new(cls):
        """
        Return a new ``<w:tbl>`` element, containing the required
        ``<w:tblPr>`` and ``<w:tblGrid>`` child elements.
        """
        tbl = OxmlElement('w:tbl')
        tblPr = CT_TblPr.new()
        tbl.append(tblPr)
        tblGrid = CT_TblGrid.new()
        tbl.append(tblGrid)
        return tbl


class CT_TblGrid(BaseOxmlElement):
    """
    ``<w:tblGrid>`` element, child of ``<w:tbl>``, holds ``<w:gridCol>``
    elements that define column count, width, etc.
    """
    def add_gridCol(self):
        """
        Return a new <w:gridCol> element that has been added at the end of
        any existing gridCol elements.
        """
        gridCol = CT_TblGridCol.new()
        return self._append_gridCol(gridCol)

    @property
    def gridCol_lst(self):
        """
        Sequence containing the ``<w:gridCol>`` child elements in this
        ``<w:tblGrid>``.
        """
        return self.findall(qn('w:gridCol'))

    @classmethod
    def new(cls):
        """
        Return a new ``<w:tblGrid>`` element.
        """
        return OxmlElement('w:tblGrid')

    def _append_gridCol(self, gridCol):
        """
        Return *gridCol* after appending it to end of gridCol sequence.
        """
        successor = self.first_child_found_in('w:tblGridChange')
        if successor is not None:
            successor.addprevious(gridCol)
        else:
            self.append(gridCol)
        return gridCol

    def first_child_found_in(self, *tagnames):
        """
        Return the first child found with tag in *tagnames*, or None if
        not found.
        """
        for tagname in tagnames:
            child = self.find(qn(tagname))
            if child is not None:
                return child
        return None


class CT_TblGridCol(BaseOxmlElement):
    """
    ``<w:gridCol>`` element, child of ``<w:tblGrid>``, defines a table
    column.
    """
    @classmethod
    def new(cls):
        """
        Return a new ``<w:gridCol>`` element.
        """
        return OxmlElement('w:gridCol')


class CT_TblPr(BaseOxmlElement):
    """
    ``<w:tblPr>`` element, child of ``<w:tbl>``, holds child elements that
    define table properties such as style and borders.
    """
    def add_tblStyle(self, style_name):
        """
        Return a new <w:tblStyle> element newly inserted in sequence among
        the existing child elements, respecting the schema definition.
        """
        tblStyle = CT_String.new('w:tblStyle', style_name)
        return self._insert_tblStyle(tblStyle)

    @classmethod
    def new(cls):
        """
        Return a new ``<w:tblPr>`` element.
        """
        return OxmlElement('w:tblPr')

    @property
    def tblStyle(self):
        """
        Optional <w:tblStyle> child element, or |None| if not present.
        """
        return self.find(qn('w:tblStyle'))

    def _insert_tblStyle(self, tblStyle):
        """
        Return *tblStyle* after inserting it in sequence among the existing
        child elements. Assumes no ``<w:tblStyle>`` element is present.
        """
        assert self.tblStyle is None
        self.insert(0, tblStyle)
        return tblStyle


class CT_Tc(BaseOxmlElement):
    """
    ``<w:tc>`` table cell element
    """
    def add_p(self):
        """
        Return a new <w:p> element that has been added at the end of any
        existing cell content.
        """
        p = CT_P.new()
        self.append(p)
        return p

    def clear_content(self):
        """
        Remove all content child elements, preserving the ``<w:tcPr>``
        element if present.
        """
        new_children = []
        tcPr = self.tcPr
        if tcPr is not None:
            new_children.append(tcPr)
        self[:] = new_children

    @classmethod
    def new(cls):
        """
        Return a new ``<w:tc>`` element, containing an empty paragraph as the
        required EG_BlockLevelElt.
        """
        tc = OxmlElement('w:tc')
        p = CT_P.new()
        tc.append(p)
        return tc

    @property
    def p_lst(self):
        """
        List of <w:p> child elements.
        """
        return self.findall(qn('w:p'))

    @property
    def tcPr(self):
        """
        <w:tcPr> child element or |None| if not present.
        """
        return self.find(qn('w:tcPr'))
