.. _WdRowHeightRule:

``WD_ROW_HEIGHT_RULE``
======================

alias: **WD_ROW_HEIGHT**

Specifies the rule for determining the height of a table row

Example::

    from docx.enum.table import WD_ROW_HEIGHT_RULE

    table = document.add_table(3, 3)
    table.rows[0].height_rule = WD_ROW_HEIGHT_RULE.EXACTLY

----

AUTO
    The row height is adjusted to accommodate the tallest value in the row.

AT_LEAST
    The row height is at least a minimum specified value.

EXACTLY
    The row height is an exact value.
