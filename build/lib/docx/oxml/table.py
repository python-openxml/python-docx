# encoding: utf-8

"""Custom element classes for tables"""

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

from . import parse_xml
from ..enum.table import WD_CELL_VERTICAL_ALIGNMENT, WD_ROW_HEIGHT_RULE
from ..exceptions import InvalidSpanError
from .ns import nsdecls, qn
from ..shared import Emu, Twips
from .simpletypes import (
    ST_Merge, ST_TblLayoutType, ST_TblWidth, ST_TwipsMeasure, XsdInt
)
from .xmlchemy import (
    BaseOxmlElement, OneAndOnlyOne, OneOrMore, OptionalAttribute,
    RequiredAttribute, ZeroOrOne, ZeroOrMore
)


class CT_Height(BaseOxmlElement):
    """
    Used for ``<w:trHeight>`` to specify a row height and row height rule.
    """
    val = OptionalAttribute('w:val', ST_TwipsMeasure)
    hRule = OptionalAttribute('w:hRule', WD_ROW_HEIGHT_RULE)


class CT_Row(BaseOxmlElement):
    """
    ``<w:tr>`` element
    """
    tblPrEx = ZeroOrOne('w:tblPrEx')  # custom inserter below
    trPr = ZeroOrOne('w:trPr')        # custom inserter below
    tc = ZeroOrMore('w:tc')

    def tc_at_grid_col(self, idx):
        """
        The ``<w:tc>`` element appearing at grid column *idx*. Raises
        |ValueError| if no ``w:tc`` element begins at that grid column.
        """
        grid_col = 0
        for tc in self.tc_lst:
            if grid_col == idx:
                return tc
            grid_col += tc.grid_span
            if grid_col > idx:
                raise ValueError('no cell on grid column %d' % idx)
        raise ValueError('index out of bounds')

    @property
    def tr_idx(self):
        """
        The index of this ``<w:tr>`` element within its parent ``<w:tbl>``
        element.
        """
        return self.getparent().tr_lst.index(self)

    @property
    def trHeight_hRule(self):
        """
        Return the value of `w:trPr/w:trHeight@w:hRule`, or |None| if not
        present.
        """
        trPr = self.trPr
        if trPr is None:
            return None
        return trPr.trHeight_hRule

    @trHeight_hRule.setter
    def trHeight_hRule(self, value):
        trPr = self.get_or_add_trPr()
        trPr.trHeight_hRule = value

    @property
    def trHeight_val(self):
        """
        Return the value of `w:trPr/w:trHeight@w:val`, or |None| if not
        present.
        """
        trPr = self.trPr
        if trPr is None:
            return None
        return trPr.trHeight_val

    @trHeight_val.setter
    def trHeight_val(self, value):
        trPr = self.get_or_add_trPr()
        trPr.trHeight_val = value

    def _insert_tblPrEx(self, tblPrEx):
        self.insert(0, tblPrEx)

    def _insert_trPr(self, trPr):
        tblPrEx = self.tblPrEx
        if tblPrEx is not None:
            tblPrEx.addnext(trPr)
        else:
            self.insert(0, trPr)

    def _new_tc(self):
        return CT_Tc.new()


