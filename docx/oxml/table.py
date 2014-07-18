# encoding: utf-8

"""
Custom element classes for tables
"""

from __future__ import absolute_import, print_function, unicode_literals

from . import parse_xml
from .ns import nsdecls
from ..shared import Emu, Twips
from .simpletypes import (
    ST_TblLayoutType, ST_TblWidth, ST_TwipsMeasure, XsdInt
)
from .xmlchemy import (
    BaseOxmlElement, OneAndOnlyOne, OneOrMore, OptionalAttribute,
    RequiredAttribute, ZeroOrOne, ZeroOrMore
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


class CT_TblLayoutType(BaseOxmlElement):
    """
    ``<w:tblLayout>`` element, specifying whether column widths are fixed or
    can be automatically adjusted based on content.
    """
    type = OptionalAttribute('w:type', ST_TblLayoutType)


class CT_TblPr(BaseOxmlElement):
    """
    ``<w:tblPr>`` element, child of ``<w:tbl>``, holds child elements that
    define table properties such as style and borders.
    """
    tblStyle = ZeroOrOne('w:tblStyle', successors=(
        'w:tblpPr', 'w:tblOverlap', 'w:bidiVisual', 'w:tblStyleRowBandSize',
        'w:tblStyleColBandSize', 'w:tblW', 'w:jc', 'w:tblCellSpacing',
        'w:tblInd', 'w:tblBorders', 'w:shd', 'w:tblLayout', 'w:tblCellMar',
        'w:tblLook', 'w:tblCaption', 'w:tblDescription', 'w:tblPrChange'
    ))
    tblLayout = ZeroOrOne('w:tblLayout', successors=(
        'w:tblLayout', 'w:tblCellMar', 'w:tblLook', 'w:tblCaption',
        'w:tblDescription', 'w:tblPrChange'
    ))

    @property
    def autofit(self):
        """
        Return |False| if there is a ``<w:tblLayout>`` child with ``w:type``
        attribute set to ``'fixed'``. Otherwise return |True|.
        """
        tblLayout = self.tblLayout
        if tblLayout is None:
            return True
        return False if tblLayout.type == 'fixed' else True

    @autofit.setter
    def autofit(self, value):
        tblLayout = self.get_or_add_tblLayout()
        tblLayout.type = 'autofit' if value else 'fixed'

    @property
    def style(self):
        """
        Return the value of the ``val`` attribute of the ``<w:tblStyle>``
        child or |None| if not present.
        """
        tblStyle = self.tblStyle
        if tblStyle is None:
            return None
        return tblStyle.val

    @style.setter
    def style(self, value):
        self._remove_tblStyle()
        if value is None:
            return
        self._add_tblStyle(val=value)


class CT_TblWidth(BaseOxmlElement):
    """
    Used for ``<w:tblW>`` and ``<w:tcW>`` elements and many others, to
    specify a table-related width.
    """
    # the type for `w` attr is actually ST_MeasurementOrPercent, but using
    # XsdInt for now because only dxa (twips) values are being used. It's not
    # entirely clear what the semantics are for other values like -01.4mm
    w = RequiredAttribute('w:w', XsdInt)
    type = RequiredAttribute('w:type', ST_TblWidth)

    @property
    def width(self):
        """
        Return the EMU length value represented by the combined ``w:w`` and
        ``w:type`` attributes.
        """
        if self.type != 'dxa':
            return None
        return Twips(self.w)

    @width.setter
    def width(self, value):
        self.type = 'dxa'
        self.w = Emu(value).twips


class CT_Tc(BaseOxmlElement):
    """
    ``<w:tc>`` table cell element
    """
    tcPr = ZeroOrOne('w:tcPr')  # bunches of successors, overriding insert
    p = OneOrMore('w:p')
    tbl = OneOrMore('w:tbl')

    def _insert_tcPr(self, tcPr):
        """
        ``tcPr`` has a bunch of successors, but it comes first if it appears,
        so just overriding and using insert(0, ...) rather than spelling out
        successors.
        """
        self.insert(0, tcPr)
        return tcPr

    def _new_tbl(self):
        return CT_Tbl.new()

    def clear_content(self):
        """
        Remove all content child elements, preserving the ``<w:tcPr>``
        element if present. Note that this leaves the ``<w:tc>`` element in
        an invalid state because it doesn't contain at least one block-level
        element. It's up to the caller to add a ``<w:p>``child element as the
        last content element.
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

    @property
    def width(self):
        """
        Return the EMU length value represented in the ``./w:tcPr/w:tcW``
        child element or |None| if not present.
        """
        tcPr = self.tcPr
        if tcPr is None:
            return None
        return tcPr.width

    @width.setter
    def width(self, value):
        tcPr = self.get_or_add_tcPr()
        tcPr.width = value


class CT_TcPr(BaseOxmlElement):
    """
    ``<w:tcPr>`` element, defining table cell properties
    """
    tcW = ZeroOrOne('w:tcW', successors=(
        'w:gridSpan', 'w:hMerge', 'w:vMerge', 'w:tcBorders', 'w:shd',
        'w:noWrap', 'w:tcMar', 'w:textDirection', 'w:tcFitText', 'w:vAlign',
        'w:hideMark', 'w:headers', 'w:cellIns', 'w:cellDel', 'w:cellMerge',
        'w:tcPrChange'
    ))

    @property
    def width(self):
        """
        Return the EMU length value represented in the ``<w:tcW>`` child
        element or |None| if not present or its type is not 'dxa'.
        """
        tcW = self.tcW
        if tcW is None:
            return None
        return tcW.width

    @width.setter
    def width(self, value):
        tcW = self.get_or_add_tcW()
        tcW.width = value
