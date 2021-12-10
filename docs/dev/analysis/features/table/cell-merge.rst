
Table - Merge Cells
===================

Word allows contiguous table cells to be merged, such that two or more cells
appear to be a single cell. Cells can be merged horizontally (spanning
multple columns) or vertically (spanning multiple rows). Cells can also be
merged both horizontally and vertically at the same time, producing a cell
that spans both rows and columns. Only rectangular ranges of cells can be
merged.


Table diagrams
--------------

Diagrams like the one below are used to depict tables in this analysis.
Horizontal spans are depicted as a continuous horizontal cell without
vertical dividers within the span. Vertical spans are depicted as a vertical
sequence of cells of the same width where continuation cells are separated by
a dashed top border and contain a caret ('^') to symbolize the continuation
of the cell above. Cell 'addresses' are depicted at the column and row grid
lines. This is conceptually convenient as it reuses the notion of list
indices (and slices) and makes certain operations more intuitive to specify.
The merged cell `A` below has top, left, bottom, and right values of 0, 0, 2,
and 2 respectively::

  \ 0   1   2   3
  0 +---+---+---+
    | A     |   |
  1 + - - - +---+
    | ^     |   |
  2 +---+---+---+
    |   |   |   |
  3 +---+---+---+


Basic cell access protocol
--------------------------

There are three ways to access a table cell:

* ``Table.cell(row_idx, col_idx)``
* ``Row.cells[col_idx]``
* ``Column.cells[col_idx]``


Accessing the middle cell of a 3 x 3 table::

    >>> table = document.add_table(3, 3)
    >>> middle_cell = table.cell(1, 1)
    >>> table.rows[1].cells[1] == middle_cell
    True
    >>> table.columns[1].cells[1] == middle_cell
    True


Basic merge protocol
--------------------

A merge is specified using two diagonal cells::

    >>> table = document.add_table(3, 3)
    >>> a = table.cell(0, 0)
    >>> b = table.cell(1, 1)
    >>> A = a.merge(b)

::

    \ 0   1   2   3
    0 +---+---+---+        +---+---+---+
      | a |   |   |        | A     |   |
    1 +---+---+---+        + - - - +---+
      |   | b |   |  -->   | ^     |   |
    2 +---+---+---+        +---+---+---+
      |   |   |   |        |   |   |   |
    3 +---+---+---+        +---+---+---+


Accessing a merged cell
-----------------------

A cell is accessed by its "layout grid" position regardless of any spans that
may be present. A grid address that falls in a span returns the top-leftmost
cell in that span. This means a span has as many addresses as layout grid
cells it spans. For example, the merged cell `A` above can be addressed as
(0, 0), (0, 1), (1, 0), or (1, 1). This addressing scheme leads to desirable
access behaviors when spans are present in the table.

The length of Row.cells is always equal to the number of grid columns,
regardless of any spans that are present. Likewise, the length of
Column.cells is always equal to the number of table rows, regardless of any
spans.

::

    >>> table = document.add_table(2, 3)
    >>> row = table.rows[0]
    >>> len(row.cells)
    3
    >>> row.cells[0] == row.cells[1]
    False

    >>> a, b = row.cells[:2]
    >>> a.merge(b)

    >>> len(row.cells)
    3
    >>> row.cells[0] == row.cells[1]
    True

::

    \ 0   1   2   3
    0 +---+---+---+        +---+---+---+
      | a | b |   |        | A     |   |
    1 +---+---+---+  -->   +---+---+---+
      |   |   |   |        |   |   |   |
    2 +---+---+---+        +---+---+---+


Cell content behavior on merge
------------------------------

When two or more cells are merged, any existing content is concatenated and
placed in the resulting merged cell. Content from each original cell is
separated from that in the prior original cell by a paragraph mark. An
original cell having no content is skipped in the contatenation process. In
Python, the procedure would look roughly like this::

  merged_cell_text = '\n'.join(
      cell.text for cell in original_cells if cell.text
  )

Merging four cells with content ``'a'``, ``'b'``, ``''``, and ``'d'``
respectively results in a merged cell having text ``'a\nb\nd'``.


Cell size behavior on merge
---------------------------

