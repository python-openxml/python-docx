"""The |Table| object and related proxy classes."""

from __future__ import annotations

from typing import TYPE_CHECKING, Iterator, cast, overload

from typing_extensions import TypeAlias

from docx.blkcntnr import BlockItemContainer
from docx.enum.style import WD_STYLE_TYPE
from docx.enum.table import WD_CELL_VERTICAL_ALIGNMENT
from docx.oxml.simpletypes import ST_Merge
from docx.oxml.table import CT_TblGridCol
from docx.shared import Inches, Parented, StoryChild, lazyproperty

if TYPE_CHECKING:
    import docx.types as t
    from docx.enum.table import WD_ROW_HEIGHT_RULE, WD_TABLE_ALIGNMENT, WD_TABLE_DIRECTION
    from docx.oxml.table import CT_Row, CT_Tbl, CT_TblPr, CT_Tc
    from docx.shared import Length
    from docx.styles.style import (
        ParagraphStyle,
        _TableStyle,  # pyright: ignore[reportPrivateUsage]
    )

TableParent: TypeAlias = "Table | _Columns | _Rows"


class Table(StoryChild):
    """Proxy class for a WordprocessingML ``<w:tbl>`` element."""

    def __init__(self, tbl: CT_Tbl, parent: t.ProvidesStoryPart):
        super(Table, self).__init__(parent)
        self._element = tbl
        self._tbl = tbl

    def add_column(self, width: Length):
        """Return a |_Column| object of `width`, newly added rightmost to the table."""
        tblGrid = self._tbl.tblGrid
        gridCol = tblGrid.add_gridCol()
        gridCol.w = width
        for tr in self._tbl.tr_lst:
            tc = tr.add_tc()
            tc.width = width
        return _Column(gridCol, self)

    def add_row(self):
        """Return a |_Row| instance, newly added bottom-most to the table."""
        tbl = self._tbl
        tr = tbl.add_tr()
        for gridCol in tbl.tblGrid.gridCol_lst:
            tc = tr.add_tc()
            if gridCol.w is not None:
                tc.width = gridCol.w
        return _Row(tr, self)

    @property
    def alignment(self) -> WD_TABLE_ALIGNMENT | None:
        """Read/write.

        A member of :ref:`WdRowAlignment` or None, specifying the positioning of this
        table between the page margins. |None| if no setting is specified, causing the
        effective value to be inherited from the style hierarchy.
        """
        return self._tblPr.alignment

    @alignment.setter
    def alignment(self, value: WD_TABLE_ALIGNMENT | None):
        self._tblPr.alignment = value

    @property
    def autofit(self) -> bool:
        """|True| if column widths can be automatically adjusted to improve the fit of
        cell contents.

        |False| if table layout is fixed. Column widths are adjusted in either case if
        total column width exceeds page width. Read/write boolean.
        """
        return self._tblPr.autofit

    @autofit.setter
    def autofit(self, value: bool):
        self._tblPr.autofit = value

    def cell(self, row_idx: int, col_idx: int) -> _Cell:
        """|_Cell| at `row_idx`, `col_idx` intersection.

        (0, 0) is the top, left-most cell.
        """
        cell_idx = col_idx + (row_idx * self._column_count)
        return self._cells[cell_idx]

    def column_cells(self, column_idx: int) -> list[_Cell]:
        """Sequence of cells in the column at `column_idx` in this table."""
        cells = self._cells
        idxs = range(column_idx, len(cells), self._column_count)
        return [cells[idx] for idx in idxs]

    @lazyproperty
    def columns(self):
        """|_Columns| instance representing the sequence of columns in this table."""
        return _Columns(self._tbl, self)

    def row_cells(self, row_idx: int) -> list[_Cell]:
        """DEPRECATED: Use `table.rows[row_idx].cells` instead.

        Sequence of cells in the row at `row_idx` in this table.
        """
        column_count = self._column_count
        start = row_idx * column_count
        end = start + column_count
        return self._cells[start:end]

    @lazyproperty
    def rows(self) -> _Rows:
        """|_Rows| instance containing the sequence of rows in this table."""
        return _Rows(self._tbl, self)

    @property
    def style(self) -> _TableStyle | None:
        """|_TableStyle| object representing the style applied to this table.

        Read/write. The default table style for the document (often `Normal Table`) is
        returned if the table has no directly-applied style. Assigning |None| to this
        property removes any directly-applied table style causing it to inherit the
        default table style of the document.

        Note that the style name of a table style differs slightly from that displayed
        in the user interface; a hyphen, if it appears, must be removed. For example,
        `Light Shading - Accent 1` becomes `Light Shading Accent 1`.
        """
        style_id = self._tbl.tblStyle_val
        return cast("_TableStyle | None", self.part.get_style(style_id, WD_STYLE_TYPE.TABLE))

    @style.setter
    def style(self, style_or_name: _TableStyle | str | None):
        style_id = self.part.get_style_id(style_or_name, WD_STYLE_TYPE.TABLE)
        self._tbl.tblStyle_val = style_id

    @property
    def table(self):
        """Provide child objects with reference to the |Table| object they belong to,
        without them having to know their direct parent is a |Table| object.

        This is the terminus of a series of `parent._table` calls from an arbitrary
        child through its ancestors.
        """
        return self

    @property
    def table_direction(self) -> WD_TABLE_DIRECTION | None:
        """Member of :ref:`WdTableDirection` indicating cell-ordering direction.

        For example: `WD_TABLE_DIRECTION.LTR`. |None| indicates the value is inherited
        from the style hierarchy.
        """
        return cast("WD_TABLE_DIRECTION | None", self._tbl.bidiVisual_val)

    @table_direction.setter
    def table_direction(self, value: WD_TABLE_DIRECTION | None):
        self._element.bidiVisual_val = value

    @property
    def _cells(self) -> list[_Cell]:
        """A sequence of |_Cell| objects, one for each cell of the layout grid.

        If the table contains a span, one or more |_Cell| object references are
        repeated.
        """
        col_count = self._column_count
        cells: list[_Cell] = []
        for tc in self._tbl.iter_tcs():
            for grid_span_idx in range(tc.grid_span):
                if tc.vMerge == ST_Merge.CONTINUE:
                    cells.append(cells[-col_count])
                elif grid_span_idx > 0:
                    cells.append(cells[-1])
                else:
                    cells.append(_Cell(tc, self))
        return cells

    @property
    def _column_count(self):
        """The number of grid columns in this table."""
        return self._tbl.col_count

    @property
    def _tblPr(self) -> CT_TblPr:
        return self._tbl.tblPr


