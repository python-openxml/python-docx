# encoding: utf-8

"""
Enumerations related to tables in WordprocessingML files
"""

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

from .base import (
    Enumeration, EnumMember, XmlEnumeration, XmlMappedEnumMember
)


class WD_ROW_HEIGHT_RULE(XmlEnumeration):
    """
    Specifies the rule for determining the height or a table row

    Example::

        from docx.enum.table import WD_ROW_HEIGHT_RULE

        table = document.add_table(3, 3)
        table.rows[0].height_rule = WD_ROW_HEIGHT_RULE.EXACTLY
    """

    __ms_name__ = "WdRowHeightRule"

    __url__ = 'https://msdn.microsoft.com/en-us/library/office/ff193620.aspx'

    __members__ = (
        XmlMappedEnumMember(
            'AUTO', 0, 'auto', 'The row height is adjusted to accommodate the '
            'tallest value in the row.'
        ),
        XmlMappedEnumMember(
            'AT_LEAST', 1, 'atLeast', 'The row height is at least a minimum '
            'specified value.'
        ),
        XmlMappedEnumMember(
            'EXACTLY', 2, 'exact', 'The row height is an exact value.'
        ),
    )


class WD_TABLE_ALIGNMENT(XmlEnumeration):
    """
    Specifies table justification type.

    Example::

        from docx.enum.table import WD_TABLE_ALIGNMENT

        table = document.add_table(3, 3)
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
    """

    __ms_name__ = 'WdRowAlignment'

    __url__ = ' http://office.microsoft.com/en-us/word-help/HV080607259.aspx'

    __members__ = (
        XmlMappedEnumMember(
            'LEFT', 0, 'left', 'Left-aligned'
        ),
        XmlMappedEnumMember(
            'CENTER', 1, 'center', 'Center-aligned.'
        ),
        XmlMappedEnumMember(
            'RIGHT', 2, 'right', 'Right-aligned.'
        ),
    )


class WD_TABLE_DIRECTION(Enumeration):
    """
    Specifies the direction in which an application orders cells in the
    specified table or row.

    Example::

        from docx.enum.table import WD_TABLE_DIRECTION

        table = document.add_table(3, 3)
        table.direction = WD_TABLE_DIRECTION.RTL
    """

    __ms_name__ = 'WdTableDirection'

    __url__ = ' http://msdn.microsoft.com/en-us/library/ff835141.aspx'

    __members__ = (
        EnumMember(
            'LTR', 0, 'The table or row is arranged with the first column '
            'in the leftmost position.'
        ),
        EnumMember(
            'RTL', 1, 'The table or row is arranged with the first column '
            'in the rightmost position.'
        ),
    )
