# encoding: utf-8

"""
Custom element classes for shape-related elements like ``<w:inline>``
"""

from docx.oxml.shared import (
    nsmap, nspfxmap, OxmlBaseElement, OxmlElement, qn
)
from docx.shared import Emu


class CT_Blip(OxmlBaseElement):
    """
    ``<a:blip>`` element, specifies image source and adjustments such as
    alpha and tint.
    """
    @property
    def embed(self):
        return self.get(qn('r:embed'))

    @property
    def link(self):
        return self.get(qn('r:link'))

    @classmethod
    def new(cls, rId):
        blip = OxmlElement('a:blip')
        blip.set(qn('r:embed'), rId)
        return blip


class CT_BlipFillProperties(OxmlBaseElement):
    """
    ``<pic:blipFill>`` element, specifies picture properties
    """
    @property
    def blip(self):
        return self.find(qn('a:blip'))

    @classmethod
    def new(cls, rId):
        blipFill = OxmlElement('pic:blipFill')
        blipFill.append(CT_Blip.new(rId))
        blipFill.append(CT_StretchInfoProperties.new())
        return blipFill


class CT_GraphicalObject(OxmlBaseElement):
    """
    ``<a:graphic>`` element, container for a DrawingML object
    """
    @property
    def graphicData(self):
        return self.find(qn('a:graphicData'))

    @classmethod
    def new(cls, uri, pic):
        graphic = OxmlElement('a:graphic')
        graphic.append(CT_GraphicalObjectData.new(uri, pic))
        return graphic


class CT_GraphicalObjectData(OxmlBaseElement):
    """
    ``<a:graphicData>`` element, container for the XML of a DrawingML object
    """
    @classmethod
    def new(cls, uri, pic):
        graphicData = OxmlElement('a:graphicData')
        graphicData.set('uri', uri)
        graphicData.append(pic)
        return graphicData

    @property
    def pic(self):
        return self.find(qn('pic:pic'))

    @property
    def uri(self):
        return self.get('uri')


class CT_Inline(OxmlBaseElement):
    """
    ``<w:inline>`` element, container for an inline shape.
    """
    @property
    def extent(self):
        return self.find(qn('wp:extent'))

    @property
    def graphic(self):
        return self.find(qn('a:graphic'))

    @classmethod
    def new(cls, cx, cy, shape_id, pic):
        """
        Return a new ``<wp:inline>`` element populated with the values passed
        as parameters.
        """
        name = 'Picture %d' % shape_id
        uri = nsmap['pic']

        inline = OxmlElement('wp:inline', nsmap=nspfxmap('wp', 'r'))
        inline.append(CT_PositiveSize2D.new('wp:extent', cx, cy))
        inline.append(CT_NonVisualDrawingProps.new(
            'wp:docPr', shape_id, name
        ))
        inline.append(CT_GraphicalObject.new(uri, pic))
        return inline


class CT_NonVisualDrawingProps(OxmlBaseElement):
    """
    Used for ``<wp:docPr>`` element, and perhaps others. Specifies the id and
    name of a DrawingML drawing.
    """
    @classmethod
    def new(cls, nsptagname_str, shape_id, name):
        elt = OxmlElement(nsptagname_str)
        elt.set('id', str(shape_id))
        elt.set('name', name)
        return elt


class CT_NonVisualPictureProperties(OxmlBaseElement):
    """
    ``<pic:cNvPicPr>`` element, specifies picture locking and resize
    behaviors.
    """
    @classmethod
    def new(cls):
        return OxmlElement('pic:cNvPicPr')


class CT_Picture(OxmlBaseElement):
    """
    ``<pic:pic>`` element, a DrawingML picture
    """
    @property
    def blipFill(self):
        return self.find(qn('pic:blipFill'))

    @classmethod
    def new(cls, pic_id, filename, rId, cx, cy):
        """
        Return a new ``<pic:pic>`` element populated with the minimal
        contents required to define a viable picture element, based on the
        values passed as parameters.
        """
        pic = OxmlElement('pic:pic', nsmap=nspfxmap('pic', 'r'))
        pic.append(CT_PictureNonVisual.new(pic_id, filename))
        pic.append(CT_BlipFillProperties.new(rId))
        pic.append(CT_ShapeProperties.new(cx, cy))
        return pic


class CT_PictureNonVisual(OxmlBaseElement):
    """
    ``<pic:nvPicPr>`` element, non-visual picture properties
    """
    @classmethod
    def new(cls, pic_id, image_filename):
        nvPicPr = OxmlElement('pic:nvPicPr')
        nvPicPr.append(CT_NonVisualDrawingProps.new(
            'pic:cNvPr', pic_id, image_filename
        ))
        nvPicPr.append(CT_NonVisualPictureProperties.new())
        return nvPicPr


class CT_Point2D(OxmlBaseElement):
    """
    Used for ``<a:off>`` element, and perhaps others. Specifies an x, y
    coordinate (point).
    """
    @classmethod
    def new(cls, nsptagname_str, x, y):
        elm = OxmlElement(nsptagname_str)
        elm.set('x', str(x))
        elm.set('y', str(y))
        return elm


class CT_PositiveSize2D(OxmlBaseElement):
    """
    Used for ``<wp:extent>`` element, and perhaps others later. Specifies the
    size of a DrawingML drawing.
    """
    @property
    def cx(self):
        cx_str = self.get('cx')
        cx = int(cx_str)
        return Emu(cx)

    @cx.setter
    def cx(self, cx):
        cx_str = str(cx)
        self.set('cx', cx_str)

    @property
    def cy(self):
        cy_str = self.get('cy')
        cy = int(cy_str)
        return Emu(cy)

    @cy.setter
    def cy(self, cy):
        cy_str = str(cy)
        self.set('cy', cy_str)

    @classmethod
    def new(cls, nsptagname_str, cx, cy):
        elm = OxmlElement(nsptagname_str)
        elm.set('cx', str(cx))
        elm.set('cy', str(cy))
        return elm


class CT_PresetGeometry2D(OxmlBaseElement):
    """
    ``<a:prstGeom>`` element, specifies an preset autoshape geometry, such
    as ``rect``.
    """
    @classmethod
    def new(cls, prst):
        prstGeom = OxmlElement('a:prstGeom')
        prstGeom.set('prst', prst)
        return prstGeom


class CT_RelativeRect(OxmlBaseElement):
    """
    ``<a:fillRect>`` element, specifying picture should fill containing
    rectangle shape.
    """
    @classmethod
    def new(cls):
        return OxmlElement('a:fillRect')


class CT_ShapeProperties(OxmlBaseElement):
    """
    ``<pic:spPr>`` element, specifies size and shape of picture container.
    """
    @classmethod
    def new(cls, cx, cy):
        spPr = OxmlElement('pic:spPr')
        spPr.append(CT_Transform2D.new(cx, cy))
        spPr.append(CT_PresetGeometry2D.new('rect'))
        return spPr


class CT_StretchInfoProperties(OxmlBaseElement):
    """
    ``<a:stretch>`` element, specifies how picture should fill its containing
    shape.
    """
    @classmethod
    def new(cls):
        stretch = OxmlElement('a:stretch')
        stretch.append(CT_RelativeRect.new())
        return stretch


class CT_Transform2D(OxmlBaseElement):
    """
    ``<a:xfrm>`` element, specifies size and shape of picture container.
    """
    @classmethod
    def new(cls, cx, cy):
        spPr = OxmlElement('a:xfrm')
        spPr.append(CT_Point2D.new('a:off', 0, 0))
        spPr.append(CT_PositiveSize2D.new('a:ext', cx, cy))
        return spPr
