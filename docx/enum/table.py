# encoding: utf-8

"""
Enumerations related to tables in WordprocessingML files
"""

from __future__ import absolute_import, print_function, unicode_literals

from .base import XmlEnumeration, XmlMappedEnumMember


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