class _Cell(BlockItemContainer):
    """Table cell."""

    def __init__(self, tc: CT_Tc, parent: TableParent):
        super(_Cell, self).__init__(tc, cast("t.ProvidesStoryPart", parent))
        self._parent = parent
        self._tc = self._element = tc

    def add_paragraph(self, text: str = "", style: str | ParagraphStyle | None = None):
        """Return a paragraph newly added to the end of the content in this cell.

        If present, `text` is added to the paragraph in a single run. If specified, the
        paragraph style `style` is applied. If `style` is not specified or is |None|,
        the result is as though the 'Normal' style was applied. Note that the formatting
        of text in a cell can be influenced by the table style. `text` can contain tab
        (``\\t``) characters, which are converted to the appropriate XML form for a tab.
        `text` can also include newline (``\\n``) or carriage return (``\\r``)
        characters, each of which is converted to a line break.
        """
        return super(_Cell, self).add_paragraph(text, style)

    def add_table(  # pyright: ignore[reportIncompatibleMethodOverride]
        self, rows: int, cols: int
    ) -> Table:
        """Return a table newly added to this cell after any existing cell content.

        The new table will have `rows` rows and `cols` columns.

        An empty paragraph is added after the table because Word requires a paragraph
        element as the last element in every cell.
        """
        width = self.width if self.width is not None else Inches(1)
        table = super(_Cell, self).add_table(rows, cols, width)
        self.add_paragraph()
        return table

    @property
    def grid_span(self) -> int:
        """Number of layout-grid cells this cell spans horizontally.

        A "normal" cell has a grid-span of 1. A horizontally merged cell has a grid-span of 2 or
        more.
        """
        return self._tc.grid_span

    def merge(self, other_cell: _Cell):
        """Return a merged cell created by spanning the rectangular region having this
        cell and `other_cell` as diagonal corners.

        Raises |InvalidSpanError| if the cells do not define a rectangular region.
        """
        tc, tc_2 = self._tc, other_cell._tc
        merged_tc = tc.merge(tc_2)
        return _Cell(merged_tc, self._parent)

    @property
    def paragraphs(self):
        """List of paragraphs in the cell.

        A table cell is required to contain at least one block-level element and end
        with a paragraph. By default, a new cell contains a single paragraph. Read-only
        """
        return super(_Cell, self).paragraphs

    @property
    def tables(self):
        """List of tables in the cell, in the order they appear.

        Read-only.
        """
        return super(_Cell, self).tables

    @property
    def text(self) -> str:
        """The entire contents of this cell as a string of text.

        Assigning a string to this property replaces all existing content with a single
        paragraph containing the assigned text in a single run.
        """
        return "\n".join(p.text for p in self.paragraphs)

    @text.setter
    def text(self, text: str):
        """Write-only.

        Set entire contents of cell to the string `text`. Any existing content or
        revisions are replaced.
        """
        tc = self._tc
        tc.clear_content()
        p = tc.add_p()
        r = p.add_r()
        r.text = text

    @property
    def vertical_alignment(self):
        """Member of :ref:`WdCellVerticalAlignment` or None.

        A value of |None| indicates vertical alignment for this cell is inherited.
        Assigning |None| causes any explicitly defined vertical alignment to be removed,
        restoring inheritance.
        """
        tcPr = self._element.tcPr
        if tcPr is None:
            return None
        return tcPr.vAlign_val

    @vertical_alignment.setter
    def vertical_alignment(self, value: WD_CELL_VERTICAL_ALIGNMENT | None):
        tcPr = self._element.get_or_add_tcPr()
        tcPr.vAlign_val = value

    @property
    def width(self):
        """The width of this cell in EMU, or |None| if no explicit width is set."""
        return self._tc.width

    @width.setter
    def width(self, value: Length):
        self._tc.width = value


