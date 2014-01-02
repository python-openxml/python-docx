
.. _table_api:

Table objects
================

Table objects are constructed using the ``add_table()`` method on |Document|.

Protocol example::

    table = document.add_table(rows=2, cols=2)
    top_left_cell = table.cell(0, 0)
    top_left_cell.text = 'foobar'

    # OR

    table = document.add_table(rows=1, cols=2)
    table.style = 'LightShading-Accent1'
    header_cells = table.rows[0].cells
    header_cells[0].text = 'Qty'
    header_cells[1].text = 'Desc'
    for item in items:
        row_cells = table.rows.add().cells
        row_cells[0].text = str(item.qty)
        row_cells[2].text = item.desc


.. currentmodule:: docx.table


|Table| objects
---------------

.. autoclass:: Table
   :members:


|_Cell| objects
------------------------

.. autoclass:: _Cell
   :members:


|_Row| objects
--------------

.. autoclass:: _Row
   :members:


|_Column| objects
-----------------

.. autoclass:: _Column
   :members:


|_RowCollection| objects
------------------------

.. autoclass:: _RowCollection
   :members:


|_ColumnCollection| objects
---------------------------

.. autoclass:: _ColumnCollection
   :members:
