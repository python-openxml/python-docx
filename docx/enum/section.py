# encoding: utf-8

"""
Enumerations related to the main document in WordprocessingML files
"""

from __future__ import absolute_import, print_function, unicode_literals

from .base import alias, XmlEnumeration, XmlMappedEnumMember


@alias("WD_HEADER_FOOTER")
class WD_HEADER_FOOTER_INDEX(XmlEnumeration):
    """
    alias: **WD_HEADER_FOOTER**

    Specifies one of the three possible header/footer definitions for a section.

    For internal use only; not part of the python-docx API.
    """

    __ms_name__ = "WdHeaderFooterIndex"

    __url__ = "https://docs.microsoft.com/en-us/office/vba/api/word.wdheaderfooterindex"

    __members__ = (
        XmlMappedEnumMember(
            "PRIMARY", 1, "default", "Header for odd pages or all if no even header."
        ),
        XmlMappedEnumMember(
            "FIRST_PAGE", 2, "first", "Header for first page of section."
        ),
        XmlMappedEnumMember(
            "EVEN_PAGE", 3, "even", "Header for even pages of recto/verso section."
        ),
    )


@alias("WD_ORIENT")
class WD_ORIENTATION(XmlEnumeration):
    """
    alias: **WD_ORIENT**

    Specifies the page layout orientation.

    Example::

        from docx.enum.section import WD_ORIENT

        section = document.sections[-1]
        section.orientation = WD_ORIENT.LANDSCAPE
    """

    __ms_name__ = "WdOrientation"

    __url__ = "http://msdn.microsoft.com/en-us/library/office/ff837902.aspx"

    __members__ = (
        XmlMappedEnumMember("PORTRAIT", 0, "portrait", "Portrait orientation."),
        XmlMappedEnumMember("LANDSCAPE", 1, "landscape", "Landscape orientation."),
    )


@alias("WD_SECTION")
class WD_SECTION_START(XmlEnumeration):
    """
    alias: **WD_SECTION**

    Specifies the start type of a section break.

    Example::

        from docx.enum.section import WD_SECTION

        section = document.sections[0]
        section.start_type = WD_SECTION.NEW_PAGE
    """

    __ms_name__ = "WdSectionStart"

    __url__ = "http://msdn.microsoft.com/en-us/library/office/ff840975.aspx"

    __members__ = (
        XmlMappedEnumMember("CONTINUOUS", 0, "continuous", "Continuous section break."),
        XmlMappedEnumMember("NEW_COLUMN", 1, "nextColumn", "New column section break."),
        XmlMappedEnumMember("NEW_PAGE", 2, "nextPage", "New page section break."),
        XmlMappedEnumMember("EVEN_PAGE", 3, "evenPage", "Even pages section break."),
        XmlMappedEnumMember(
            "ODD_PAGE", 4, "oddPage", "Section begins on next odd page."
        ),
    )