class CT_Tbl(BaseOxmlElement):
    """
    ``<w:tbl>`` element
    """
    tblPr = OneAndOnlyOne('w:tblPr')
    tblGrid = OneAndOnlyOne('w:tblGrid')
    tr = ZeroOrMore('w:tr')

    @property
    def bidiVisual_val(self):
        """
        Value of `w:tblPr/w:bidiVisual/@w:val` or |None| if not present.
        Controls whether table cells are displayed right-to-left or
        left-to-right.
        """
        bidiVisual = self.tblPr.bidiVisual
        if bidiVisual is None:
            return None
        return bidiVisual.val

    @bidiVisual_val.setter
    def bidiVisual_val(self, value):
        tblPr = self.tblPr
        if value is None:
            tblPr._remove_bidiVisual()
        else:
            tblPr.get_or_add_bidiVisual().val = value

    @property
    def col_count(self):
        """
        The number of grid columns in this table.
        """
        return len(self.tblGrid.gridCol_lst)

    def iter_tcs(self):
        """
        Generate each of the `w:tc` elements in this table, left to right and
        top to bottom. Each cell in the first row is generated, followed by
        each cell in the second row, etc.
        """
        for tr in self.tr_lst:
            for tc in tr.tc_lst:
                yield tc

    @classmethod
    def new_tbl(cls, rows, cols, width):
        """
        Return a new `w:tbl` element having *rows* rows and *cols* columns
        with *width* distributed evenly between the columns.
        """
        return parse_xml(cls._tbl_xml(rows, cols, width))

    @property
    def tblStyle_val(self):
        """
        Value of `w:tblPr/w:tblStyle/@w:val` (a table style id) or |None| if
        not present.
        """
        tblStyle = self.tblPr.tblStyle
        if tblStyle is None:
            return None
        return tblStyle.val

    @tblStyle_val.setter
    def tblStyle_val(self, styleId):
        """
        Set the value of `w:tblPr/w:tblStyle/@w:val` (a table style id) to
        *styleId*. If *styleId* is None, remove the `w:tblStyle` element.
        """
        tblPr = self.tblPr
        tblPr._remove_tblStyle()
        if styleId is None:
            return
        tblPr._add_tblStyle().val = styleId

    @classmethod
    def _tbl_xml(cls, rows, cols, width):
        col_width = Emu(width/cols) if cols > 0 else Emu(0)
        return (
            '<w:tbl %s>\n'
            '  <w:tblPr>\n'
            '    <w:tblW w:type="auto" w:w="0"/>\n'
            '    <w:tblLook w:firstColumn="1" w:firstRow="1"\n'
            '               w:lastColumn="0" w:lastRow="0" w:noHBand="0"\n'
            '               w:noVBand="1" w:val="04A0"/>\n'
            '  </w:tblPr>\n'
            '%s'  # tblGrid
            '%s'  # trs
            '</w:tbl>\n'
        ) % (
            nsdecls('w'),
            cls._tblGrid_xml(cols, col_width),
            cls._trs_xml(rows, cols, col_width)
        )

    @classmethod
    def _tblGrid_xml(cls, col_count, col_width):
        xml = '  <w:tblGrid>\n'
        for i in range(col_count):
            xml += '    <w:gridCol w:w="%d"/>\n' % col_width.twips
        xml += '  </w:tblGrid>\n'
        return xml

    @classmethod
    def _trs_xml(cls, row_count, col_count, col_width):
        xml = ''
        for i in range(row_count):
            xml += (
                '  <w:tr>\n'
                '%s'
                '  </w:tr>\n'
            ) % cls._tcs_xml(col_count, col_width)
        return xml

    @classmethod
    def _tcs_xml(cls, col_count, col_width):
        xml = ''
        for i in range(col_count):
            xml += (
                '    <w:tc>\n'
                '      <w:tcPr>\n'
                '        <w:tcW w:type="dxa" w:w="%d"/>\n'
                '      </w:tcPr>\n'
                '      <w:p/>\n'
                '    </w:tc>\n'
            ) % col_width.twips
        return xml


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

    @property
    def gridCol_idx(self):
        """
        The index of this ``<w:gridCol>`` element within its parent
        ``<w:tblGrid>`` element.
        """
        return self.getparent().gridCol_lst.index(self)


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
    _tag_seq = (
        'w:tblStyle', 'w:tblpPr', 'w:tblOverlap', 'w:bidiVisual',
        'w:tblStyleRowBandSize', 'w:tblStyleColBandSize', 'w:tblW', 'w:jc',
        'w:tblCellSpacing', 'w:tblInd', 'w:tblBorders', 'w:shd',
        'w:tblLayout', 'w:tblCellMar', 'w:tblLook', 'w:tblCaption',
        'w:tblDescription', 'w:tblPrChange'
    )
    tblStyle = ZeroOrOne('w:tblStyle', successors=_tag_seq[1:])
    bidiVisual = ZeroOrOne('w:bidiVisual', successors=_tag_seq[4:])
    jc = ZeroOrOne('w:jc', successors=_tag_seq[8:])
    tblLayout = ZeroOrOne('w:tblLayout', successors=_tag_seq[13:])
    del _tag_seq

    @property
    def alignment(self):
        """
        Member of :ref:`WdRowAlignment` enumeration or |None|, based on the
        contents of the `w:val` attribute of `./w:jc`. |None| if no `w:jc`
        element is present.
        """
        jc = self.jc
        if jc is None:
            return None
        return jc.val

    @alignment.setter
    def alignment(self, value):
        self._remove_jc()
        if value is None:
            return
        jc = self.get_or_add_jc()
        jc.val = value

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
    """`w:tc` table cell element"""

    tcPr = ZeroOrOne('w:tcPr')  # bunches of successors, overriding insert
    p = OneOrMore('w:p')
    tbl = OneOrMore('w:tbl')

    @property
    def bottom(self):
        """
        The row index that marks the bottom extent of the vertical span of
        this cell. This is one greater than the index of the bottom-most row
        of the span, similar to how a slice of the cell's rows would be
        specified.
        """
        if self.vMerge is not None:
            tc_below = self._tc_below
            if tc_below is not None and tc_below.vMerge == ST_Merge.CONTINUE:
                return tc_below.bottom
        return self._tr_idx + 1

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

    @property
    def grid_span(self):
        """
        The integer number of columns this cell spans. Determined by
        ./w:tcPr/w:gridSpan/@val, it defaults to 1.
        """
        tcPr = self.tcPr
        if tcPr is None:
            return 1
        return tcPr.grid_span

    @grid_span.setter
    def grid_span(self, value):
        tcPr = self.get_or_add_tcPr()
        tcPr.grid_span = value

    def iter_block_items(self):
        """
        Generate a reference to each of the block-level content elements in
        this cell, in the order they appear.
        """
        block_item_tags = (qn('w:p'), qn('w:tbl'), qn('w:sdt'))
        for child in self:
            if child.tag in block_item_tags:
                yield child

    @property
    def left(self):
        """
        The grid column index at which this ``<w:tc>`` element appears.
        """
        return self._grid_col

    def merge(self, other_tc):
        """
        Return the top-left ``<w:tc>`` element of a new span formed by
        merging the rectangular region defined by using this tc element and
        *other_tc* as diagonal corners.
        """
        top, left, height, width = self._span_dimensions(other_tc)
        top_tc = self._tbl.tr_lst[top].tc_at_grid_col(left)
        top_tc._grow_to(width, height)
        return top_tc

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
    def right(self):
        """
        The grid column index that marks the right-side extent of the
        horizontal span of this cell. This is one greater than the index of
        the right-most column of the span, similar to how a slice of the
        cell's columns would be specified.
        """
        return self._grid_col + self.grid_span

    @property
    def top(self):
        """
        The top-most row index in the vertical span of this cell.
        """
        if self.vMerge is None or self.vMerge == ST_Merge.RESTART:
            return self._tr_idx
        return self._tc_above.top

    @property
    def vMerge(self):
        """
        The value of the ./w:tcPr/w:vMerge/@val attribute, or |None| if the
        w:vMerge element is not present.
        """
        tcPr = self.tcPr
        if tcPr is None:
            return None
        return tcPr.vMerge_val

    @vMerge.setter
    def vMerge(self, value):
        tcPr = self.get_or_add_tcPr()
        tcPr.vMerge_val = value

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

    def _add_width_of(self, other_tc):
        """
        Add the width of *other_tc* to this cell. Does nothing if either this
        tc or *other_tc* does not have a specified width.
        """
        if self.width and other_tc.width:
            self.width += other_tc.width

    @property
    def _grid_col(self):
        """
        The grid column at which this cell begins.
        """
        tr = self._tr
        idx = tr.tc_lst.index(self)
        preceding_tcs = tr.tc_lst[:idx]
        return sum(tc.grid_span for tc in preceding_tcs)

    def _grow_to(self, width, height, top_tc=None):
        """
        Grow this cell to *width* grid columns and *height* rows by expanding
        horizontal spans and creating continuation cells to form vertical
        spans.
        """
        def vMerge_val(top_tc):
            if top_tc is not self:
                return ST_Merge.CONTINUE
            if height == 1:
                return None
            return ST_Merge.RESTART

        top_tc = self if top_tc is None else top_tc
        self._span_to_width(width, top_tc, vMerge_val(top_tc))
        if height > 1:
            self._tc_below._grow_to(width, height-1, top_tc)

    def _insert_tcPr(self, tcPr):
        """
        ``tcPr`` has a bunch of successors, but it comes first if it appears,
        so just overriding and using insert(0, ...) rather than spelling out
        successors.
        """
        self.insert(0, tcPr)
        return tcPr

    @property
    def _is_empty(self):
        """
        True if this cell contains only a single empty ``<w:p>`` element.
        """
        block_items = list(self.iter_block_items())
        if len(block_items) > 1:
            return False
        p = block_items[0]  # cell must include at least one <w:p> element
        if len(p.r_lst) == 0:
            return True
        return False

    def _move_content_to(self, other_tc):
        """
        Append the content of this cell to *other_tc*, leaving this cell with
        a single empty ``<w:p>`` element.
        """
        if other_tc is self:
            return
        if self._is_empty:
            return
        other_tc._remove_trailing_empty_p()
        # appending moves each element from self to other_tc
        for block_element in self.iter_block_items():
            other_tc.append(block_element)
        # add back the required minimum single empty <w:p> element
        self.append(self._new_p())

    def _new_tbl(self):
        return CT_Tbl.new()

    @property
    def _next_tc(self):
        """
        The `w:tc` element immediately following this one in this row, or
        |None| if this is the last `w:tc` element in the row.
        """
        following_tcs = self.xpath('./following-sibling::w:tc')
        return following_tcs[0] if following_tcs else None

    def _remove(self):
        """
        Remove this `w:tc` element from the XML tree.
        """
        self.getparent().remove(self)

    def _remove_trailing_empty_p(self):
        """
        Remove the last content element from this cell if it is an empty
        ``<w:p>`` element.
        """
        block_items = list(self.iter_block_items())
        last_content_elm = block_items[-1]
        if last_content_elm.tag != qn('w:p'):
            return
        p = last_content_elm
        if len(p.r_lst) > 0:
            return
        self.remove(p)

    def _span_dimensions(self, other_tc):
        """
        Return a (top, left, height, width) 4-tuple specifying the extents of
        the merged cell formed by using this tc and *other_tc* as opposite
        corner extents.
        """
        def raise_on_inverted_L(a, b):
            if a.top == b.top and a.bottom != b.bottom:
                raise InvalidSpanError('requested span not rectangular')
            if a.left == b.left and a.right != b.right:
                raise InvalidSpanError('requested span not rectangular')

        def raise_on_tee_shaped(a, b):
            top_most, other = (a, b) if a.top < b.top else (b, a)
            if top_most.top < other.top and top_most.bottom > other.bottom:
                raise InvalidSpanError('requested span not rectangular')

            left_most, other = (a, b) if a.left < b.left else (b, a)
            if left_most.left < other.left and left_most.right > other.right:
                raise InvalidSpanError('requested span not rectangular')

        raise_on_inverted_L(self, other_tc)
        raise_on_tee_shaped(self, other_tc)

        top = min(self.top, other_tc.top)
        left = min(self.left, other_tc.left)
        bottom = max(self.bottom, other_tc.bottom)
        right = max(self.right, other_tc.right)

        return top, left, bottom - top, right - left

    def _span_to_width(self, grid_width, top_tc, vMerge):
        """
        Incorporate and then remove `w:tc` elements to the right of this one
        until this cell spans *grid_width*. Raises |ValueError| if
        *grid_width* cannot be exactly achieved, such as when a merged cell
        would drive the span width greater than *grid_width* or if not enough
        grid columns are available to make this cell that wide. All content
        from incorporated cells is appended to *top_tc*. The val attribute of
        the vMerge element on the single remaining cell is set to *vMerge*.
        If *vMerge* is |None|, the vMerge element is removed if present.
        """
        self._move_content_to(top_tc)
        while self.grid_span < grid_width:
            self._swallow_next_tc(grid_width, top_tc)
        self.vMerge = vMerge

    def _swallow_next_tc(self, grid_width, top_tc):
        """
        Extend the horizontal span of this `w:tc` element to incorporate the
        following `w:tc` element in the row and then delete that following
        `w:tc` element. Any content in the following `w:tc` element is
        appended to the content of *top_tc*. The width of the following
        `w:tc` element is added to this one, if present. Raises
        |InvalidSpanError| if the width of the resulting cell is greater than
        *grid_width* or if there is no next `<w:tc>` element in the row.
        """
        def raise_on_invalid_swallow(next_tc):
            if next_tc is None:
                raise InvalidSpanError('not enough grid columns')
            if self.grid_span + next_tc.grid_span > grid_width:
                raise InvalidSpanError('span is not rectangular')

        next_tc = self._next_tc
        raise_on_invalid_swallow(next_tc)
        next_tc._move_content_to(top_tc)
        self._add_width_of(next_tc)
        self.grid_span += next_tc.grid_span
        next_tc._remove()

    @property
    def _tbl(self):
        """
        The tbl element this tc element appears in.
        """
        return self.xpath('./ancestor::w:tbl[position()=1]')[0]

    @property
    def _tc_above(self):
        """
        The `w:tc` element immediately above this one in its grid column.
        """
        return self._tr_above.tc_at_grid_col(self._grid_col)

    @property
    def _tc_below(self):
        """
        The tc element immediately below this one in its grid column.
        """
        tr_below = self._tr_below
        if tr_below is None:
            return None
        return tr_below.tc_at_grid_col(self._grid_col)

    @property
    def _tr(self):
        """
        The tr element this tc element appears in.
        """
        return self.xpath('./ancestor::w:tr[position()=1]')[0]

    @property
    def _tr_above(self):
        """
        The tr element prior in sequence to the tr this cell appears in.
        Raises |ValueError| if called on a cell in the top-most row.
        """
        tr_lst = self._tbl.tr_lst
        tr_idx = tr_lst.index(self._tr)
        if tr_idx == 0:
            raise ValueError('no tr above topmost tr')
        return tr_lst[tr_idx-1]

    @property
    def _tr_below(self):
        """
        The tr element next in sequence after the tr this cell appears in, or
        |None| if this cell appears in the last row.
        """
        tr_lst = self._tbl.tr_lst
        tr_idx = tr_lst.index(self._tr)
        try:
            return tr_lst[tr_idx+1]
        except IndexError:
            return None

    @property
    def _tr_idx(self):
        """
        The row index of the tr element this tc element appears in.
        """
        return self._tbl.tr_lst.index(self._tr)


