"""Custom element classes for shape-related elements like `<w:inline>`."""

from __future__ import annotations

from typing import TYPE_CHECKING, cast

from docx.oxml.ns import nsdecls
from docx.oxml.parser import parse_xml
from docx.oxml.simpletypes import (
    ST_Coordinate,
    ST_DrawingElementId,
    ST_PositiveCoordinate,
    ST_RelationshipId,
    XsdString,
    XsdToken,
)
from docx.oxml.xmlchemy import (
    BaseOxmlElement,
    OneAndOnlyOne,
    OptionalAttribute,
    RequiredAttribute,
    ZeroOrOne,
)

if TYPE_CHECKING:
    from docx.shared import Length


class CT_Anchor(BaseOxmlElement):
    """`<wp:anchor>` element, container for a "floating" shape."""


class CT_Blip(BaseOxmlElement):
    """``<a:blip>`` element, specifies image source and adjustments such as alpha and
    tint."""

    embed: str | None = OptionalAttribute(  # pyright: ignore[reportAssignmentType]
        "r:embed", ST_RelationshipId
    )
    link: str | None = OptionalAttribute(  # pyright: ignore[reportAssignmentType]
        "r:link", ST_RelationshipId
    )


class CT_BlipFillProperties(BaseOxmlElement):
    """``<pic:blipFill>`` element, specifies picture properties."""

    blip: CT_Blip = ZeroOrOne(  # pyright: ignore[reportAssignmentType]
        "a:blip", successors=("a:srcRect", "a:tile", "a:stretch")
    )


class CT_GraphicalObject(BaseOxmlElement):
    """``<a:graphic>`` element, container for a DrawingML object."""

    graphicData: CT_GraphicalObjectData = OneAndOnlyOne(  # pyright: ignore[reportAssignmentType]
        "a:graphicData"
    )


class CT_GraphicalObjectData(BaseOxmlElement):
    """``<a:graphicData>`` element, container for the XML of a DrawingML object."""

    pic: CT_Picture = ZeroOrOne("pic:pic")  # pyright: ignore[reportAssignmentType]
    uri: str = RequiredAttribute("uri", XsdToken)  # pyright: ignore[reportAssignmentType]


class CT_Inline(BaseOxmlElement):
    """`<wp:inline>` element, container for an inline shape."""

    extent: CT_PositiveSize2D = OneAndOnlyOne("wp:extent")  # pyright: ignore[reportAssignmentType]
    docPr: CT_NonVisualDrawingProps = OneAndOnlyOne(  # pyright: ignore[reportAssignmentType]
        "wp:docPr"
    )
    graphic: CT_GraphicalObject = OneAndOnlyOne(  # pyright: ignore[reportAssignmentType]
        "a:graphic"
    )

    @classmethod
    def new(cls, cx: Length, cy: Length, shape_id: int, pic: CT_Picture) -> CT_Inline:
        """Return a new ``<wp:inline>`` element populated with the values passed as
        parameters."""
        inline = cast(CT_Inline, parse_xml(cls._inline_xml()))
        inline.extent.cx = cx
        inline.extent.cy = cy
        inline.docPr.id = shape_id
        inline.docPr.name = "Picture %d" % shape_id
        inline.graphic.graphicData.uri = "http://schemas.openxmlformats.org/drawingml/2006/picture"
        inline.graphic.graphicData._insert_pic(pic)
        return inline

    @classmethod
    def new_pic_inline(
        cls, shape_id: int, rId: str, filename: str, cx: Length, cy: Length
    ) -> CT_Inline:
        """Create `wp:inline` element containing a `pic:pic` element.

        The contents of the `pic:pic` element is taken from the argument values.
        """
        pic_id = 0  # Word doesn't seem to use this, but does not omit it
        pic = CT_Picture.new(pic_id, filename, rId, cx, cy)
        inline = cls.new(cx, cy, shape_id, pic)
        inline.graphic.graphicData._insert_pic(pic)
        return inline

    @classmethod
    def _inline_xml(cls):
        return (
            "<wp:inline %s>\n"
            '  <wp:extent cx="914400" cy="914400"/>\n'
            '  <wp:docPr id="666" name="unnamed"/>\n'
            "  <wp:cNvGraphicFramePr>\n"
            '    <a:graphicFrameLocks noChangeAspect="1"/>\n'
            "  </wp:cNvGraphicFramePr>\n"
            "  <a:graphic>\n"
            '    <a:graphicData uri="URI not set"/>\n'
            "  </a:graphic>\n"
            "</wp:inline>" % nsdecls("wp", "a", "pic", "r")
        )


class CT_NonVisualDrawingProps(BaseOxmlElement):
    """Used for ``<wp:docPr>`` element, and perhaps others.

    Specifies the id and name of a DrawingML drawing.
    """

    id = RequiredAttribute("id", ST_DrawingElementId)
    name = RequiredAttribute("name", XsdString)


class CT_NonVisualPictureProperties(BaseOxmlElement):
    """``<pic:cNvPicPr>`` element, specifies picture locking and resize behaviors."""