class _Column(Parented):
    """Table column."""

    def __init__(self, gridCol: CT_TblGridCol, parent: TableParent):
        super(_Column, self).__init__(parent)
        self._parent = parent
        self._gridCol = gridCol

    @property
    def cells(self) -> tuple[_Cell, ...]:
        """Sequence of |_Cell| instances corresponding to cells in this column."""
        return tuple(self.table.column_cells(self._index))

    @property
    def table(self) -> Table:
        """Reference to the |Table| object this column belongs to."""
        return self._parent.table

    @property
    def width(self) -> Length | None:
        """The width of this column in EMU, or |None| if no explicit width is set."""
        return self._gridCol.w

    @width.setter
    def width(self, value: Length | None):
        self._gridCol.w = value

    @property
    def _index(self):
        """Index of this column in its table, starting from zero."""
        return self._gridCol.gridCol_idx


class _Columns(Parented):
    """Sequence of |_Column| instances corresponding to the columns in a table.

    Supports ``len()``, iteration and indexed access.
    """

    def __init__(self, tbl: CT_Tbl, parent: TableParent):
        super(_Columns, self).__init__(parent)
        self._parent = parent
        self._tbl = tbl

    def __getitem__(self, idx: int):
        """Provide indexed access, e.g. 'columns[0]'."""
        try:
            gridCol = self._gridCol_lst[idx]
        except IndexError:
            msg = "column index [%d] is out of range" % idx
            raise IndexError(msg)
        return _Column(gridCol, self)

    def __iter__(self):
        for gridCol in self._gridCol_lst:
            yield _Column(gridCol, self)

    def __len__(self):
        return len(self._gridCol_lst)

    @property
    def table(self) -> Table:
        """Reference to the |Table| object this column collection belongs to."""
        return self._parent.table

    @property
    def _gridCol_lst(self):
        """Sequence containing ``<w:gridCol>`` elements for this table, each
        representing a table column."""
        tblGrid = self._tbl.tblGrid
        return tblGrid.gridCol_lst


