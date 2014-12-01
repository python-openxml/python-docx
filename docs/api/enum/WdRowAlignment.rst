.. _WdRowAlignment:

``WD_TABLE_ALIGNMENT``
======================

Specifies table justification type.

Example::

    from docx.enum.table import WD_TABLE_ALIGNMENT

    table = document.add_table(3, 3)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER

----

LEFT
    Left-aligned

CENTER
    Center-aligned.

RIGHT
    Right-aligned.
