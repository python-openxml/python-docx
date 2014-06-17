# encoding: utf-8

"""
Custom element classes for shape-related elements like ``<w:inline>``
"""

from . import OxmlElement
from .ns import nsmap, nspfxmap, qn
from .simpletypes import ST_PositiveCoordinate, ST_RelationshipId, XsdToken
from .xmlchemy import (
    BaseOxmlElement, OneAndOnlyOne, OptionalAttribute, RequiredAttribute,
    ZeroOrOne
)


class CT_Blip(BaseOxmlElement):
    """
    ``<a:blip>`` element, specifies image source and adjustments such as
    alpha and tint.
    """
    embed = OptionalAttribute('r:embed', ST_RelationshipId)
    link = OptionalAttribute('r:link', ST_RelationshipId)

    @classmethod
    def new(cls, rId):
        blip = OxmlElement('a:blip')
        blip.set(qn('r:embed'), rId)
        return blip


class CT_BlipFillProperties(BaseOxmlElement):
    """
    ``<pic:blipFill>`` element, specifies picture properties
    """
    blip = ZeroOrOne('a:blip', successors=(
        'a:srcRect', 'a:tile', 'a:stretch'
    ))

    @classmethod
    def new(cls, rId):
        blipFill = OxmlElement('pic:blipFill')
        blipFill.append(CT_Blip.new(rId))
        blipFill.append(CT_StretchInfoProperties.new())
        return blipFill


class CT_GraphicalObject(BaseOxmlElement):
    """
    ``<a:graphic>`` element, container for a DrawingML object
    """
    graphicData = OneAndOnlyOne('a:graphicData')

    @classmethod
    def new(cls, uri, pic):
        graphic = OxmlElement('a:graphic')
        graphic.append(CT_GraphicalObjectData.new(uri, pic))
        return graphic


class CT_GraphicalObjectData(BaseOxmlElement):
    """
    ``<a:graphicData>`` element, container for the XML of a DrawingML object
    """
    pic = ZeroOrOne('pic:pic')
    uri = RequiredAttribute('uri', XsdToken)

    @classmethod
    def new(cls, uri, pic):
        graphicData = OxmlElement('a:graphicData')
        graphicData.uri = uri
        graphicData._insert_pic(pic)
        return graphicData


class CT_Inline(BaseOxmlElement):
    """
    ``<w:inline>`` element, container for an inline shape.
    """
    extent = OneAndOnlyOne('wp:extent')
    graphic = OneAndOnlyOne('a:graphic')

    @classmethod
    def new(cls, cx, cy, shape_id, pic):
        """
        Return a new ``<wp:inline>`` element populated with the values passed
        as parameters.
        """
        name = 'Picture %d' % shape_id
        uri = nsmap['pic']

        inline = OxmlElement('wp:inline', nsdecls=nspfxmap('wp', 'r'))
        inline.append(CT_PositiveSize2D.new('wp:extent', cx, cy))
        inline.append(CT_NonVisualDrawingProps.new(
            'wp:docPr', shape_id, name
        ))
        inline.append(CT_GraphicalObject.new(uri, pic))
        return inline


class CT_NonVisualDrawingProps(BaseOxmlElement):
    """
    Used for ``<wp:docPr>`` element, and perhaps others. Specifies the id and
    name of a DrawingML drawing.
    """
    @classmethod
    def new(cls, nsptagname_str, shape_id, name):
        elm = OxmlElement(nsptagname_str)
        elm.set('id', str(shape_id))
        elm.set('name', name)
        return elm


class CT_NonVisualPictureProperties(BaseOxmlElement):
    """
    ``<pic:cNvPicPr>`` element, specifies picture locking and resize
    behaviors.
    """
    @classmethod
    def new(cls):
        return OxmlElement('pic:cNvPicPr')


class CT_Picture(BaseOxmlElement):
    """
    ``<pic:pic>`` element, a DrawingML picture
    """
    blipFill = OneAndOnlyOne('pic:blipFill')

    @classmethod
    def new(cls, pic_id, filename, rId, cx, cy):
        """
        Return a new ``<pic:pic>`` element populated with the minimal
        contents required to define a viable picture element, based on the
        values passed as parameters.
        """
        pic = OxmlElement('pic:pic', nsdecls=nspfxmap('pic', 'r'))
        pic.append(CT_PictureNonVisual.new(pic_id, filename))
        pic.append(CT_BlipFillProperties.new(rId))
        pic.append(CT_ShapeProperties.new(cx, cy))
        return pic


class CT_PictureNonVisual(BaseOxmlElement):
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


class CT_Point2D(BaseOxmlElement):
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


class CT_PositiveSize2D(BaseOxmlElement):
    """
    Used for ``<wp:extent>`` element, and perhaps others later. Specifies the
    size of a DrawingML drawing.
    """
    cx = RequiredAttribute('cx', ST_PositiveCoordinate)
    cy = RequiredAttribute('cy', ST_PositiveCoordinate)

    @classmethod
    def new(cls, nsptagname_str, cx, cy):
        elm = OxmlElement(nsptagname_str)
        elm.cx = cx
        elm.cy = cy
        return elm


class CT_PresetGeometry2D(BaseOxmlElement):
    """
    ``<a:prstGeom>`` element, specifies an preset autoshape geometry, such
    as ``rect``.
    """
    @classmethod
    def new(cls, prst):
        prstGeom = OxmlElement('a:prstGeom')
        prstGeom.set('prst', prst)
        return prstGeom


class CT_RelativeRect(BaseOxmlElement):
    """
    ``<a:fillRect>`` element, specifying picture should fill containing
    rectangle shape.
    """
    @classmethod
    def new(cls):
        return OxmlElement('a:fillRect')


class CT_ShapeProperties(BaseOxmlElement):
    """
    ``<pic:spPr>`` element, specifies size and shape of picture container.
    """
    @classmethod
    def new(cls, cx, cy):
        spPr = OxmlElement('pic:spPr')
        spPr.append(CT_Transform2D.new(cx, cy))
        spPr.append(CT_PresetGeometry2D.new('rect'))
        return spPr


class CT_StretchInfoProperties(BaseOxmlElement):
    """
    ``<a:stretch>`` element, specifies how picture should fill its containing
    shape.
    """
    @classmethod
    def new(cls):
        stretch = OxmlElement('a:stretch')
        stretch.append(CT_RelativeRect.new())
        return stretch


class CT_Transform2D(BaseOxmlElement):
    """
    ``<a:xfrm>`` element, specifies size and shape of picture container.
    """
    @classmethod
    def new(cls, cx, cy):
        spPr = OxmlElement('a:xfrm')
        spPr.append(CT_Point2D.new('a:off', 0, 0))
        spPr.append(CT_PositiveSize2D.new('a:ext', cx, cy))
        return spPr
