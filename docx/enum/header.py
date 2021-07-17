# encoding: utf-8

"""
Enumerations related to headers and footers
"""

from __future__ import (
    absolute_import, print_function, unicode_literals, division
)

from .base import alias, XmlEnumeration, XmlMappedEnumMember


@alias('WD_HEADER_FOOTER')
class WD_HEADER_FOOTER_INDEX(XmlEnumeration):
    """
    alias: **WD_HEADER_FOOTER**

    Specifies the type of a header or footer.
    """

    __ms_name__ = 'WdHeaderFooterIndex'

    __url__ = 'https://msdn.microsoft.com/en-us/library/office/ff839314.aspx'

    __members__ = (
        XmlMappedEnumMember(
            'PRIMARY', 1, 'default', 'The header or footer appearing on all '
            'pages except when an even and/or first-page header/footer is de'
            'fined.'
        ),
        XmlMappedEnumMember(
            'FIRST_PAGE', 2, 'first', 'The header or footer appearing only o'
            'n the first page of the specified section.'
        ),
        XmlMappedEnumMember(
            'EVEN_PAGES', 3, 'even', 'The header or footer appearing on even'
            ' numbered (verso) pages in the specified section.'
        ),
    )
