# encoding: utf-8

"""
Enumerations related to text in WordprocessingML files
"""

from __future__ import absolute_import, print_function, unicode_literals

from .base import XmlEnumeration, XmlMappedEnumMember


class WD_BREAK_TYPE(object):
    """
    Corresponds to WdBreakType enumeration
    http://msdn.microsoft.com/en-us/library/office/ff195905.aspx
    """
    COLUMN = 8
    LINE = 6
    LINE_CLEAR_LEFT = 9
    LINE_CLEAR_RIGHT = 10
    LINE_CLEAR_ALL = 11  # added for consistency, not in MS version
    PAGE = 7
    SECTION_CONTINUOUS = 3
    SECTION_EVEN_PAGE = 4
    SECTION_NEXT_PAGE = 2
    SECTION_ODD_PAGE = 5
    TEXT_WRAPPING = 11

WD_BREAK = WD_BREAK_TYPE


class WD_UNDERLINE(XmlEnumeration):
    """
    Specifies the style of underline applied to a run of characters.
    """

    __ms_name__ = 'WdUnderline'

    __url__ = 'http://msdn.microsoft.com/en-us/library/office/ff822388.aspx'

    __members__ = (
        XmlMappedEnumMember(
            None, None, None, 'Inherit underline setting from containing par'
            'agraph.'
        ),
        XmlMappedEnumMember(
            'NONE', 0, 'none', 'No underline. This setting overrides any inh'
            'erited underline value, so can be used to remove underline from'
            ' a run that inherits underlining from its containing paragraph.'
            ' Note this is not the same as assigning |None| to Run.underline'
            '. |None| is a valid assignment value, but causes the run to inh'
            'erit its underline value. Assigning ``WD_UNDERLINE.NONE`` cause'
            's underlining to be unconditionally turned off.'
        ),
        XmlMappedEnumMember(
            'SINGLE', 1, 'single', 'A single line. Note that this setting is'
            'write-only in the sense that |True| (rather than ``WD_UNDERLINE'
            '.SINGLE``) is returned for a run having this setting.'
        ),
        XmlMappedEnumMember(
            'WORDS', 2, 'words', 'Underline individual words only.'
        ),
        XmlMappedEnumMember(
            'DOUBLE', 3, 'double', 'A double line.'
        ),
        XmlMappedEnumMember(
            'DOTTED', 4, 'dotted', 'Dots.'
        ),
        XmlMappedEnumMember(
            'THICK', 6, 'thick', 'A single thick line.'
        ),
        XmlMappedEnumMember(
            'DASH', 7, 'dash', 'Dashes.'
        ),
        XmlMappedEnumMember(
            'DOT_DASH', 9, 'dotDash', 'Alternating dots and dashes.'
        ),
        XmlMappedEnumMember(
            'DOT_DOT_DASH', 10, 'dotDotDash', 'An alternating dot-dot-dash p'
            'attern.'
        ),
        XmlMappedEnumMember(
            'WAVY', 11, 'wave', 'A single wavy line.'
        ),
        XmlMappedEnumMember(
            'DOTTED_HEAVY', 20, 'dottedHeavy', 'Heavy dots.'
        ),
        XmlMappedEnumMember(
            'DASH_HEAVY', 23, 'dashedHeavy', 'Heavy dashes.'
        ),
        XmlMappedEnumMember(
            'DOT_DASH_HEAVY', 25, 'dashDotHeavy', 'Alternating heavy dots an'
            'd heavy dashes.'
        ),
        XmlMappedEnumMember(
            'DOT_DOT_DASH_HEAVY', 26, 'dashDotDotHeavy', 'An alternating hea'
            'vy dot-dot-dash pattern.'
        ),
        XmlMappedEnumMember(
            'WAVY_HEAVY', 27, 'wavyHeavy', 'A heavy wavy line.'
        ),
        XmlMappedEnumMember(
            'DASH_LONG', 39, 'dashLong', 'Long dashes.'
        ),
        XmlMappedEnumMember(
            'WAVY_DOUBLE', 43, 'wavyDouble', 'A double wavy line.'
        ),
        XmlMappedEnumMember(
            'DASH_LONG_HEAVY', 55, 'dashLongHeavy', 'Long heavy dashes.'
        ),
    )