class CT_TcPr(BaseOxmlElement):
    """
    ``<w:tcPr>`` element, defining table cell properties
    """
    _tag_seq = (
        'w:cnfStyle', 'w:tcW', 'w:gridSpan', 'w:hMerge', 'w:vMerge',
        'w:tcBorders', 'w:shd', 'w:noWrap', 'w:tcMar', 'w:textDirection',
        'w:tcFitText', 'w:vAlign', 'w:hideMark', 'w:headers', 'w:cellIns',
        'w:cellDel', 'w:cellMerge', 'w:tcPrChange'
    )
    tcW = ZeroOrOne('w:tcW', successors=_tag_seq[2:])
    gridSpan = ZeroOrOne('w:gridSpan', successors=_tag_seq[3:])
    vMerge = ZeroOrOne('w:vMerge', successors=_tag_seq[5:])
    vAlign = ZeroOrOne('w:vAlign', successors=_tag_seq[12:])
    del _tag_seq

    @property
    def grid_span(self):
        """
        The integer number of columns this cell spans. Determined by
        ./w:gridSpan/@val, it defaults to 1.
        """
        gridSpan = self.gridSpan
        if gridSpan is None:
            return 1
        return gridSpan.val

    @grid_span.setter
    def grid_span(self, value):
        self._remove_gridSpan()
        if value > 1:
            self.get_or_add_gridSpan().val = value

    @property
    def vAlign_val(self):
        """Value of `w:val` attribute on  `w:vAlign` child.

        Value is |None| if `w:vAlign` child is not present. The `w:val`
        attribute on `w:vAlign` is required.
        """
        vAlign = self.vAlign
        if vAlign is None:
            return None
        return vAlign.val

    @vAlign_val.setter
    def vAlign_val(self, value):
        if value is None:
            self._remove_vAlign()
            return
        self.get_or_add_vAlign().val = value

    @property
    def vMerge_val(self):
        """
        The value of the ./w:vMerge/@val attribute, or |None| if the
        w:vMerge element is not present.
        """
        vMerge = self.vMerge
        if vMerge is None:
            return None
        return vMerge.val

    @vMerge_val.setter
    def vMerge_val(self, value):
        self._remove_vMerge()
        if value is not None:
            self._add_vMerge().val = value

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