Cell width and height, if present, are added when cells are merged::

    >>> a, b = row.cells[:2]
    >>> a.width.inches, b.width.inches
    (1.0, 1.0)
    >>> A = a.merge(b)
    >>> A.width.inches
    2.0


Removing a redundant row or column
----------------------------------

**Collapsing a column.** When all cells in a grid column share the same
``w:gridSpan`` specification, the spanned columns can be collapsed into
a single column by removing the ``w:gridSpan`` attributes.


Word behavior
-------------

* Row and Column access in the MS API just plain breaks when the table is not
  uniform. `Table.Rows(n)` and `Cell.Row` raise `EnvironmentError` when
  a table contains a vertical span, and `Table.Columns(n)` and `Cell.Column`
  unconditionally raise `EnvironmentError` when the table contains
  a horizontal span. We can do better.

* `Table.Cell(n, m)` works on any non-uniform table, although it uses
  a *visual grid* that greatly complicates access. It raises an error for `n`
  or `m` out of visual range, and provides no way other than try/except to
  determine what that visual range is, since `Row.Count` and `Column.Count`
  are unavailable.

* In a merge operation, the text of the continuation cells is appended to
  that of the origin cell as separate paragraph(s).

* If a merge range contains previously merged cells, the range must
  completely enclose the merged cells.

* Word resizes a table (adds rows) when a cell is referenced by an
  out-of-bounds row index. If the column identifier is out of bounds, an
  exception is raised. This behavior will not be implemented in |docx|.


Glossary
--------

layout grid
    The regular two-dimensional matrix of rows and columns that determines
    the layout of cells in the table. The grid is primarily defined by the
    `w:gridCol` elements that define the layout columns for the table. Each
    row essentially duplicates that layout for an additional row, although
    its height can differ from other rows. Every actual cell in the table
    must begin and end on a layout grid "line", whether the cell is merged or
    not.

span
    The single "combined" cell occupying the area of a set of merged cells.

skipped cell
    The WordprocessingML (WML) spec allows for 'skipped' cells, where
    a layout cell location contains no actual cell. I can't find a way to
    make a table like this using the Word UI and haven't experimented yet to
    see whether Word will load one constructed by hand in the XML.

uniform table
    A table in which each cell corresponds exactly to a layout cell.
    A uniform table contains no spans or skipped cells.

non-uniform table
    A table that contains one or more spans, such that not every cell
    corresponds to a single layout cell. I suppose it would apply when there
    was one or more skipped cells too, but in this analysis the term is only
    used to indicate a table with one or more spans.

uniform cell
    A cell not part of a span, occupying a single cell in the layout grid.

origin cell
    The top-leftmost cell in a span. Contrast with *continuation cell*.

continuation cell
    A layout cell that has been subsumed into a span. A continuation cell is
    mostly an abstract concept, although a actual `w:tc` element will always
    exist in the XML for each continuation cell in a vertical span.


Understanding merge XML intuitively
-----------------------------------

A key insight is that merged cells always look like the diagram below.
Horizontal spans are accomplished with a single `w:tc` element in each row,
using the `gridSpan` attribute to span additional grid columns. Vertical
spans are accomplished with an identical cell in each continuation row,
having the same `gridSpan` value, and having vMerge set to `continue` (the
default). These vertical continuation cells are depicted in the diagrams
below with a dashed top border and a caret ('^') in the left-most grid column
to symbolize the continuation of the cell above.::

  \ 0   1   2   3
  0 +---+---+---+
    | A     |   |
  1 + - - - +---+
    | ^     |   |
  2 +---+---+---+
    |   |   |   |
  3 +---+---+---+

.. highlight:: xml

The table depicted above corresponds to this XML (minimized for clarity)::

  <w:tbl>
    <w:tblGrid>
       <w:gridCol/>
       <w:gridCol/>
       <w:gridCol/>
    </w:tblGrid>
    <w:tr>
       <w:tc>
          <w:tcPr>
             <w:gridSpan w:val="2"/>
             <w:vMerge w:val="restart"/>
          </w:tcPr>
       </w:tc>
       <w:tc/>
    </w:tr>
    <w:tr>
       <w:tc>
          <w:tcPr>
             <w:gridSpan w:val="2"/>
             <w:vMerge/>
          </w:tcPr>
       </w:tc>
       <w:tc/>
    </w:tr>
    <w:tr>
       <w:tc/>
       <w:tc/>
       <w:tc/>
    </w:tr>
  </w:tbl>


