"""Enumerations related to tables in WordprocessingML files."""

from docx.enum.base import BaseEnum, BaseXmlEnum


class WD_CELL_VERTICAL_ALIGNMENT(BaseXmlEnum):
    """Alias: **WD_ALIGN_VERTICAL**

    Specifies the vertical alignment of text in one or more cells of a table.

    Example::

        from docx.enum.table import WD_ALIGN_VERTICAL

        table = document.add_table(3, 3)
        table.cell(0, 0).vertical_alignment = WD_ALIGN_VERTICAL.BOTTOM

    MS API name: `WdCellVerticalAlignment`

    https://msdn.microsoft.com/en-us/library/office/ff193345.aspx
    """

    TOP = (0, "top", "Text is aligned to the top border of the cell.")
    """Text is aligned to the top border of the cell."""

    CENTER = (1, "center", "Text is aligned to the center of the cell.")
    """Text is aligned to the center of the cell."""

    BOTTOM = (3, "bottom", "Text is aligned to the bottom border of the cell.")
    """Text is aligned to the bottom border of the cell."""

    BOTH = (
        101,
        "both",
        "This is an option in the OpenXml spec, but not in Word itself. It's not"
        " clear what Word behavior this setting produces. If you find out please"
        " let us know and we'll update this documentation. Otherwise, probably best"
        " to avoid this option.",
    )
    """This is an option in the OpenXml spec, but not in Word itself.

    It's not clear what Word behavior this setting produces. If you find out please let
    us know and we'll update this documentation. Otherwise, probably best to avoid this
    option.
    """


WD_ALIGN_VERTICAL = WD_CELL_VERTICAL_ALIGNMENT


class WD_ROW_HEIGHT_RULE(BaseXmlEnum):
    """Alias: **WD_ROW_HEIGHT**

    Specifies the rule for determining the height of a table row

    Example::

        from docx.enum.table import WD_ROW_HEIGHT_RULE

        table = document.add_table(3, 3)
        table.rows[0].height_rule = WD_ROW_HEIGHT_RULE.EXACTLY

    MS API name: `WdRowHeightRule`

    https://msdn.microsoft.com/en-us/library/office/ff193620.aspx
    """

    AUTO = (
        0,
        "auto",
        "The row height is adjusted to accommodate the tallest value in the row.",
    )
    """The row height is adjusted to accommodate the tallest value in the row."""

    AT_LEAST = (1, "atLeast", "The row height is at least a minimum specified value.")
    """The row height is at least a minimum specified value."""

    EXACTLY = (2, "exact", "The row height is an exact value.")
    """The row height is an exact value."""


WD_ROW_HEIGHT = WD_ROW_HEIGHT_RULE


class WD_TABLE_ALIGNMENT(BaseXmlEnum):
    """Specifies table justification type.

    Example::

        from docx.enum.table import WD_TABLE_ALIGNMENT

        table = document.add_table(3, 3)
        table.alignment = WD_TABLE_ALIGNMENT.CENTER

    MS API name: `WdRowAlignment`

    http://office.microsoft.com/en-us/word-help/HV080607259.aspx
    """

    LEFT = (0, "left", "Left-aligned")
    """Left-aligned"""

    CENTER = (1, "center", "Center-aligned.")
    """Center-aligned."""

    RIGHT = (2, "right", "Right-aligned.")
    """Right-aligned."""


class WD_TABLE_DIRECTION(BaseEnum):
    """Specifies the direction in which an application orders cells in the specified
    table or row.

    Example::

        from docx.enum.table import WD_TABLE_DIRECTION

        table = document.add_table(3, 3)
        table.direction = WD_TABLE_DIRECTION.RTL

    MS API name: `WdTableDirection`

    http://msdn.microsoft.com/en-us/library/ff835141.aspx
    """

    LTR = (
        0,
        "The table or row is arranged with the first column in the leftmost position.",
    )
    """The table or row is arranged with the first column in the leftmost position."""

    RTL = (
        1,
        "The table or row is arranged with the first column in the rightmost position.",
    )
    """The table or row is arranged with the first column in the rightmost position."""
