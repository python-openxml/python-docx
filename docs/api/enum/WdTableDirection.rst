.. _WdTableDirection:

``WD_TABLE_DIRECTION``
======================

Specifies the direction in which an application orders cells in the
specified table or row.

Example::

    from docx.enum.table import WD_TABLE_DIRECTION

    table = document.add_table(3, 3)
    table.direction = WD_TABLE_DIRECTION.RTL

----

LTR
    The table or row is arranged with the first column in the leftmost
    position.

RTL
    The table or row is arranged with the first column in the rightmost
    position.
