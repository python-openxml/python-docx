"""Custom element classes for tables."""

from __future__ import annotations

from typing import TYPE_CHECKING, Callable, cast

from docx.enum.table import WD_CELL_VERTICAL_ALIGNMENT, WD_ROW_HEIGHT_RULE, WD_TABLE_DIRECTION
from docx.exceptions import InvalidSpanError
from docx.oxml.ns import nsdecls, qn
from docx.oxml.parser import parse_xml
from docx.oxml.shared import CT_DecimalNumber
from docx.oxml.simpletypes import (
    ST_Merge,
    ST_TblLayoutType,
    ST_TblWidth,
    ST_TwipsMeasure,
    XsdInt,
)
from docx.oxml.text.paragraph import CT_P
from docx.oxml.xmlchemy import (
    BaseOxmlElement,
    OneAndOnlyOne,
    OneOrMore,
    OptionalAttribute,
    RequiredAttribute,
    ZeroOrMore,
    ZeroOrOne,
)
from docx.shared import Emu, Length, Twips

if TYPE_CHECKING:
    from docx.enum.table import WD_TABLE_ALIGNMENT
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.oxml.shared import CT_OnOff, CT_String
    from docx.oxml.text.parfmt import CT_Jc


class CT_Height(BaseOxmlElement):
    """Used for `w:trHeight` to specify a row height and row height rule."""

    val: Length | None = OptionalAttribute(  # pyright: ignore[reportAssignmentType]
        "w:val", ST_TwipsMeasure
    )
    hRule: WD_ROW_HEIGHT_RULE | None = OptionalAttribute(  # pyright: ignore[reportAssignmentType]
        "w:hRule", WD_ROW_HEIGHT_RULE
    )


class CT_Row(BaseOxmlElement):
    """``<w:tr>`` element."""

    add_tc: Callable[[], CT_Tc]
    get_or_add_trPr: Callable[[], CT_TrPr]
    _add_trPr: Callable[[], CT_TrPr]

    tc_lst: list[CT_Tc]
    # -- custom inserter below --
    tblPrEx: CT_TblPrEx | None = ZeroOrOne("w:tblPrEx")  # pyright: ignore[reportAssignmentType]
    # -- custom inserter below --
    trPr: CT_TrPr | None = ZeroOrOne("w:trPr")  # pyright: ignore[reportAssignmentType]
    tc = ZeroOrMore("w:tc")

    @property
    def grid_after(self) -> int:
        """The number of unpopulated layout-grid cells at the end of this row."""
        trPr = self.trPr
        if trPr is None:
            return 0
        return trPr.grid_after

    @property
    def grid_before(self) -> int:
        """The number of unpopulated layout-grid cells at the start of this row."""
        trPr = self.trPr
        if trPr is None:
            return 0
        return trPr.grid_before

    def tc_at_grid_offset(self, grid_offset: int) -> CT_Tc:
        """The `tc` element in this tr at exact `grid offset`.

        Raises ValueError when this `w:tr` contains no `w:tc` with exact starting `grid_offset`.
        """
        # -- account for omitted cells at the start of the row --
        remaining_offset = grid_offset - self.grid_before

        for tc in self.tc_lst:
            # -- We've gone past grid_offset without finding a tc, no sense searching further. --
            if remaining_offset < 0:
                break
            # -- We've arrived at grid_offset, this is the `w:tc` we're looking for. --
            if remaining_offset == 0:
                return tc
            # -- We're not there yet, skip forward the number of layout-grid cells this cell
            # -- occupies.
            remaining_offset -= tc.grid_span

        raise ValueError(f"no `tc` element at grid_offset={grid_offset}")

    @property
    def tr_idx(self) -> int:
        """Index of this `w:tr` element within its parent `w:tbl` element."""
        tbl = cast(CT_Tbl, self.getparent())
        return tbl.tr_lst.index(self)

    @property
    def trHeight_hRule(self) -> WD_ROW_HEIGHT_RULE | None:
        """The value of `./w:trPr/w:trHeight/@w:hRule`, or |None| if not present."""
        trPr = self.trPr
        if trPr is None:
            return None
        return trPr.trHeight_hRule

    @trHeight_hRule.setter
    def trHeight_hRule(self, value: WD_ROW_HEIGHT_RULE | None):
        trPr = self.get_or_add_trPr()
        trPr.trHeight_hRule = value

    @property
    def trHeight_val(self):
        """Return the value of `w:trPr/w:trHeight@w:val`, or |None| if not present."""
        trPr = self.trPr
        if trPr is None:
            return None
        return trPr.trHeight_val

    @trHeight_val.setter
    def trHeight_val(self, value: Length | None):
        trPr = self.get_or_add_trPr()
        trPr.trHeight_val = value

    def _insert_tblPrEx(self, tblPrEx: CT_TblPrEx):
        self.insert(0, tblPrEx)

    def _insert_trPr(self, trPr: CT_TrPr):
        tblPrEx = self.tblPrEx
        if tblPrEx is not None:
            tblPrEx.addnext(trPr)
        else:
            self.insert(0, trPr)

    def _new_tc(self):
        return CT_Tc.new()


class CT_Tbl(BaseOxmlElement):
    """``<w:tbl>`` element."""

    add_tr: Callable[[], CT_Row]
    tr_lst: list[CT_Row]

    tblPr: CT_TblPr = OneAndOnlyOne("w:tblPr")  # pyright: ignore[reportAssignmentType]
    tblGrid: CT_TblGrid = OneAndOnlyOne("w:tblGrid")  # pyright: ignore[reportAssignmentType]
    tr = ZeroOrMore("w:tr")

    @property
    def bidiVisual_val(self) -> bool | None:
        """Value of `./w:tblPr/w:bidiVisual/@w:val` or |None| if not present.

        Controls whether table cells are displayed right-to-left or left-to-right.
        """
        bidiVisual = self.tblPr.bidiVisual
        if bidiVisual is None:
            return None
        return bidiVisual.val

    @bidiVisual_val.setter
    def bidiVisual_val(self, value: WD_TABLE_DIRECTION | None):
        tblPr = self.tblPr
        if value is None:
            tblPr._remove_bidiVisual()  # pyright: ignore[reportPrivateUsage]
        else:
            tblPr.get_or_add_bidiVisual().val = bool(value)

    @property
    def col_count(self):
        """The number of grid columns in this table."""
        return len(self.tblGrid.gridCol_lst)

    def iter_tcs(self):
        """Generate each of the `w:tc` elements in this table, left to right and top to
        bottom.

        Each cell in the first row is generated, followed by each cell in the second
        row, etc.
        """
        for tr in self.tr_lst:
            for tc in tr.tc_lst:
                yield tc

    @classmethod
    def new_tbl(cls, rows: int, cols: int, width: Length) -> CT_Tbl:
        """Return a new `w:tbl` element having `rows` rows and `cols` columns.

        `width` is distributed evenly between the columns.
        """
        return cast(CT_Tbl, parse_xml(cls._tbl_xml(rows, cols, width)))

    @property
    def tblStyle_val(self) -> str | None:
        """`w:tblPr/w:tblStyle/@w:val` (a table style id) or |None| if not present."""
        tblStyle = self.tblPr.tblStyle
        if tblStyle is None:
            return None
        return tblStyle.val

    @tblStyle_val.setter
    def tblStyle_val(self, styleId: str | None) -> None:
        """Set the value of `w:tblPr/w:tblStyle/@w:val` (a table style id) to `styleId`.

        If `styleId` is None, remove the `w:tblStyle` element.
        """
        tblPr = self.tblPr
        tblPr._remove_tblStyle()  # pyright: ignore[reportPrivateUsage]
        if styleId is None:
            return
        tblPr._add_tblStyle().val = styleId  # pyright: ignore[reportPrivateUsage]

    @classmethod
    def _tbl_xml(cls, rows: int, cols: int, width: Length) -> str:
        col_width = Emu(width // cols) if cols > 0 else Emu(0)
        return (
            f"<w:tbl {nsdecls('w')}>\n"
            f"  <w:tblPr>\n"
            f'    <w:tblW w:type="auto" w:w="0"/>\n'
            f'    <w:tblLook w:firstColumn="1" w:firstRow="1"\n'
            f'               w:lastColumn="0" w:lastRow="0" w:noHBand="0"\n'
            f'               w:noVBand="1" w:val="04A0"/>\n'
            f"  </w:tblPr>\n"
            f"{cls._tblGrid_xml(cols, col_width)}"
            f"{cls._trs_xml(rows, cols, col_width)}"
            f"</w:tbl>\n"
        )

    @classmethod
    def _tblGrid_xml(cls, col_count: int, col_width: Length) -> str:
        xml = "  <w:tblGrid>\n"
        for _ in range(col_count):
            xml += '    <w:gridCol w:w="%d"/>\n' % col_width.twips
        xml += "  </w:tblGrid>\n"
        return xml

    @classmethod
    def _trs_xml(cls, row_count: int, col_count: int, col_width: Length) -> str:
        return f"  <w:tr>\n{cls._tcs_xml(col_count, col_width)}  </w:tr>\n" * row_count

    @classmethod
    def _tcs_xml(cls, col_count: int, col_width: Length) -> str:
        return (
            f"    <w:tc>\n"
            f"      <w:tcPr>\n"
            f'        <w:tcW w:type="dxa" w:w="{col_width.twips}"/>\n'
            f"      </w:tcPr>\n"
            f"      <w:p/>\n"
            f"    </w:tc>\n"
        ) * col_count


class CT_TblGrid(BaseOxmlElement):
    """`w:tblGrid` element.

    Child of `w:tbl`, holds `w:gridCol> elements that define column count, width, etc.
    """

    add_gridCol: Callable[[], CT_TblGridCol]
    gridCol_lst: list[CT_TblGridCol]

    gridCol = ZeroOrMore("w:gridCol", successors=("w:tblGridChange",))


class CT_TblGridCol(BaseOxmlElement):
    """`w:gridCol` element, child of `w:tblGrid`, defines a table column."""

    w: Length | None = OptionalAttribute(  # pyright: ignore[reportAssignmentType]
        "w:w", ST_TwipsMeasure
    )

    @property
    def gridCol_idx(self) -> int:
        """Index of this `w:gridCol` element within its parent `w:tblGrid` element."""
        tblGrid = cast(CT_TblGrid, self.getparent())
        return tblGrid.gridCol_lst.index(self)


class CT_TblLayoutType(BaseOxmlElement):
    """`w:tblLayout` element.

    Specifies whether column widths are fixed or can be automatically adjusted based on
    content.
    """

    type: str | None = OptionalAttribute(  # pyright: ignore[reportAssignmentType]
        "w:type", ST_TblLayoutType
    )


class CT_TblPr(BaseOxmlElement):
    """``<w:tblPr>`` element, child of ``<w:tbl>``, holds child elements that define
    table properties such as style and borders."""

    get_or_add_bidiVisual: Callable[[], CT_OnOff]
    get_or_add_jc: Callable[[], CT_Jc]
    get_or_add_tblLayout: Callable[[], CT_TblLayoutType]
    _add_tblStyle: Callable[[], CT_String]
    _remove_bidiVisual: Callable[[], None]
    _remove_jc: Callable[[], None]
    _remove_tblStyle: Callable[[], None]

    _tag_seq = (
        "w:tblStyle",
        "w:tblpPr",
        "w:tblOverlap",
        "w:bidiVisual",
        "w:tblStyleRowBandSize",
        "w:tblStyleColBandSize",
        "w:tblW",
        "w:jc",
        "w:tblCellSpacing",
        "w:tblInd",
        "w:tblBorders",
        "w:shd",
        "w:tblLayout",
        "w:tblCellMar",
        "w:tblLook",
        "w:tblCaption",
        "w:tblDescription",
        "w:tblPrChange",
    )
    tblStyle: CT_String | None = ZeroOrOne(  # pyright: ignore[reportAssignmentType]
        "w:tblStyle", successors=_tag_seq[1:]
    )
    bidiVisual: CT_OnOff | None = ZeroOrOne(  # pyright: ignore[reportAssignmentType]
        "w:bidiVisual", successors=_tag_seq[4:]
    )
    jc: CT_Jc | None = ZeroOrOne(  # pyright: ignore[reportAssignmentType]
        "w:jc", successors=_tag_seq[8:]
    )
    tblLayout: CT_TblLayoutType | None = ZeroOrOne(  # pyright: ignore[reportAssignmentType]
        "w:tblLayout", successors=_tag_seq[13:]
    )
    del _tag_seq

    @property
    def alignment(self) -> WD_TABLE_ALIGNMENT | None:
        """Horizontal alignment of table, |None| if `./w:jc` is not present."""
        jc = self.jc
        if jc is None:
            return None
        return cast("WD_TABLE_ALIGNMENT | None", jc.val)

    @alignment.setter
    def alignment(self, value: WD_TABLE_ALIGNMENT | None):
        self._remove_jc()
        if value is None:
            return
        jc = self.get_or_add_jc()
        jc.val = cast("WD_ALIGN_PARAGRAPH", value)

    @property
    def autofit(self) -> bool:
        """|False| when there is a `w:tblLayout` child with `@w:type="fixed"`.

        Otherwise |True|.
        """
        tblLayout = self.tblLayout
        return True if tblLayout is None else tblLayout.type != "fixed"

    @autofit.setter
    def autofit(self, value: bool):
        tblLayout = self.get_or_add_tblLayout()
        tblLayout.type = "autofit" if value else "fixed"

    @property
    def style(self):
        """Return the value of the ``val`` attribute of the ``<w:tblStyle>`` child or
        |None| if not present."""
        tblStyle = self.tblStyle
        if tblStyle is None:
            return None
        return tblStyle.val

    @style.setter
    def style(self, value: str | None):
        self._remove_tblStyle()
        if value is None:
            return
        self._add_tblStyle().val = value


class CT_TblPrEx(BaseOxmlElement):
    """`w:tblPrEx` element, exceptions to table-properties.

    Applied at a lower level, like a `w:tr` to modify the appearance. Possibly used when
    two tables are merged. For more see:
    http://officeopenxml.com/WPtablePropertyExceptions.php
    """


class CT_TblWidth(BaseOxmlElement):
    """Used for `w:tblW` and `w:tcW` and others, specifies a table-related width."""

    # the type for `w` attr is actually ST_MeasurementOrPercent, but using
    # XsdInt for now because only dxa (twips) values are being used. It's not
    # entirely clear what the semantics are for other values like -01.4mm
    w: int = RequiredAttribute("w:w", XsdInt)  # pyright: ignore[reportAssignmentType]
    type = RequiredAttribute("w:type", ST_TblWidth)

    @property
    def width(self) -> Length | None:
        """EMU length indicated by the combined `w:w` and `w:type` attrs."""
        if self.type != "dxa":
            return None
        return Twips(self.w)

    @width.setter
    def width(self, value: Length):
        self.type = "dxa"
        self.w = Emu(value).twips


class CT_Tc(BaseOxmlElement):
    """`w:tc` table cell element."""

    add_p: Callable[[], CT_P]
    get_or_add_tcPr: Callable[[], CT_TcPr]
    p_lst: list[CT_P]
    tbl_lst: list[CT_Tbl]
    _insert_tbl: Callable[[CT_Tbl], CT_Tbl]
    _new_p: Callable[[], CT_P]

    # -- tcPr has many successors, `._insert_tcPr()` is overridden below --
    tcPr: CT_TcPr | None = ZeroOrOne("w:tcPr")  # pyright: ignore[reportAssignmentType]
    p = OneOrMore("w:p")
    tbl = OneOrMore("w:tbl")

    @property
    def bottom(self) -> int:
        """The row index that marks the bottom extent of the vertical span of this cell.

        This is one greater than the index of the bottom-most row of the span, similar
        to how a slice of the cell's rows would be specified.
        """
        if self.vMerge is not None:
            tc_below = self._tc_below
            if tc_below is not None and tc_below.vMerge == ST_Merge.CONTINUE:
                return tc_below.bottom
        return self._tr_idx + 1

    def clear_content(self):
        """Remove all content elements, preserving `w:tcPr` element if present.

        Note that this leaves the `w:tc` element in an invalid state because it doesn't
        contain at least one block-level element. It's up to the caller to add a
        `w:p`child element as the last content element.
        """
        # -- remove all cell inner-content except a `w:tcPr` when present. --
        for e in self.xpath("./*[not(self::w:tcPr)]"):
            self.remove(e)

    @property
    def grid_offset(self) -> int:
        """Starting offset of `tc` in the layout-grid columns of its table.

        A cell in the leftmost grid-column has offset 0.
        """
        grid_before = self._tr.grid_before
        preceding_tc_grid_spans = sum(
            tc.grid_span for tc in self.xpath("./preceding-sibling::w:tc")
        )
        return grid_before + preceding_tc_grid_spans

    @property
    def grid_span(self) -> int:
        """The integer number of columns this cell spans.

        Determined by ./w:tcPr/w:gridSpan/@val, it defaults to 1.
        """
        tcPr = self.tcPr
        return 1 if tcPr is None else tcPr.grid_span

    @grid_span.setter
    def grid_span(self, value: int):
        tcPr = self.get_or_add_tcPr()
        tcPr.grid_span = value

    @property
    def inner_content_elements(self) -> list[CT_P | CT_Tbl]:
        """Generate all `w:p` and `w:tbl` elements in this document-body.

        Elements appear in document order. Elements shaded by nesting in a `w:ins` or
        other "wrapper" element will not be included.
        """
        return self.xpath("./w:p | ./w:tbl")

    def iter_block_items(self):
        """Generate a reference to each of the block-level content elements in this
        cell, in the order they appear."""
        block_item_tags = (qn("w:p"), qn("w:tbl"), qn("w:sdt"))
        for child in self:
            if child.tag in block_item_tags:
                yield child

    @property
    def left(self) -> int:
        """The grid column index at which this ``<w:tc>`` element appears."""
        return self.grid_offset

    def merge(self, other_tc: CT_Tc) -> CT_Tc:
        """Return top-left `w:tc` element of a new span.

        Span is formed by merging the rectangular region defined by using this tc
        element and `other_tc` as diagonal corners.
        """
        top, left, height, width = self._span_dimensions(other_tc)
        top_tc = self._tbl.tr_lst[top].tc_at_grid_offset(left)
        top_tc._grow_to(width, height)
        return top_tc

    @classmethod
    def new(cls) -> CT_Tc:
        """A new `w:tc` element, containing an empty paragraph as the required EG_BlockLevelElt."""
        return cast(CT_Tc, parse_xml("<w:tc %s><w:p/></w:tc>" % nsdecls("w")))

    @property
    def right(self) -> int:
        """The grid column index that marks the right-side extent of the horizontal span
        of this cell.

        This is one greater than the index of the right-most column of the span, similar
        to how a slice of the cell's columns would be specified.
        """
        return self.grid_offset + self.grid_span

    @property
    def top(self) -> int:
        """The top-most row index in the vertical span of this cell."""
        if self.vMerge is None or self.vMerge == ST_Merge.RESTART:
            return self._tr_idx
        return self._tc_above.top

    @property
    def vMerge(self) -> str | None:
        """Value of ./w:tcPr/w:vMerge/@val, |None| if w:vMerge is not present."""
        tcPr = self.tcPr
        if tcPr is None:
            return None
        return tcPr.vMerge_val

    @vMerge.setter
    def vMerge(self, value: str | None):
        tcPr = self.get_or_add_tcPr()
        tcPr.vMerge_val = value

    @property
    def width(self) -> Length | None:
        """EMU length represented in `./w:tcPr/w:tcW` or |None| if not present."""
        tcPr = self.tcPr
        if tcPr is None:
            return None
        return tcPr.width

    @width.setter
    def width(self, value: Length):
        tcPr = self.get_or_add_tcPr()
        tcPr.width = value

    def _add_width_of(self, other_tc: CT_Tc):
        """Add the width of `other_tc` to this cell.

        Does nothing if either this tc or `other_tc` does not have a specified width.
        """
        if self.width and other_tc.width:
            self.width = Length(self.width + other_tc.width)

    def _grow_to(self, width: int, height: int, top_tc: CT_Tc | None = None):
        """Grow this cell to `width` grid columns and `height` rows.

        This is accomplished by expanding horizontal spans and creating continuation
        cells to form vertical spans.
        """

        def vMerge_val(top_tc: CT_Tc):
            return (
                ST_Merge.CONTINUE
                if top_tc is not self
                else None
                if height == 1
                else ST_Merge.RESTART
            )

        top_tc = self if top_tc is None else top_tc
        self._span_to_width(width, top_tc, vMerge_val(top_tc))
        if height > 1:
            tc_below = self._tc_below
            assert tc_below is not None
            tc_below._grow_to(width, height - 1, top_tc)

    def _insert_tcPr(self, tcPr: CT_TcPr) -> CT_TcPr:
        """Override default `._insert_tcPr()`."""
        # -- `tcPr`` has a large number of successors, but always comes first if it appears,
        # -- so just using insert(0, ...) rather than spelling out successors.
        self.insert(0, tcPr)
        return tcPr

    @property
    def _is_empty(self) -> bool:
        """True if this cell contains only a single empty `w:p` element."""
        block_items = list(self.iter_block_items())
        if len(block_items) > 1:
            return False
        # -- cell must include at least one block item but can be a `w:tbl`, `w:sdt`,
        # -- `w:customXml` or a `w:p`
        only_item = block_items[0]
        return isinstance(only_item, CT_P) and len(only_item.r_lst) == 0

    def _move_content_to(self, other_tc: CT_Tc):
        """Append the content of this cell to `other_tc`.

        Leaves this cell with a single empty ``<w:p>`` element.
        """
        if other_tc is self:
            return
        if self._is_empty:
            return
        other_tc._remove_trailing_empty_p()
        # -- appending moves each element from self to other_tc --
        for block_element in self.iter_block_items():
            other_tc.append(block_element)
        # -- add back the required minimum single empty <w:p> element --
        self.append(self._new_p())

    def _new_tbl(self) -> None:
        raise NotImplementedError(
            "use CT_Tbl.new_tbl() to add a new table, specifying rows and columns"
        )

    @property
    def _next_tc(self) -> CT_Tc | None:
        """The `w:tc` element immediately following this one in this row, or |None| if
        this is the last `w:tc` element in the row."""
        following_tcs = self.xpath("./following-sibling::w:tc")
        return following_tcs[0] if following_tcs else None

    def _remove(self):
        """Remove this `w:tc` element from the XML tree."""
        parent_element = self.getparent()
        assert parent_element is not None
        parent_element.remove(self)

    def _remove_trailing_empty_p(self):
        """Remove last content element from this cell if it's an empty `w:p` element."""
        block_items = list(self.iter_block_items())
        last_content_elm = block_items[-1]
        if not isinstance(last_content_elm, CT_P):
            return
        p = last_content_elm
        if len(p.r_lst) > 0:
            return
        self.remove(p)

    def _span_dimensions(self, other_tc: CT_Tc) -> tuple[int, int, int, int]:
        """Return a (top, left, height, width) 4-tuple specifying the extents of the
        merged cell formed by using this tc and `other_tc` as opposite corner
        extents."""

        def raise_on_inverted_L(a: CT_Tc, b: CT_Tc):
            if a.top == b.top and a.bottom != b.bottom:
                raise InvalidSpanError("requested span not rectangular")
            if a.left == b.left and a.right != b.right:
                raise InvalidSpanError("requested span not rectangular")

        def raise_on_tee_shaped(a: CT_Tc, b: CT_Tc):
            top_most, other = (a, b) if a.top < b.top else (b, a)
            if top_most.top < other.top and top_most.bottom > other.bottom:
                raise InvalidSpanError("requested span not rectangular")

            left_most, other = (a, b) if a.left < b.left else (b, a)
            if left_most.left < other.left and left_most.right > other.right:
                raise InvalidSpanError("requested span not rectangular")

        raise_on_inverted_L(self, other_tc)
        raise_on_tee_shaped(self, other_tc)

        top = min(self.top, other_tc.top)
        left = min(self.left, other_tc.left)
        bottom = max(self.bottom, other_tc.bottom)
        right = max(self.right, other_tc.right)

        return top, left, bottom - top, right - left

    def _span_to_width(self, grid_width: int, top_tc: CT_Tc, vMerge: str | None):
        """Incorporate `w:tc` elements to the right until this cell spans `grid_width`.

        Incorporated `w:tc` elements are removed (replaced by gridSpan value).

        Raises |ValueError| if `grid_width` cannot be exactly achieved, such as when a
        merged cell would drive the span width greater than `grid_width` or if not
        enough grid columns are available to make this cell that wide. All content from
        incorporated cells is appended to `top_tc`. The val attribute of the vMerge
        element on the single remaining cell is set to `vMerge`. If `vMerge` is |None|,
        the vMerge element is removed if present.
        """
        self._move_content_to(top_tc)
        while self.grid_span < grid_width:
            self._swallow_next_tc(grid_width, top_tc)
        self.vMerge = vMerge

    def _swallow_next_tc(self, grid_width: int, top_tc: CT_Tc):
        """Extend the horizontal span of this `w:tc` element to incorporate the
        following `w:tc` element in the row and then delete that following `w:tc`
        element.

        Any content in the following `w:tc` element is appended to the content of
        `top_tc`. The width of the following `w:tc` element is added to this one, if
        present. Raises |InvalidSpanError| if the width of the resulting cell is greater
        than `grid_width` or if there is no next `<w:tc>` element in the row.
        """

        def raise_on_invalid_swallow(next_tc: CT_Tc | None):
            if next_tc is None:
                raise InvalidSpanError("not enough grid columns")
            if self.grid_span + next_tc.grid_span > grid_width:
                raise InvalidSpanError("span is not rectangular")

        next_tc = self._next_tc
        raise_on_invalid_swallow(next_tc)
        assert next_tc is not None
        next_tc._move_content_to(top_tc)
        self._add_width_of(next_tc)
        self.grid_span += next_tc.grid_span
        next_tc._remove()

    @property
    def _tbl(self) -> CT_Tbl:
        """The tbl element this tc element appears in."""
        return cast(CT_Tbl, self.xpath("./ancestor::w:tbl[position()=1]")[0])

    @property
    def _tc_above(self) -> CT_Tc:
        """The `w:tc` element immediately above this one in its grid column."""
        return self._tr_above.tc_at_grid_offset(self.grid_offset)

    @property
    def _tc_below(self) -> CT_Tc | None:
        """The tc element immediately below this one in its grid column."""
        tr_below = self._tr_below
        if tr_below is None:
            return None
        return tr_below.tc_at_grid_offset(self.grid_offset)

    @property
    def _tr(self) -> CT_Row:
        """The tr element this tc element appears in."""
        return cast(CT_Row, self.xpath("./ancestor::w:tr[position()=1]")[0])

    @property
    def _tr_above(self) -> CT_Row:
        """The tr element prior in sequence to the tr this cell appears in.

        Raises |ValueError| if called on a cell in the top-most row.
        """
        tr_aboves = self.xpath("./ancestor::w:tr[position()=1]/preceding-sibling::w:tr[1]")
        if not tr_aboves:
            raise ValueError("no tr above topmost tr in w:tbl")
        return tr_aboves[0]

    @property
    def _tr_below(self) -> CT_Row | None:
        """The tr element next in sequence after the tr this cell appears in, or |None|
        if this cell appears in the last row."""
        tr_lst = self._tbl.tr_lst
        tr_idx = tr_lst.index(self._tr)
        try:
            return tr_lst[tr_idx + 1]
        except IndexError:
            return None

    @property
    def _tr_idx(self) -> int:
        """The row index of the tr element this tc element appears in."""
        return self._tbl.tr_lst.index(self._tr)


class CT_TcPr(BaseOxmlElement):
    """``<w:tcPr>`` element, defining table cell properties."""

    get_or_add_gridSpan: Callable[[], CT_DecimalNumber]
    get_or_add_tcW: Callable[[], CT_TblWidth]
    get_or_add_vAlign: Callable[[], CT_VerticalJc]
    _add_vMerge: Callable[[], CT_VMerge]
    _remove_gridSpan: Callable[[], None]
    _remove_vAlign: Callable[[], None]
    _remove_vMerge: Callable[[], None]

    _tag_seq = (
        "w:cnfStyle",
        "w:tcW",
        "w:gridSpan",
        "w:hMerge",
        "w:vMerge",
        "w:tcBorders",
        "w:shd",
        "w:noWrap",
        "w:tcMar",
        "w:textDirection",
        "w:tcFitText",
        "w:vAlign",
        "w:hideMark",
        "w:headers",
        "w:cellIns",
        "w:cellDel",
        "w:cellMerge",
        "w:tcPrChange",
    )
    tcW: CT_TblWidth | None = ZeroOrOne(  # pyright: ignore[reportAssignmentType]
        "w:tcW", successors=_tag_seq[2:]
    )
    gridSpan: CT_DecimalNumber | None = ZeroOrOne(  # pyright: ignore[reportAssignmentType]
        "w:gridSpan", successors=_tag_seq[3:]
    )
    vMerge: CT_VMerge | None = ZeroOrOne(  # pyright: ignore[reportAssignmentType]
        "w:vMerge", successors=_tag_seq[5:]
    )
    vAlign: CT_VerticalJc | None = ZeroOrOne(  # pyright: ignore[reportAssignmentType]
        "w:vAlign", successors=_tag_seq[12:]
    )
    del _tag_seq

    @property
    def grid_span(self) -> int:
        """The integer number of columns this cell spans.

        Determined by ./w:gridSpan/@val, it defaults to 1.
        """
        gridSpan = self.gridSpan
        return 1 if gridSpan is None else gridSpan.val

    @grid_span.setter
    def grid_span(self, value: int):
        self._remove_gridSpan()
        if value > 1:
            self.get_or_add_gridSpan().val = value

    @property
    def vAlign_val(self):
        """Value of `w:val` attribute on  `w:vAlign` child.

        Value is |None| if `w:vAlign` child is not present. The `w:val` attribute on
        `w:vAlign` is required.
        """
        vAlign = self.vAlign
        if vAlign is None:
            return None
        return vAlign.val

    @vAlign_val.setter
    def vAlign_val(self, value: WD_CELL_VERTICAL_ALIGNMENT | None):
        if value is None:
            self._remove_vAlign()
            return
        self.get_or_add_vAlign().val = value

    @property
    def vMerge_val(self):
        """The value of the ./w:vMerge/@val attribute, or |None| if the w:vMerge element
        is not present."""
        vMerge = self.vMerge
        if vMerge is None:
            return None
        return vMerge.val

    @vMerge_val.setter
    def vMerge_val(self, value: str | None):
        self._remove_vMerge()
        if value is not None:
            self._add_vMerge().val = value

    @property
    def width(self) -> Length | None:
        """EMU length in `./w:tcW` or |None| if not present or its type is not 'dxa'."""
        tcW = self.tcW
        if tcW is None:
            return None
        return tcW.width

    @width.setter
    def width(self, value: Length):
        tcW = self.get_or_add_tcW()
        tcW.width = value


class CT_TrPr(BaseOxmlElement):
    """``<w:trPr>`` element, defining table row properties."""

    get_or_add_trHeight: Callable[[], CT_Height]

    _tag_seq = (
        "w:cnfStyle",
        "w:divId",
        "w:gridBefore",
        "w:gridAfter",
        "w:wBefore",
        "w:wAfter",
        "w:cantSplit",
        "w:trHeight",
        "w:tblHeader",
        "w:tblCellSpacing",
        "w:jc",
        "w:hidden",
        "w:ins",
        "w:del",
        "w:trPrChange",
    )
    gridAfter: CT_DecimalNumber | None = ZeroOrOne(  # pyright: ignore[reportAssignmentType]
        "w:gridAfter", successors=_tag_seq[4:]
    )
    gridBefore: CT_DecimalNumber | None = ZeroOrOne(  # pyright: ignore[reportAssignmentType]
        "w:gridBefore", successors=_tag_seq[3:]
    )
    trHeight: CT_Height | None = ZeroOrOne(  # pyright: ignore[reportAssignmentType]
        "w:trHeight", successors=_tag_seq[8:]
    )
    del _tag_seq

    @property
    def grid_after(self) -> int:
        """The number of unpopulated layout-grid cells at the end of this row."""
        gridAfter = self.gridAfter
        return 0 if gridAfter is None else gridAfter.val

    @property
    def grid_before(self) -> int:
        """The number of unpopulated layout-grid cells at the start of this row."""
        gridBefore = self.gridBefore
        return 0 if gridBefore is None else gridBefore.val

    @property
    def trHeight_hRule(self) -> WD_ROW_HEIGHT_RULE | None:
        """Return the value of `w:trHeight@w:hRule`, or |None| if not present."""
        trHeight = self.trHeight
        return None if trHeight is None else trHeight.hRule

    @trHeight_hRule.setter
    def trHeight_hRule(self, value: WD_ROW_HEIGHT_RULE | None):
        if value is None and self.trHeight is None:
            return
        trHeight = self.get_or_add_trHeight()
        trHeight.hRule = value

    @property
    def trHeight_val(self):
        """Return the value of `w:trHeight@w:val`, or |None| if not present."""
        trHeight = self.trHeight
        return None if trHeight is None else trHeight.val

    @trHeight_val.setter
    def trHeight_val(self, value: Length | None):
        if value is None and self.trHeight is None:
            return
        trHeight = self.get_or_add_trHeight()
        trHeight.val = value


class CT_VerticalJc(BaseOxmlElement):
    """`w:vAlign` element, specifying vertical alignment of cell."""

    val: WD_CELL_VERTICAL_ALIGNMENT = RequiredAttribute(  # pyright: ignore[reportAssignmentType]
        "w:val", WD_CELL_VERTICAL_ALIGNMENT
    )


class CT_VMerge(BaseOxmlElement):
    """``<w:vMerge>`` element, specifying vertical merging behavior of a cell."""

    val: str | None = OptionalAttribute(  # pyright: ignore[reportAssignmentType]
        "w:val", ST_Merge, default=ST_Merge.CONTINUE
    )
