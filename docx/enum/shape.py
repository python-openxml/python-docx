# encoding: utf-8

"""
Enumerations related to DrawingML shapes in WordprocessingML files
"""

from __future__ import absolute_import, print_function, unicode_literals


class WD_INLINE_SHAPE_TYPE(object):
    """
    Corresponds to WdInlineShapeType enumeration
    http://msdn.microsoft.com/en-us/library/office/ff192587.aspx
    """
    CHART = 12
    LINKED_PICTURE = 4
    PICTURE = 3
    SMART_ART = 15
    NOT_IMPLEMENTED = -6


WD_INLINE_SHAPE = WD_INLINE_SHAPE_TYPE