XML Semantics
-------------

In a horizontal merge, the ``<w:tc w:gridSpan="?">`` attribute indicates the
number of columns the cell should span. Only the leftmost cell is preserved;
the remaining cells in the merge are deleted.

For merging vertically, the ``w:vMerge`` table cell property of the uppermost
cell of the column is set to the value "restart" of type ``w:ST_Merge``. The
following, lower cells included in the vertical merge must have the
``w:vMerge`` element present in their cell property (``w:TcPr``) element. Its
value should be set to "continue", although it is not necessary to
explicitely define it, as it is the default value. A vertical merge ends as
soon as a cell ``w:TcPr`` element lacks the ``w:vMerge`` element. Similarly
to the ``w:gridSpan`` element, the ``w:vMerge`` elements are only required
when the table's layout is not uniform across its different columns. In the
case it is, only the topmost cell is kept; the other lower cells in the
merged area are deleted along with their ``w:vMerge`` elements and the
``w:trHeight`` table row property is used to specify the combined height of
the merged cells.


len() implementation for Row.cells and Column.cells
---------------------------------------------------

Each ``Row`` and ``Column`` object provides access to the collection of cells
it contains. The length of these cell collections is unaffected by the
presence of merged cells.

`len()` always bases its count on the layout grid, as though there were no
merged cells.

* ``len(Table.columns)`` is the number of `w:gridCol` elements, representing
  the number of grid columns, without regard to the presence of merged cells
  in the table.

* ``len(Table.rows)`` is the number of `w:tr` elements, regardless of any
  merged cells that may be present in the table.

* ``len(Row.cells)`` is the number of grid columns, regardless of whether any
  cells in the row are merged.

* ``len(Column.cells)`` is the number of rows in the table, regardless of
  whether any cells in the column are merged.


Merging a cell already containing a span
----------------------------------------

One or both of the "diagonal corner" cells in a merge operation may itself be
a merged cell, as long as the specified region is rectangular.

For example::

  \   0   1   2   3
    +---+---+---+---+       +---+---+---+---+
  0 | a     | b |   |       | a\nb\nC   |   |
    + - - - +---+---+       + - - - - - +---+
  1 | ^     | C |   |       | ^         |   |
    +---+---+---+---+  -->  +---+---+---+---+
  2 |   |   |   |   |       |   |   |   |   |
    +---+---+---+---+       +---+---+---+---+
  3 |   |   |   |   |       |   |   |   |   |
    +---+---+---+---+       +---+---+---+---+

    cell(0, 0).merge(cell(1, 2))

or::

       0   1   2   3   4
     +---+---+---+---+---+       +---+---+---+---+---+
   0 | a     | b | c |   |       | abcD          |   |
     + - - - +---+---+---+       + - - - - - - - +---+
   1 | ^     | D     |   |       | ^             |   |
     +---+---+---+---+---+  -->  +---+---+---+---+---+
   2 |   |   |   |   |   |       |   |   |   |   |   |
     +---+ - - - +---+---+       +---+---+---+---+---+
   3 |   |   |   |   |   |       |   |   |   |   |   |
     +---+---+---+---+---+       +---+---+---+---+---+

     cell(0, 0).merge(cell(1, 2))


Conversely, either of these two merge operations would be illegal::

    \ 0   1   2   3   4      0   1   2   3   4
    0 +---+---+---+---+    0 +---+---+---+---+
      |   |   | b |   |      |   |   |   |   |
    1 +---+---+ - +---+    1 +---+---+---+---+
      |   | a | ^ |   |      |   | a |   |   |
    2 +---+---+ - +---+    2 +---+---+---+---+
      |   |   | ^ |   |      | b         |   |
    3 +---+---+---+---+    3 +---+---+---+---+
      |   |   |   |   |      |   |   |   |   |
    4 +---+---+---+---+    4 +---+---+---+---+

      a.merge(b)


General algorithm
~~~~~~~~~~~~~~~~~

