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
from .shared import Parented


class InlineShapes(Parented):
    """
    Sequence of |InlineShape| instances, supporting len(), iteration, and
    indexed access.
    """
    def __init__(self, body_elm, parent):
        super(InlineShapes, self).__init__(parent)
        self._body = body_elm

    def __getitem__(self, idx):
        """
        Provide indexed access, e.g. 'inline_shapes[idx]'
        """
        try:
            inline = self._inline_lst[idx]
        except IndexError:
            msg = "inline shape index [%d] out of range" % idx
            raise IndexError(msg)
        return InlineShape(inline)

    def __iter__(self):
        return (InlineShape(inline) for inline in self._inline_lst)

    def __len__(self):
        return len(self._inline_lst)

    def add_picture(self, image_descriptor, run):
        """
        Return an |InlineShape| instance containing the picture identified by
        *image_descriptor* and added to the end of *run*. The picture shape
        has the native size of the image. *image_descriptor* can be a path (a
        string) or a file-like object containing a binary image.
        """
        image_part, rId = self.part.get_or_add_image_part(image_descriptor)
        shape_id = self.part.next_id
        r = run._r
        picture = InlineShape.new_picture(r, image_part, rId, shape_id)
        return picture

    @property
    def _inline_lst(self):
        body = self._body
        xpath = '//w:p/w:r/w:drawing/wp:inline'
        return body.xpath(xpath)


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
    def new_picture(cls, r, image_part, rId, shape_id):
        """
        Return a new |InlineShape| instance containing an inline picture
        placement of *image_part* appended to run *r* and uniquely identified
        by *shape_id*.
        """
        cx, cy, filename = (
            image_part.default_cx, image_part.default_cy, image_part.filename
        )
        pic_id = 0
        pic = CT_Picture.new(pic_id, filename, rId, cx, cy)
        inline = CT_Inline.new(cx, cy, shape_id, pic)
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