class CT_TrPr(BaseOxmlElement):
    """
    ``<w:trPr>`` element, defining table row properties
    """
    _tag_seq = (
        'w:cnfStyle', 'w:divId', 'w:gridBefore', 'w:gridAfter', 'w:wBefore',
        'w:wAfter', 'w:cantSplit', 'w:trHeight', 'w:tblHeader',
        'w:tblCellSpacing', 'w:jc', 'w:hidden', 'w:ins', 'w:del',
        'w:trPrChange'
    )
    trHeight = ZeroOrOne('w:trHeight', successors=_tag_seq[8:])
    del _tag_seq

    @property
    def trHeight_hRule(self):
        """
        Return the value of `w:trHeight@w:hRule`, or |None| if not present.
        """
        trHeight = self.trHeight
        if trHeight is None:
            return None
        return trHeight.hRule

    @trHeight_hRule.setter
    def trHeight_hRule(self, value):
        if value is None and self.trHeight is None:
            return
        trHeight = self.get_or_add_trHeight()
        trHeight.hRule = value

    @property
    def trHeight_val(self):
        """
        Return the value of `w:trHeight@w:val`, or |None| if not present.
        """
        trHeight = self.trHeight
        if trHeight is None:
            return None
        return trHeight.val

    @trHeight_val.setter
    def trHeight_val(self, value):
        if value is None and self.trHeight is None:
            return
        trHeight = self.get_or_add_trHeight()
        trHeight.val = value


class CT_VerticalJc(BaseOxmlElement):
    """`w:vAlign` element, specifying vertical alignment of cell."""
    val = RequiredAttribute('w:val', WD_CELL_VERTICAL_ALIGNMENT)


class CT_VMerge(BaseOxmlElement):
    """
    ``<w:vMerge>`` element, specifying vertical merging behavior of a cell.
    """
    val = OptionalAttribute('w:val', ST_Merge, default=ST_Merge.CONTINUE)
