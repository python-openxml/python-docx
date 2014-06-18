# encoding: utf-8

"""
Custom element classes for tables
"""

from __future__ import absolute_import, print_function, unicode_literals

from . import parse_xml
from .ns import nsdecls
from .simpletypes import ST_TwipsMeasure
from .xmlchemy import (
    BaseOxmlElement, OneAndOnlyOne, OneOrMore, OptionalAttribute, ZeroOrOne,
    ZeroOrMore
)


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
        tbl = parse_xml(cls._tbl_xml())
        return tbl

    @classmethod
    def _tbl_xml(cls):
        return (
            '<w:tbl %s>\n'
            '  <w:tblPr>\n'
            '    <w:tblW w:type="auto" w:w="0"/>\n'
            '  </w:tblPr>\n'
            '  <w:tblGrid/>\n'
            '</w:tbl>' % nsdecls('w')
        )


class CT_TblGrid(BaseOxmlElement):
    """
    ``<w:tblGrid>`` element, child of ``<w:tbl>``, holds ``<w:gridCol>``
    elements that define column count, width, etc.
    """
    gridCol = ZeroOrMore('w:gridCol', successors=('w:tblGridChange',))


class CT_TblGridCol(BaseOxmlElement):
    """
    ``<w:gridCol>`` element, child of ``<w:tblGrid>``, defines a table
    column.
    """
    w = OptionalAttribute('w:w', ST_TwipsMeasure)


class CT_TblPr(BaseOxmlElement):
    """
    ``<w:tblPr>`` element, child of ``<w:tbl>``, holds child elements that
    define table properties such as style and borders.
    """
    tblStyle = ZeroOrOne('w:tblStyle')

    def add_tblStyle(self, style_name):
        """
        Return a new <w:tblStyle> element having its style set to
        *style_name*.
        """
        return self._add_tblStyle(val=style_name)


class CT_Tc(BaseOxmlElement):
    """
    ``<w:tc>`` table cell element
    """
    tcPr = ZeroOrOne('w:tcPr')  # bunches of successors, overriding insert
    p = OneOrMore('w:p')

    def _insert_tcPr(self, tcPr):
        """
        ``tcPr`` has a bunch of successors, but it comes first if it appears,
        so just overriding and using insert(0, ...) rather than spelling out
        successors.
        """
        self.insert(0, tcPr)
        return tcPr

    def clear_content(self):
        """
        Remove all content child elements, preserving the ``<w:tcPr>``
        element if present. Note that this leaves the ``<w:tc>`` element in
        an invalid state because it doesn't contain at least one block-level
        element. It's up to the caller to add a ``<w:p>`` or ``<w:tbl>``
        child element.
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
        return parse_xml(
            '<w:tc %s>\n'
            '  <w:p/>\n'
            '</w:tc>' % nsdecls('w')
        )