* find top-left and target width, height
* for each tr in target height, tc.grow_right(target_width)


Specimen XML
------------

.. highlight:: xml

A 3 x 3 table where an area defined by the 2 x 2 topleft cells has been
merged, demonstrating the combined use of the ``w:gridSpan`` as well as the
``w:vMerge`` elements, as produced by Word::

  <w:tbl>
    <w:tblPr>
       <w:tblW w:w="0" w:type="auto" />
    </w:tblPr>
    <w:tblGrid>
       <w:gridCol w:w="3192" />
       <w:gridCol w:w="3192" />
       <w:gridCol w:w="3192" />
    </w:tblGrid>
    <w:tr>
       <w:tc>
          <w:tcPr>
             <w:tcW w:w="6384" w:type="dxa" />
             <w:gridSpan w:val="2" />
             <w:vMerge w:val="restart" />
          </w:tcPr>
       </w:tc>
       <w:tc>
          <w:tcPr>
             <w:tcW w:w="3192" w:type="dxa" />
          </w:tcPr>
       </w:tc>
    </w:tr>
    <w:tr>
       <w:tc>
          <w:tcPr>
             <w:tcW w:w="6384" w:type="dxa" />
             <w:gridSpan w:val="2" />
             <w:vMerge />
          </w:tcPr>
       </w:tc>
       <w:tc>
          <w:tcPr>
             <w:tcW w:w="3192" w:type="dxa" />
          </w:tcPr>
       </w:tc>
    </w:tr>
    <w:tr>
       <w:tc>
          <w:tcPr>
             <w:tcW w:w="3192" w:type="dxa" />
          </w:tcPr>
       </w:tc>
       <w:tc>
          <w:tcPr>
             <w:tcW w:w="3192" w:type="dxa" />
          </w:tcPr>
       </w:tc>
       <w:tc>
          <w:tcPr>
             <w:tcW w:w="3192" w:type="dxa" />
          </w:tcPr>
       </w:tc>
    </w:tr>
  </w:tbl>


Schema excerpt
--------------

.. highlight:: xml

