
Picture
=======

Word allows a picture to be placed in a graphical object container, either an
inline shape or a floating shape.


Candidate protocol
------------------

::

    >>> run = paragraph.add_run()
    >>> inline_shape = run.add_picture(file_like_image, MIME_type=None)
    >>> inline_shape.width = width
    >>> inline_shape.height = height


Minimal XML
-----------

.. highlight:: xml

This XML represents the working hypothesis of the minimum XML that must be
inserted to add a working picture to a document::

    <pic:pic xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture">
      <pic:nvPicPr>
        <pic:cNvPr id="1" name="python-powered.png"/>
        <pic:cNvPicPr/>
      </pic:nvPicPr>
      <pic:blipFill>
        <a:blip r:embed="rId7"/>
        <a:stretch>
          <a:fillRect/>
        </a:stretch>
      </pic:blipFill>
      <pic:spPr>
        <a:xfrm>
          <a:off x="0" y="0"/>
          <a:ext cx="859536" cy="343814"/>
        </a:xfrm>
        <a:prstGeom prst="rect"/>
      </pic:spPr>
    </pic:pic>


Required parameters:

* unique DrawingML object id (document-wide, pretty sure it's just the part)
* name, either filename or generic if file-like object.
* rId for rel to image part
* size (cx, cy)


Specimen XML
------------

.. highlight:: xml

This XML represents a picture inserted inline on a paragraph by itself::

    <a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture">
      <pic:pic xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture">
        <pic:nvPicPr>
          <pic:cNvPr id="1" name="python-powered.png"/>
          <pic:cNvPicPr/>
        </pic:nvPicPr>
        <pic:blipFill>
          <a:blip r:embed="rId7">
            <a:alphaModFix/>
            <a:extLst>
              <a:ext uri="{28A0092B-C50C-407E-A947-70E740481C1C}">
                <a14:useLocalDpi xmlns:a14="http://schemas.microsoft.com/office/drawing/2010/main" val="0"/>
              </a:ext>
            </a:extLst>
          </a:blip>
          <a:stretch>
            <a:fillRect/>
          </a:stretch>
        </pic:blipFill>
        <pic:spPr>
          <a:xfrm>
            <a:off x="0" y="0"/>
            <a:ext cx="859536" cy="343814"/>
          </a:xfrm>
          <a:prstGeom prst="rect">
            <a:avLst/>
          </a:prstGeom>
        </pic:spPr>
      </pic:pic>
    </a:graphicData>


Schema definitions
------------------

.. highlight:: xml

::

  <xsd:element name="pic" type="CT_Picture"/>

  <xsd:complexType name="CT_Picture">
    <xsd:sequence>
      <xsd:element name="nvPicPr"  type="CT_PictureNonVisual"/>
      <xsd:element name="blipFill" type="a:CT_BlipFillProperties"/>
      <xsd:element name="spPr"     type="a:CT_ShapeProperties"/>
    </xsd:sequence>
  </xsd:complexType>

  <xsd:complexType name="CT_PictureNonVisual">
    <xsd:sequence>
      <xsd:element name="cNvPr"    type="a:CT_NonVisualDrawingProps"/>
      <xsd:element name="cNvPicPr" type="a:CT_NonVisualPictureProperties"/>
    </xsd:sequence>
  </xsd:complexType>

  <xsd:complexType name="CT_BlipFillProperties">
    <xsd:sequence>
      <xsd:element name="blip"    type="CT_Blip"         minOccurs="0"/>
      <xsd:element name="srcRect" type="CT_RelativeRect" minOccurs="0"/>
      <xsd:choice minOccurs="0">
        <xsd:element name="tile"    type="CT_TileInfoProperties"/>
        <xsd:element name="stretch" type="CT_StretchInfoProperties"/>
      </xsd:choice>
    </xsd:sequence>
    <xsd:attribute name="dpi"          type="xsd:unsignedInt"/>
    <xsd:attribute name="rotWithShape" type="xsd:boolean"/>
  </xsd:complexType>

  <xsd:complexType name="CT_ShapeProperties">
    <xsd:sequence>
      <xsd:element name="xfrm"    type="CT_Transform2D"            minOccurs="0"/>
      <xsd:group   ref="EG_Geometry"                               minOccurs="0"/>
      <xsd:group   ref="EG_FillProperties"                         minOccurs="0"/>
      <xsd:element name="ln"      type="CT_LineProperties"         minOccurs="0"/>
      <xsd:group   ref="EG_EffectProperties"                       minOccurs="0"/>
      <xsd:element name="scene3d" type="CT_Scene3D"                minOccurs="0"/>
      <xsd:element name="sp3d"    type="CT_Shape3D"                minOccurs="0"/>
      <xsd:element name="extLst"  type="CT_OfficeArtExtensionList" minOccurs="0"/>
    </xsd:sequence>
    <xsd:attribute name="bwMode" type="ST_BlackWhiteMode"/>
  </xsd:complexType>

  <xsd:complexType name="CT_Blip">  <!-- denormalized -->
    <xsd:sequence>
      <xsd:choice minOccurs="0" maxOccurs="unbounded">
        <xsd:element name="alphaBiLevel" type="CT_AlphaBiLevelEffect"/>
        <xsd:element name="alphaCeiling" type="CT_AlphaCeilingEffect"/>
        <xsd:element name="alphaFloor"   type="CT_AlphaFloorEffect"/>
        <xsd:element name="alphaInv"     type="CT_AlphaInverseEffect"/>
        <xsd:element name="alphaMod"     type="CT_AlphaModulateEffect"/>
        <xsd:element name="alphaModFix"  type="CT_AlphaModulateFixedEffect"/>
        <xsd:element name="alphaRepl"    type="CT_AlphaReplaceEffect"/>
        <xsd:element name="biLevel"      type="CT_BiLevelEffect"/>
        <xsd:element name="blur"         type="CT_BlurEffect"/>
        <xsd:element name="clrChange"    type="CT_ColorChangeEffect"/>
        <xsd:element name="clrRepl"      type="CT_ColorReplaceEffect"/>
        <xsd:element name="duotone"      type="CT_DuotoneEffect"/>
        <xsd:element name="fillOverlay"  type="CT_FillOverlayEffect"/>
        <xsd:element name="grayscl"      type="CT_GrayscaleEffect"/>
        <xsd:element name="hsl"          type="CT_HSLEffect"/>
        <xsd:element name="lum"          type="CT_LuminanceEffect"/>
        <xsd:element name="tint"         type="CT_TintEffect"/>
      </xsd:choice>
      <xsd:element name="extLst" type="CT_OfficeArtExtensionList" minOccurs="0"/>
    </xsd:sequence>
    <xsd:attribute  ref="r:embed" type="ST_RelationshipId"  default=""/>
    <xsd:attribute  ref="r:link"  type="ST_RelationshipId"  default=""/>
    <xsd:attribute name="cstate"  type="ST_BlipCompression" default="none"/>
  </xsd:complexType>

  <xsd:simpleType name="ST_RelationshipId">
    <xsd:restriction base="xsd:string"/>
  </xsd:simpleType>

  <xsd:complexType name="CT_NonVisualDrawingProps">
    <xsd:sequence>
      <xsd:element name="hlinkClick" type="CT_Hyperlink"              minOccurs="0"/>
      <xsd:element name="hlinkHover" type="CT_Hyperlink"              minOccurs="0"/>
      <xsd:element name="extLst"     type="CT_OfficeArtExtensionList" minOccurs="0"/>
    </xsd:sequence>
    <xsd:attribute name="id"     type="ST_DrawingElementId" use="required"/>
    <xsd:attribute name="name"   type="xsd:string"          use="required"/>
    <xsd:attribute name="descr"  type="xsd:string"          default=""/>
    <xsd:attribute name="hidden" type="xsd:boolean"         default="false"/>
    <xsd:attribute name="title"  type="xsd:string"          default=""/>
  </xsd:complexType>

  <xsd:complexType name="CT_NonVisualPictureProperties">
    <xsd:sequence>
      <xsd:element name="picLocks" type="CT_PictureLocking"         minOccurs="0"/>
      <xsd:element name="extLst"   type="CT_OfficeArtExtensionList" minOccurs="0"/>
    </xsd:sequence>
    <xsd:attribute name="preferRelativeResize" type="xsd:boolean" default="true"/>
  </xsd:complexType>

  <xsd:complexType name="CT_Point2D">
    <xsd:attribute name="x" type="ST_Coordinate" use="required"/>
    <xsd:attribute name="y" type="ST_Coordinate" use="required"/>
  </xsd:complexType>

  <xsd:complexType name="CT_PositiveSize2D">
    <xsd:attribute name="cx" type="ST_PositiveCoordinate" use="required"/>
    <xsd:attribute name="cy" type="ST_PositiveCoordinate" use="required"/>
  </xsd:complexType>

  <xsd:complexType name="CT_PresetGeometry2D">
    <xsd:sequence>
      <xsd:element name="avLst" type="CT_GeomGuideList" minOccurs="0"/>
    </xsd:sequence>
    <xsd:attribute name="prst" type="ST_ShapeType" use="required"/>
  </xsd:complexType>

  <xsd:complexType name="CT_RelativeRect">
    <xsd:attribute name="l" type="ST_Percentage" default="0%"/>
    <xsd:attribute name="t" type="ST_Percentage" default="0%"/>
    <xsd:attribute name="r" type="ST_Percentage" default="0%"/>
    <xsd:attribute name="b" type="ST_Percentage" default="0%"/>
  </xsd:complexType>

  <xsd:complexType name="CT_StretchInfoProperties">
    <xsd:sequence>
      <xsd:element name="fillRect" type="CT_RelativeRect" minOccurs="0"/>
    </xsd:sequence>
  </xsd:complexType>

  <xsd:complexType name="CT_Transform2D">
    <xsd:sequence>
      <xsd:element name="off" type="CT_Point2D"        minOccurs="0"/>
      <xsd:element name="ext" type="CT_PositiveSize2D" minOccurs="0"/>
    </xsd:sequence>
    <xsd:attribute name="rot"   type="ST_Angle"    default="0"/>
    <xsd:attribute name="flipH" type="xsd:boolean" default="false"/>
    <xsd:attribute name="flipV" type="xsd:boolean" default="false"/>
  </xsd:complexType>

  <xsd:group name="EG_FillModeProperties">
    <xsd:choice>
      <xsd:element name="tile"    type="CT_TileInfoProperties"/>
      <xsd:element name="stretch" type="CT_StretchInfoProperties"/>
    </xsd:choice>
  </xsd:group>

  <xsd:group name="EG_Geometry">
    <xsd:choice>
      <xsd:element name="custGeom" type="CT_CustomGeometry2D"/>
      <xsd:element name="prstGeom" type="CT_PresetGeometry2D"/>
    </xsd:choice>
  </xsd:group>
