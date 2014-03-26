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

class WD_UNDERLINE_TYPE(object):
    """
    Underline types, corresponding to WdUnderline enumeration
    http://msdn.microsoft.com/en-us/library/office/ff822388(v=office.15).aspx
    """
    DASH = 7 # Dashes.
    DASH_HEAVY = 23 # Heavy dashes.
    DASH_LONG = 39 # Long dashes.
    LONG_HEAVY = 55 # Long heavy dashes.
    DOT_DASH = 9 # Alternating dots and dashes.
    DOT_DASH_HEAVY = 25 # Alternating heavy dots and heavy dashes.
    DOT_DOT_DASH = 10 # An alternating dot-dot-dash pattern.
    DOT_DOT_DASH_HEAVY = 26 # An alternating heavy dot-dot-dash pattern.
    DOTTED = 4 # Dots.
    DOTTED_HEAVY = 20 # Heavy dots.
    DOUBLE = 3 # A double line.
    NONE = 0 # No underline.
    SINGLE = 1 # A single line. default.
    THICK = 6 # A single thick line.
    WAVY = 11 #A single wavy line.
    WAVY_DOUBLE = 43 # A double wavy line.
    WAVY_HEAVY = 27 # A heavy wavy line.
    WORDS = 2 # Underline individual words only.
    
    stringDict={
        DASH:'dash',
        DASH_HEAVY:'dashHeavy',
        DASH_LONG:'dashLong',
        LONG_HEAVY:'longHeavy',
        DOT_DASH:'dotDash',
        DOT_DASH_HEAVY:'dotDashHeavy',
        DOT_DOT_DASH:'dotDotDash',
        DOT_DOT_DASH_HEAVY:'dotDotDashHeavy',
        DOTTED:'dotted',
        DOTTED_HEAVY:'dottedHeavy',
        DOUBLE:'double',
        NONE:'none',
        SINGLE:'single',
        THICK:'thick',
        WAVY:'wavy',
        WAVY_DOUBLE:'wavyDouble',
        WAVY_HEAVY:'wavyHeavy',
        WORDS:'words',
    }    
    
WD_UNDERLINE = WD_UNDERLINE_TYPE