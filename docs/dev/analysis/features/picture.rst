
Picture
=======


Overview
--------

Word allows a picture to be placed in a graphical object container, either an
inline shape or a floating shape.


Candidate protocol
------------------

::

    >>> run = body.add_paragraph().add_run()
    >>> shape = run.add_picture(
    ...     image, width=None, height=None, MIME_type=None
    ... )


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

  <xsd:complexType name="CT_GraphicalObjectData">
    <xsd:sequence>
      <xsd:any minOccurs="0" maxOccurs="unbounded" processContents="strict"/>
    </xsd:sequence>
    <xsd:attribute name="uri" type="xsd:token" use="required"/>
  </xsd:complexType>

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
      <xsd:group   ref="EG_FillModeProperties"           minOccurs="0" maxOccurs="1"/>
    </xsd:sequence>
    <xsd:attribute name="dpi"          type="xsd:unsignedInt" use="optional"/>
    <xsd:attribute name="rotWithShape" type="xsd:boolean"     use="optional"/>
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
    <xsd:attribute name="bwMode" type="ST_BlackWhiteMode" use="optional"/>
  </xsd:complexType>

  <xsd:complexType name="CT_NonVisualDrawingProps">
    <xsd:sequence>
      <xsd:element name="hlinkClick" type="CT_Hyperlink"              minOccurs="0"/>
      <xsd:element name="hlinkHover" type="CT_Hyperlink"              minOccurs="0"/>
      <xsd:element name="extLst"     type="CT_OfficeArtExtensionList" minOccurs="0"/>
    </xsd:sequence>
    <xsd:attribute name="id"     type="ST_DrawingElementId" use="required"/>
    <xsd:attribute name="name"   type="xsd:string"          use="required"/>
    <xsd:attribute name="descr"  type="xsd:string"          use="optional" default=""/>
    <xsd:attribute name="hidden" type="xsd:boolean"         use="optional" default="false"/>
    <xsd:attribute name="title"  type="xsd:string"          use="optional" default=""/>
  </xsd:complexType>
