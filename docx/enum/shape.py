# encoding: utf-8

"""
Enumerations related to DrawingML shapes in WordprocessingML files
"""

from __future__ import absolute_import, print_function, unicode_literals

from .base import alias, EnumMember, XmlEnumeration, XmlMappedEnumMember


@alias('WD_INLINE_SHAPE')
class WD_INLINE_SHAPE_TYPE(XmlEnumeration):
    """
    Alias: **WD_INLINE_SHAPE**

    Specifies a shape type for inline shapes.
    """

    __ms_name__ = 'WdInlineShapeType'

    __url__ = 'http://msdn.microsoft.com/en-us/library/office/ff192587.aspx'

    __members__ = (
        XmlMappedEnumMember(
            'CHART', 12, 'wdInlineShapeChart', 'Inline chart.'
        ),
        XmlMappedEnumMember(
            'LINKED_PICTURE', 4, 'wdInlineShapeLinkedPicture', 'Linked picture.'
        ),
        XmlMappedEnumMember(
            'PICTURE', 4, 'wdInlineShapePicture', 'Picture.'
        ),
        XmlMappedEnumMember(
            'SMART_ART', 4, 'wdInlineShapeSmartArt', 'A SmartArt graphic.'
        ),
        EnumMember(
            'NOT_IMPLEMENTED', -6, 'Unknown type.'
        ),
    )
