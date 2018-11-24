# encoding: utf-8

"""
Enumerations related to the main document in WordprocessingML files
"""

from __future__ import absolute_import, print_function, unicode_literals

from .base import alias, XmlEnumeration, XmlMappedEnumMember


@alias('WD_HEADER_FOOTER')
class WD_HEADER_FOOTER(XmlEnumeration):
    """
    alias: **WD_HEADER_FOOTER_INDEX**

    Specified header or footer in a document or section.

    Example::

        from docx.enum.header_footer import WD_HEADER_FOOTER

        header = document.sections[-1].header
        first_page_header = document.sections[-1].first_page_header
        even_odd_header = document.sections[-1].even_odd_header
    """

    __ms_name__ = 'WdHeaderFooterIndex'

    __url__ = 'https://docs.microsoft.com/en-us/office/vba/api/word.wdheaderfooterindex'

    __members__ = (
        XmlMappedEnumMember(
            'PRIMARY', 1, 'default', 'Header or footer on all pages other than the first page of a document or section.'
        ),
        XmlMappedEnumMember(
            'FIRST_PAGE', 2, 'first', 'First header or footer in a document or section.'
        ),
        XmlMappedEnumMember(
            'EVEN_PAGE', 3, 'even', 'Headers or footers on even-numbered pages.'
        ),
    )
