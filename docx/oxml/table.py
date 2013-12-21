# encoding: utf-8

"""
Custom element classes for tables
"""

from __future__ import absolute_import, print_function, unicode_literals

from docx.oxml.shared import OxmlBaseElement, OxmlElement, qn

from . import ValidationError
from .text import CT_P


class CT_Row(OxmlBaseElement):
    """
    ``<w:tr>`` element
    """
    def add_tc(self):
        """
        Return a new <w:tc> element that has been added at the end of any
        existing tc elements.
        """
        tc = CT_Tc.new()
        return self._append_tc(tc)

    def _append_tc(self, tc):
        """
        Return *tc* after appending it to end of tc sequence.
        """
        self.append(tc)
        return tc


class CT_Tbl(OxmlBaseElement):
    """
    ``<w:tbl>`` element
    """
    @property
    def tblGrid(self):
        tblGrid = self.find(qn('w:tblGrid'))
        if tblGrid is None:
            raise ValidationError('required w:tblGrid child not found')
        return tblGrid

    @property
    def tr_lst(self):
        """
        Sequence containing the ``<w:tr>`` child elements in this
        ``<w:tbl>``.
        """
        return self.findall(qn('w:tr'))


class CT_TblGrid(OxmlBaseElement):
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


class CT_TblGridCol(OxmlBaseElement):
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


class CT_Tc(OxmlBaseElement):
    """
    ``<w:tc>`` table cell element
    """
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
