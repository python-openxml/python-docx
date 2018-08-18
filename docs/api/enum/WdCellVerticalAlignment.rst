.. _WdCellVerticalAlignment:

``WD_CELL_VERTICAL_ALIGNMENT``
==============================

alias: **WD_ALIGN_VERTICAL**

Specifies the vertical alignment of text in one or more cells of a table.

Example::

    from docx.enum.table import WD_ALIGN_VERTICAL

    table = document.add_table(3, 3)
    table.cell(0, 0).vertical_alignment = WD_ALIGN_VERTICAL.BOTTOM

----

TOP
    Text is aligned to the top border of the cell.

CENTER
    Text is aligned to the center of the cell.

BOTTOM
    Text is aligned to the bottom border of the cell.

BOTH
    This is an option in the OpenXml spec, but not in Word itself. It's not
    clear what Word behavior this setting produces. If you find out please let
    us know and we'll update this documentation. Otherwise, probably best to
    avoid this option.
