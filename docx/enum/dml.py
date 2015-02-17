# encoding: utf-8

"""
Enumerations used by DrawingML objects
"""

from __future__ import absolute_import

from .base import (
    alias, Enumeration, EnumMember, XmlEnumeration, XmlMappedEnumMember
)


class MSO_COLOR_TYPE(Enumeration):
    """
    Specifies the color specification scheme

    Example::

        from docx.enum.dml import MSO_COLOR_TYPE

        assert font.color.type == MSO_COLOR_TYPE.SCHEME
    """

    __ms_name__ = 'MsoColorType'

    __url__ = (
        'http://msdn.microsoft.com/en-us/library/office/ff864912(v=office.15'
        ').aspx'
    )

    __members__ = (
        EnumMember(
            'RGB', 1, 'Color is specified by an |RGBColor| value.'
        ),
        EnumMember(
            'THEME', 2, 'Color is one of the preset theme colors.'
        ),
        EnumMember(
            'AUTO', 101, 'Color is determined automatically by the '
            'application.'
        ),
    )


@alias('MSO_THEME_COLOR')
class MSO_THEME_COLOR_INDEX(XmlEnumeration):
    """
    Indicates the Office theme color, one of those shown in the color gallery
    on the formatting ribbon.

    Alias: ``MSO_THEME_COLOR``

    Example::

        from docx.enum.dml import MSO_THEME_COLOR

        font.color.theme_color = MSO_THEME_COLOR.ACCENT_1
    """

    __ms_name__ = 'MsoThemeColorIndex'

    __url__ = (
        'http://msdn.microsoft.com/en-us/library/office/ff860782(v=office.15'
        ').aspx'
    )

    __members__ = (
        EnumMember(
            'NOT_THEME_COLOR', 0, 'Indicates the color is not a theme color.'
        ),
        XmlMappedEnumMember(
            'ACCENT_1', 5, 'accent1', 'Specifies the Accent 1 theme color.'
        ),
        XmlMappedEnumMember(
            'ACCENT_2', 6, 'accent2', 'Specifies the Accent 2 theme color.'
        ),
        XmlMappedEnumMember(
            'ACCENT_3', 7, 'accent3', 'Specifies the Accent 3 theme color.'
        ),
        XmlMappedEnumMember(
            'ACCENT_4', 8, 'accent4', 'Specifies the Accent 4 theme color.'
        ),
        XmlMappedEnumMember(
            'ACCENT_5', 9, 'accent5', 'Specifies the Accent 5 theme color.'
        ),
        XmlMappedEnumMember(
            'ACCENT_6', 10, 'accent6', 'Specifies the Accent 6 theme color.'
        ),
        XmlMappedEnumMember(
            'BACKGROUND_1', 14, 'background1', 'Specifies the Background 1 '
            'theme color.'
        ),
        XmlMappedEnumMember(
            'BACKGROUND_2', 16, 'background2', 'Specifies the Background 2 '
            'theme color.'
        ),
        XmlMappedEnumMember(
            'DARK_1', 1, 'dark1', 'Specifies the Dark 1 theme color.'
        ),
        XmlMappedEnumMember(
            'DARK_2', 3, 'dark2', 'Specifies the Dark 2 theme color.'
        ),
        XmlMappedEnumMember(
            'FOLLOWED_HYPERLINK', 12, 'followedHyperlink', 'Specifies the '
            'theme color for a clicked hyperlink.'
        ),
        XmlMappedEnumMember(
            'HYPERLINK', 11, 'hyperlink', 'Specifies the theme color for a '
            'hyperlink.'
        ),
        XmlMappedEnumMember(
            'LIGHT_1', 2, 'light1', 'Specifies the Light 1 theme color.'
        ),
        XmlMappedEnumMember(
            'LIGHT_2', 4, 'light2', 'Specifies the Light 2 theme color.'
        ),
        XmlMappedEnumMember(
            'TEXT_1', 13, 'text1', 'Specifies the Text 1 theme color.'
        ),
        XmlMappedEnumMember(
            'TEXT_2', 15, 'text2', 'Specifies the Text 2 theme color.'
        ),
    )
