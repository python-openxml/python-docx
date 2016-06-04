.. _WdVerticalAlignment:

``WD_ALIGN_VERTICAL``
=====================

Specifies vertical alignment in table cells

Example::

    from docx.enum.table import WD_ALIGN_VERTICAL

    table = document.add_table(3, 3)
    table.cell(0, 0).vertical_alignment = WD_ALIGN_VERTICAL.BOTTOM

----

TOP
    Top vertical alignment

CENTER
    Center vertical alignment

JUSTIFY
    Justified vertical alignment

BOTTOM
    Bottom vertical alignment

