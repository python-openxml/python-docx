# encoding: utf-8

"""
Enumerations shared by docx modules.
"""

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

from .base import XmlEnumeration, XmlMappedEnumMember

class WD_ALIGN_VERTICAL(XmlEnumeration):
    """
    Specifies vertical alignment in table cells

    Example::

        from docx.enum.table import WD_ALIGN_VERTICAL

        table = document.add_table(3, 3)
        table.cell(0, 0).vertical_alignment = WD_ALIGN_VERTICAL.BOTTOM
    """

    __ms_name__ = 'WdVerticalAlignment'

    __url__ = 'https://msdn.microsoft.com/en-us/library/office/ff845387.aspx'

    __members__ = (
        XmlMappedEnumMember(
            'TOP', 0, 'top', 'Top vertical alignment'
        ),
        XmlMappedEnumMember(
            'CENTER', 1, 'center', 'Center vertical alignment'
        ),
        XmlMappedEnumMember(
            'JUSTIFY', 2, 'both', 'Justified vertical alignment'
        ),
        XmlMappedEnumMember(
            'BOTTOM', 3, 'bottom', 'Bottom vertical alignment'
        ),
    )