class CT_Picture(BaseOxmlElement):
    """``<pic:pic>`` element, a DrawingML picture."""

    nvPicPr: CT_PictureNonVisual = OneAndOnlyOne(  # pyright: ignore[reportAssignmentType]
        "pic:nvPicPr"
    )
    blipFill: CT_BlipFillProperties = OneAndOnlyOne(  # pyright: ignore[reportAssignmentType]
        "pic:blipFill"
    )
    spPr: CT_ShapeProperties = OneAndOnlyOne("pic:spPr")  # pyright: ignore[reportAssignmentType]

    @classmethod
    def new(cls, pic_id, filename, rId, cx, cy):
        """Return a new ``<pic:pic>`` element populated with the minimal contents
        required to define a viable picture element, based on the values passed as
        parameters."""
        pic = parse_xml(cls._pic_xml())
        pic.nvPicPr.cNvPr.id = pic_id
        pic.nvPicPr.cNvPr.name = filename
        pic.blipFill.blip.embed = rId
        pic.spPr.cx = cx
        pic.spPr.cy = cy
        return pic

    @classmethod
    def _pic_xml(cls):
        return (
            "<pic:pic %s>\n"
            "  <pic:nvPicPr>\n"
            '    <pic:cNvPr id="666" name="unnamed"/>\n'
            "    <pic:cNvPicPr/>\n"
            "  </pic:nvPicPr>\n"
            "  <pic:blipFill>\n"
            "    <a:blip/>\n"
            "    <a:stretch>\n"
            "      <a:fillRect/>\n"
            "    </a:stretch>\n"
            "  </pic:blipFill>\n"
            "  <pic:spPr>\n"
            "    <a:xfrm>\n"
            '      <a:off x="0" y="0"/>\n'
            '      <a:ext cx="914400" cy="914400"/>\n'
            "    </a:xfrm>\n"
            '    <a:prstGeom prst="rect"/>\n'
            "  </pic:spPr>\n"
            "</pic:pic>" % nsdecls("pic", "a", "r")
        )


class CT_PictureNonVisual(BaseOxmlElement):
    """``<pic:nvPicPr>`` element, non-visual picture properties."""

    cNvPr = OneAndOnlyOne("pic:cNvPr")


class CT_Point2D(BaseOxmlElement):
    """Used for ``<a:off>`` element, and perhaps others.

    Specifies an x, y coordinate (point).
    """

    x = RequiredAttribute("x", ST_Coordinate)
    y = RequiredAttribute("y", ST_Coordinate)


class CT_PositiveSize2D(BaseOxmlElement):
    """Used for ``<wp:extent>`` element, and perhaps others later.

    Specifies the size of a DrawingML drawing.
    """

    cx: Length = RequiredAttribute(  # pyright: ignore[reportAssignmentType]
        "cx", ST_PositiveCoordinate
    )
    cy: Length = RequiredAttribute(  # pyright: ignore[reportAssignmentType]
        "cy", ST_PositiveCoordinate
    )


class CT_PresetGeometry2D(BaseOxmlElement):
    """``<a:prstGeom>`` element, specifies an preset autoshape geometry, such as
    ``rect``."""


class CT_RelativeRect(BaseOxmlElement):
    """``<a:fillRect>`` element, specifying picture should fill containing rectangle
    shape."""


class CT_ShapeProperties(BaseOxmlElement):
    """``<pic:spPr>`` element, specifies size and shape of picture container."""

    xfrm = ZeroOrOne(
        "a:xfrm",
        successors=(
            "a:custGeom",
            "a:prstGeom",
            "a:ln",
            "a:effectLst",
            "a:effectDag",
            "a:scene3d",
            "a:sp3d",
            "a:extLst",
        ),
    )

    @property
    def cx(self):
        """Shape width as an instance of Emu, or None if not present."""
        xfrm = self.xfrm
        if xfrm is None:
            return None
        return xfrm.cx

    @cx.setter
    def cx(self, value):
        xfrm = self.get_or_add_xfrm()
        xfrm.cx = value

    @property
    def cy(self):
        """Shape height as an instance of Emu, or None if not present."""
        xfrm = self.xfrm
        if xfrm is None:
            return None
        return xfrm.cy

    @cy.setter
    def cy(self, value):
        xfrm = self.get_or_add_xfrm()
        xfrm.cy = value


class CT_StretchInfoProperties(BaseOxmlElement):
    """``<a:stretch>`` element, specifies how picture should fill its containing
    shape."""


class CT_Transform2D(BaseOxmlElement):
    """``<a:xfrm>`` element, specifies size and shape of picture container."""

    off = ZeroOrOne("a:off", successors=("a:ext",))
    ext = ZeroOrOne("a:ext", successors=())

    @property
    def cx(self):
        ext = self.ext
        if ext is None:
            return None
        return ext.cx

    @cx.setter
    def cx(self, value):
        ext = self.get_or_add_ext()
        ext.cx = value

    @property
    def cy(self):
        ext = self.ext
        if ext is None:
            return None
        return ext.cy

    @cy.setter
    def cy(self, value):
        ext = self.get_or_add_ext()
        ext.cy = value
