# encoding: utf-8

"""
Objects related to shapes, visual objects that appear on the drawing layer of
a document.
"""

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

from .enum.shape import WD_INLINE_SHAPE
from .oxml.shape import CT_Inline, CT_Picture
from .oxml.ns import nsmap


class InlineShape(object):
    """
    Proxy for an ``<wp:inline>`` element, representing the container for an
    inline graphical object.
    """
    def __init__(self, inline):
        super(InlineShape, self).__init__()
        self._inline = inline

    @property
    def height(self):
        """
        Read/write. The display height of this inline shape as an |Emu|
        instance.
        """
        return self._inline.extent.cy

    @height.setter
    def height(self, cy):
        assert isinstance(cy, int)
        assert 0 < cy
        self._inline.extent.cy = cy

    @classmethod
    def new_picture(cls, r, image_part, rId, shape_id, width, height):
        """
        Return a new |InlineShape| instance containing an inline picture
        placement of *image_part* appended to run *r* and uniquely identified
        by *shape_id*.
        """
        # scale picture dimensions if width and/or height provided
        if width is not None or height is not None:
            native_width, native_height = image_part.default_cx, image_part.default_cy
            if width is None:
                scaling_factor = float(height) / float(native_height)
                width = int(round(native_width * scaling_factor))
            elif height is None:
                scaling_factor = float(width) / float(native_width)
                height = int(round(native_height * scaling_factor))
        else:
            width = image_part.default_cx
            height = image_part.default_cy

        filename = image_part.filename
        
        pic_id = 0
        pic = CT_Picture.new(pic_id, filename, rId, width, height)
        inline = CT_Inline.new(width, height, shape_id, pic)
        r.add_drawing(inline)
        return cls(inline)

    @property
    def type(self):
        """
        The type of this inline shape as a member of
        ``docx.enum.shape.WD_INLINE_SHAPE``, e.g. ``LINKED_PICTURE``.
        Read-only.
        """
        graphicData = self._inline.graphic.graphicData
        uri = graphicData.uri
        if uri == nsmap['pic']:
            blip = graphicData.pic.blipFill.blip
            if blip.link is not None:
                return WD_INLINE_SHAPE.LINKED_PICTURE
            return WD_INLINE_SHAPE.PICTURE
        if uri == nsmap['c']:
            return WD_INLINE_SHAPE.CHART
        if uri == nsmap['dgm']:
            return WD_INLINE_SHAPE.SMART_ART
        return WD_INLINE_SHAPE.NOT_IMPLEMENTED

    @property
    def width(self):
        """
        Read/write. The display width of this inline shape as an |Emu|
        instance.
        """
        return self._inline.extent.cx

    @width.setter
    def width(self, cx):
        assert isinstance(cx, int)
        assert 0 < cx
        self._inline.extent.cx = cx
