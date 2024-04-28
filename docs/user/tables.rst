.. _tables:

Working with Tables
===================

Word provides sophisticated capabilities to create tables. As usual, this power comes with
additional conceptual complexity.

This complexity becomes most apparent when *reading* tables, in particular from documents drawn from
the wild where there is limited or no prior knowledge as to what the tables might contain or how
they might be structured.

These are some of the important concepts you'll need to understand.


Concept: Simple (uniform) tables
--------------------------------

::

  +---+---+---+
  | a | b | c |
  +---+---+---+
  | d | e | f |
  +---+---+---+
  | g | h | i |
  +---+---+---+

The basic concept of a table is intuitive enough. You have *rows* and *columns*, and at each (row,
column) position is a different *cell*. It can be described as a *grid* or a *matrix*. Let's call
this concept a *uniform table*. A relational database table and a Pandas dataframe are both examples
of a uniform table.

The following invariants apply to uniform tables:

* Each row has the same number of cells, one for each column.
* Each column has the same number of cells, one for each row.


Complication 1: Merged Cells
----------------------------

::

  +---+---+---+   +---+---+---+
  |   a   | b |   |   | b | c |
  +---+---+---+   + a +---+---+
  | c | d | e |   |   | d | e |
  +---+---+---+   +---+---+---+
  | f | g | h |   | f | g | h |
  +---+---+---+   +---+---+---+

While very suitable for data processing, a uniform table lacks expressive power desireable for
tables intended for a human reader.

Perhaps the most important characteristic a uniform table lacks is *merged cells*. It is very common
to want to group multiple cells into one, for example to form a column-group heading or provide the
same value for a sequence of cells rather than repeat it for each cell. These make a rendered table
more *readable* by reducing the cognitive load on the human reader and make certain relationships
explicit that might easily be missed otherwise.

Unfortunately, accommodating merged cells breaks both the invariants of a uniform table:

* Each row can have a different number of cells.
* Each column can have a different number of cells.

This challenges reading table contents programatically. One might naturally want to read the table
into a uniform matrix data structure like a 3 x 3 "2D array" (list of lists perhaps), but this is
not directly possible when the table is not known to be uniform.


Concept: The layout grid
------------------------

::

  + - + - + - +
  |   |   |   |
  + - + - + - +
  |   |   |   |
  + - + - + - +
  |   |   |   |
  + - + - + - +

In Word, each table has a *layout grid*.

- The layout grid is *uniform*. There is a layout position for every (layout-row, layout-column)
  pair.
- The layout grid itself is not visible. However it is represented and referenced by certain
  elements and attributes within the table XML
- Each table cell is located at a layout-grid position; i.e. the top-left corner of each cell is the
  top-left corner of a layout-grid cell.
- Each table cell occupies one or more whole layout-grid cells. A merged cell will occupy multiple
  layout-grid cells. No table cell can occupy a partial layout-grid cell.
- Another way of saying this is that every vertical boundary (left and right) of a cell aligns with
  a layout-grid vertical boundary, likewise for horizontal boundaries. But not all layout-grid
  boundaries need be occupied by a cell boundary of the table.


Complication 2: Omitted Cells
-----------------------------

::

      +---+---+   +---+---+---+
      | a | b |   | a | b | c |
  +---+---+---+   +---+---+---+
  | c | d |           | d |
  +---+---+       +---+---+---+
      | e |       | e | f | g |
      +---+       +---+---+---+

Word is unusual in that it allows cells to be omitted from the beginning or end (but not the middle)
of a row. A typical practical example is a table with both a row of column headings and a column of
row headings, but no top-left cell (position 0, 0), such as this XOR truth table.

::

      +---+---+
      | T | F |
  +---+---+---+
  | T | F | T |
  +---+---+---+
  | F | T | F |
  +---+---+---+

In `python-docx`, omitted cells in a |_Row| object are represented by the ``.grid_cols_before`` and
``.grid_cols_after`` properties. In the example above, for the first row, ``.grid_cols_before``
would equal ``1`` and ``.grid_cols_after`` would equal ``0``.

Note that omitted cells are not just "empty" cells. They represent layout-grid positions that are
unoccupied by a cell and they cannot be represented by a |_Cell| object. This distinction becomes
important when trying to produce a uniform representation (e.g. a 2D array) for an arbitrary Word
table.


Concept: `python-docx` approximates uniform tables by default
-------------------------------------------------------------

To accurately represent an arbitrary table would require a complex graph data structure. Navigating
this data structure would be at least as complex as navigating the `python-docx` object graph for a
table. When extracting content from a collection of arbitrary Word files, such as for indexing the
document, it is common to choose a simpler data structure and *approximate* the table in that
structure.

Reflecting on how a relational table or dataframe represents tabular information, a straightforward
approximation would simply repeat merged-cell values for each layout-grid cell occupied by the
merged cell::


  +---+---+---+      +---+---+---+
  |   a   | b |  ->  | a | a | b |
  +---+---+---+      +---+---+---+
  |   | d | e |  ->  | c | d | e |
  + c +---+---+      +---+---+---+
  |   | f | g |  ->  | c | f | g |
  +---+---+---+      +---+---+---+

This is what ``_Row.cells`` does by default. Conceptually::

  >>> [tuple(c.text for c in r.cells) for r in table.rows]
  [
    (a, a, b),
    (c, d, e),
    (c, f, g),
  ]

Note this only produces a uniform "matrix" of cells when there are no omitted cells. Dealing with
omitted cells requires a more sophisticated approach when maintaining column integrity is required::

  #     +---+---+
  #     | a | b |
  # +---+---+---+
  # | c | d |
  # +---+---+
  #     | e |
  #     +---+

  def iter_row_cell_texts(row: _Row) -> Iterator[str]:
      for _ in range(row.grid_cols_before):
          yield ""
      for c in row.cells:
          yield c.text
      for _ in range(row.grid_cols_after):
          yield ""

  >>> [tuple(iter_row_cell_texts(r)) for r in table.rows]
  [
    ("",  "a", "b"),
    ("c", "d", ""),
    ("",  "e", ""),
  ]


Complication 3: Tables are Recursive
------------------------------------

Further complicating table processing is their recursive nature. In Word, as in HTML, a table cell
can itself include one or more tables.

These can be detected using ``_Cell.tables`` or ``_Cell.iter_inner_content()``. The latter preserves
the document order of the table with respect to paragraphs also in the cell.