class _Row(Parented):
    """Table row."""

    def __init__(self, tr: CT_Row, parent: TableParent):
        super(_Row, self).__init__(parent)
        self._parent = parent
        self._tr = self._element = tr

    @property
    def cells(self) -> tuple[_Cell, ...]:
        """Sequence of |_Cell| instances corresponding to cells in this row.

        Note that Word allows table rows to start later than the first column and end before the
        last column.

        - Only cells actually present are included in the return value.
        - This implies the length of this cell sequence may differ between rows of the same table.
        - If you are reading the cells from each row to form a rectangular "matrix" data structure
          of the table cell values, you will need to account for empty leading and/or trailing
          layout-grid positions using `.grid_cols_before` and `.grid_cols_after`.

        """

        def iter_tc_cells(tc: CT_Tc) -> Iterator[_Cell]:
            """Generate a cell object for each layout-grid cell in `tc`.

            In particular, a `<w:tc>` element with a horizontal "span" with generate the same cell
            multiple times, one for each grid-cell being spanned. This approximates a row in a
            "uniform" table, where each row has a cell for each column in the table.
            """
            # -- a cell comprising the second or later row of a vertical span is indicated by
            # -- tc.vMerge="continue" (the default value of the `w:vMerge` attribute, when it is
            # -- present in the XML). The `w:tc` element at the same grid-offset in the prior row
            # -- is guaranteed to be the same width (gridSpan). So we can delegate content
            # -- discovery to that prior-row `w:tc` element (recursively) until we arrive at the
            # -- "root" cell -- for the vertical span.
            if tc.vMerge == "continue":
                yield from iter_tc_cells(tc._tc_above)  # pyright: ignore[reportPrivateUsage]
                return

            # -- Otherwise, vMerge is either "restart" or None, meaning this `tc` holds the actual
            # -- content of the cell (whether it is vertically merged or not).
            cell = _Cell(tc, self.table)
            for _ in range(tc.grid_span):
                yield cell

        def _iter_row_cells() -> Iterator[_Cell]:
            """Generate `_Cell` instance for each populated layout-grid cell in this row."""
            for tc in self._tr.tc_lst:
                yield from iter_tc_cells(tc)

        return tuple(_iter_row_cells())

    @property
    def grid_cols_after(self) -> int:
        """Count of unpopulated grid-columns after the last cell in this row.

        Word allows a row to "end early", meaning that one or more cells are not present at the
        end of that row.

        Note these are not simply "empty" cells. The renderer reads this value and "skips" this
        many columns after drawing the last cell.

        Note this also implies that not all rows are guaranteed to have the same number of cells,
        e.g. `_Row.cells` could have length `n` for one row and `n - m` for the next row in the same
        table. Visually this appears as a column (at the beginning or end, not in the middle) with
        one or more cells missing.
        """
        return self._tr.grid_after

    @property
    def grid_cols_before(self) -> int:
        """Count of unpopulated grid-columns before the first cell in this row.

        Word allows a row to "start late", meaning that one or more cells are not present at the
        beginning of that row.

        Note these are not simply "empty" cells. The renderer reads this value and skips forward to
        the table layout-grid position of the first cell in this row; the renderer "skips" this many
        columns before drawing the first cell.

        Note this also implies that not all rows are guaranteed to have the same number of cells,
        e.g. `_Row.cells` could have length `n` for one row and `n - m` for the next row in the same
        table.
        """
        return self._tr.grid_before

    @property
    def height(self) -> Length | None:
        """Return a |Length| object representing the height of this cell, or |None| if
        no explicit height is set."""
        return self._tr.trHeight_val

    @height.setter
    def height(self, value: Length | None):
        self._tr.trHeight_val = value

    @property
    def height_rule(self) -> WD_ROW_HEIGHT_RULE | None:
        """Return the height rule of this cell as a member of the :ref:`WdRowHeightRule`.

        This value is |None| if no explicit height_rule is set.
        """
        return self._tr.trHeight_hRule

    @height_rule.setter
    def height_rule(self, value: WD_ROW_HEIGHT_RULE | None):
        self._tr.trHeight_hRule = value

    @property
    def table(self) -> Table:
        """Reference to the |Table| object this row belongs to."""
        return self._parent.table

    @property
    def _index(self) -> int:
        """Index of this row in its table, starting from zero."""
        return self._tr.tr_idx


class _Rows(Parented):
    """Sequence of |_Row| objects corresponding to the rows in a table.

    Supports ``len()``, iteration, indexed access, and slicing.
    """

    def __init__(self, tbl: CT_Tbl, parent: TableParent):
        super(_Rows, self).__init__(parent)
        self._parent = parent
        self._tbl = tbl

    @overload
    def __getitem__(self, idx: int) -> _Row: ...

    @overload
    def __getitem__(self, idx: slice) -> list[_Row]: ...

    def __getitem__(self, idx: int | slice) -> _Row | list[_Row]:
        """Provide indexed access, (e.g. `rows[0]` or `rows[1:3]`)"""
        return list(self)[idx]

    def __iter__(self):
        return (_Row(tr, self) for tr in self._tbl.tr_lst)

    def __len__(self):
        return len(self._tbl.tr_lst)

    @property
    def table(self) -> Table:
        """Reference to the |Table| object this row collection belongs to."""
        return self._parent.table