::

  <xsd:complexType name="CT_Tc">  <!-- denormalized -->
    <xsd:sequence>
      <xsd:element name="tcPr" type="CT_TcPr" minOccurs="0"/>
      <xsd:choice minOccurs="1" maxOccurs="unbounded">
        <xsd:element name="p"                           type="CT_P"/>
        <xsd:element name="tbl"                         type="CT_Tbl"/>
        <xsd:element name="customXml"                   type="CT_CustomXmlBlock"/>
        <xsd:element name="sdt"                         type="CT_SdtBlock"/>
        <xsd:element name="proofErr"                    type="CT_ProofErr"/>
        <xsd:element name="permStart"                   type="CT_PermStart"/>
        <xsd:element name="permEnd"                     type="CT_Perm"/>
        <xsd:element name="ins"                         type="CT_RunTrackChange"/>
        <xsd:element name="del"                         type="CT_RunTrackChange"/>
        <xsd:element name="moveFrom"                    type="CT_RunTrackChange"/>
        <xsd:element name="moveTo"                      type="CT_RunTrackChange"/>
        <xsd:element  ref="m:oMathPara"                 type="CT_OMathPara"/>
        <xsd:element  ref="m:oMath"                     type="CT_OMath"/>
        <xsd:element name="bookmarkStart"               type="CT_Bookmark"/>
        <xsd:element name="bookmarkEnd"                 type="CT_MarkupRange"/>
        <xsd:element name="moveFromRangeStart"          type="CT_MoveBookmark"/>
        <xsd:element name="moveFromRangeEnd"            type="CT_MarkupRange"/>
        <xsd:element name="moveToRangeStart"            type="CT_MoveBookmark"/>
        <xsd:element name="moveToRangeEnd"              type="CT_MarkupRange"/>
        <xsd:element name="commentRangeStart"           type="CT_MarkupRange"/>
        <xsd:element name="commentRangeEnd"             type="CT_MarkupRange"/>
        <xsd:element name="customXmlInsRangeStart"      type="CT_TrackChange"/>
        <xsd:element name="customXmlInsRangeEnd"        type="CT_Markup"/>
        <xsd:element name="customXmlDelRangeStart"      type="CT_TrackChange"/>
        <xsd:element name="customXmlDelRangeEnd"        type="CT_Markup"/>
        <xsd:element name="customXmlMoveFromRangeStart" type="CT_TrackChange"/>
        <xsd:element name="customXmlMoveFromRangeEnd"   type="CT_Markup"/>
        <xsd:element name="customXmlMoveToRangeStart"   type="CT_TrackChange"/>
        <xsd:element name="customXmlMoveToRangeEnd"     type="CT_Markup"/>
        <xsd:element name="altChunk"                    type="CT_AltChunk"/>
      </xsd:choice>
    </xsd:sequence>
    <xsd:attribute name="id" type="s:ST_String" use="optional"/>
  </xsd:complexType>

  <xsd:complexType name="CT_TcPr">  <!-- denormalized -->
    <xsd:sequence>
      <xsd:element name="cnfStyle"             type="CT_Cnf"           minOccurs="0"/>
      <xsd:element name="tcW"                  type="CT_TblWidth"      minOccurs="0"/>
      <xsd:element name="gridSpan"             type="CT_DecimalNumber" minOccurs="0"/>
      <xsd:element name="hMerge"               type="CT_HMerge"        minOccurs="0"/>
      <xsd:element name="vMerge"               type="CT_VMerge"        minOccurs="0"/>
      <xsd:element name="tcBorders"            type="CT_TcBorders"     minOccurs="0"/>
      <xsd:element name="shd"                  type="CT_Shd"           minOccurs="0"/>
      <xsd:element name="noWrap"               type="CT_OnOff"         minOccurs="0"/>
      <xsd:element name="tcMar"                type="CT_TcMar"         minOccurs="0"/>
      <xsd:element name="textDirection"        type="CT_TextDirection" minOccurs="0"/>
      <xsd:element name="tcFitText"            type="CT_OnOff"         minOccurs="0"/>
      <xsd:element name="vAlign"               type="CT_VerticalJc"    minOccurs="0"/>
      <xsd:element name="hideMark"             type="CT_OnOff"         minOccurs="0"/>
      <xsd:element name="headers"              type="CT_Headers"       minOccurs="0"/>
      <xsd:choice  minOccurs="0">
        <xsd:element name="cellIns"            type="CT_TrackChange"/>
        <xsd:element name="cellDel"            type="CT_TrackChange"/>
        <xsd:element name="cellMerge"          type="CT_CellMergeTrackChange"/>
      </xsd:choice>
      <xsd:element name="tcPrChange"           type="CT_TcPrChange"    minOccurs="0"/>
    </xsd:sequence>
  </xsd:complexType>

  <xsd:complexType name="CT_DecimalNumber">
    <xsd:attribute name="val" type="ST_DecimalNumber" use="required"/>
  </xsd:complexType>

  <xsd:simpleType name="ST_DecimalNumber">
     <xsd:restriction base="xsd:integer"/>
  </xsd:simpleType>

  <xsd:complexType name="CT_VMerge">
    <xsd:attribute name="val" type="ST_Merge"/>
  </xsd:complexType>

  <xsd:complexType name="CT_HMerge">
    <xsd:attribute name="val" type="ST_Merge"/>
  </xsd:complexType>

  <xsd:simpleType name="ST_Merge">
    <xsd:restriction base="xsd:string">
      <xsd:enumeration value="continue"/>
      <xsd:enumeration value="restart"/>
    </xsd:restriction>
  </xsd:simpleType>


Open Issues
-----------

* Does Word allow "skipped" cells at the beginning of a row (`w:gridBefore`
  element)? These are described in the spec, but I don't see a way in the
  Word UI to create such a table.


Ressources
----------

* `Cell.Merge Method on MSDN`_

.. _`Cell.Merge Method on MSDN`:
   http://msdn.microsoft.com/en-us/library/office/ff821310%28v=office.15%29.aspx

Relevant sections in the ISO Spec
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
* 17.4.17 gridSpan (Grid Columns Spanned by Current Table Cell)
* 17.4.84 vMerge (Vertically Merged Cell)
* 17.18.57 ST_Merge (Merged Cell Type)
