# encoding: utf-8

"""
Enumerations related to text in WordprocessingML files
"""

from __future__ import absolute_import, print_function, unicode_literals


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


class WD_UNDERLINE(object):
    """
    Corresponds to WdUnderline enumeration
    http://msdn.microsoft.com/en-us/library/office/ff822388.aspx
    """
    NONE = 0
    SINGLE = 1
    WORDS = 2
    DOUBLE = 3
    DOTTED = 4
    THICK = 6
    DASH = 7
    DOT_DASH = 9
    DOT_DOT_DASH = 10
    WAVY = 11
    DOTTED_HEAVY = 20
    DASH_HEAVY = 23
    DOT_DASH_HEAVY = 25
    DOT_DOT_DASH_HEAVY = 26
    WAVY_HEAVY = 27
    DASH_LONG = 39
    WAVY_DOUBLE = 43
    DASH_LONG_HEAVY = 55
