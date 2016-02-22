
Inline shape
============

Word allows a graphical object to be placed into a document as an inline
object. An inline shape appears as a ``<w:drawing>`` element as a child of
a ``<w:r>`` element.


Candidate protocol -- inline shape access
-----------------------------------------

The following interactive session illustrates the protocol for accessing an
inline shape::

    >>> inline_shapes = document.body.inline_shapes
    >>> inline_shape = inline_shapes[0]
    >>> assert inline_shape.type == MSO_SHAPE_TYPE.PICTURE


Resources
---------

* `Document Members (Word) on MSDN`_
* `InlineShape Members (Word) on MSDN`_
* `Shape Members (Word) on MSDN`_

.. _Document Members (Word) on MSDN:
   http://msdn.microsoft.com/en-us/library/office/ff840898.aspx

.. _InlineShape Members (Word) on MSDN:
   http://msdn.microsoft.com/en-us/library/office/ff840794.aspx

.. _Shape Members (Word) on MSDN:
   http://msdn.microsoft.com/en-us/library/office/ff195191.aspx


MS API
------

The Shapes and InlineShapes properties on Document hold references to things
like pictures in the MS API.

* Height and Width
* Borders
* Shadow
* Hyperlink
* PictureFormat (providing brightness, color, crop, transparency, contrast)
* ScaleHeight and ScaleWidth
* HasChart
* HasSmartArt
* Type (Chart, LockedCanvas, Picture, SmartArt, etc.)


Spec references
---------------

* 17.3.3.9 drawing (DrawingML Object)
* 20.4.2.8 inline (Inline DrawingML Object)
* 20.4.2.7 extent (Drawing Object Size)


Minimal XML
-----------

.. highlight:: xml

This XML represents my best guess of the minimal inline shape container that
Word will load::

    <w:r>
      <w:drawing>
        <wp:inline>
          <wp:extent cx="914400" cy="914400"/>
          <wp:docPr id="1" name="Picture 1"/>
          <a:graphic xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">
            <a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture">

              <!-- might not have to put anything here for a start -->

            </a:graphicData>
          </a:graphic>
        </wp:inline>
      </w:drawing>
    </w:r>


Specimen XML
------------

.. highlight:: xml

A ``CT_Drawing`` (``<w:drawing>``) element can appear in a run, as a peer of,
for example, a ``<w:t>`` element. This element contains a DrawingML object.
WordprocessingML drawings are discussed in section 20.4 of the ISO/IEC spec.

This XML represents an inline shape inserted inline on a paragraph by itself.
The particulars of the graphical object itself are redacted::

    <w:p>
      <w:r>
        <w:rPr/>
          <w:noProof/>
        </w:rPr>
        <w:drawing>
          <wp:inline distT="0" distB="0" distL="0" distR="0" wp14:anchorId="1BDE1558" wp14:editId="31E593BB">
            <wp:extent cx="859536" cy="343814"/>
            <wp:effectExtent l="0" t="0" r="4445" b="12065"/>
            <wp:docPr id="1" name="Picture 1"/>
            <wp:cNvGraphicFramePr>
              <a:graphicFrameLocks xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" noChangeAspect="1"/>
            </wp:cNvGraphicFramePr>
            <a:graphic xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">
              <a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture">

                <!-- graphical object, such as pic:pic, goes here -->

              </a:graphicData>
            </a:graphic>
          </wp:inline>
        </w:drawing>
      </w:r>
    </w:p>


Schema definitions
------------------

.. highlight:: xml

::

  <xsd:complexType name="CT_Drawing">
    <xsd:choice minOccurs="1" maxOccurs="unbounded">
      <xsd:element ref="wp:anchor" minOccurs="0"/>
      <xsd:element ref="wp:inline" minOccurs="0"/>
    </xsd:choice>
  </xsd:complexType>

  <xsd:complexType name="CT_Inline">
    <xsd:sequence>
      <xsd:element name="extent"            type="a:CT_PositiveSize2D"/>
      <xsd:element name="effectExtent"      type="CT_EffectExtent"                      minOccurs="0"/>
      <xsd:element name="docPr"             type="a:CT_NonVisualDrawingProps"/>
      <xsd:element name="cNvGraphicFramePr" type="a:CT_NonVisualGraphicFrameProperties" minOccurs="0"/>
      <xsd:element name="graphic"           type="CT_GraphicalObject"/>
    </xsd:sequence>
    <xsd:attribute name="distT" type="ST_WrapDistance"/>
    <xsd:attribute name="distB" type="ST_WrapDistance"/>
    <xsd:attribute name="distL" type="ST_WrapDistance"/>
    <xsd:attribute name="distR" type="ST_WrapDistance"/>
  </xsd:complexType>

  <xsd:complexType name="CT_PositiveSize2D">
    <xsd:attribute name="cx" type="ST_PositiveCoordinate" use="required"/>
    <xsd:attribute name="cy" type="ST_PositiveCoordinate" use="required"/>
  </xsd:complexType>

  <xsd:complexType name="CT_EffectExtent">
    <xsd:attribute name="l" type="a:ST_Coordinate" use="required"/>
    <xsd:attribute name="t" type="a:ST_Coordinate" use="required"/>
    <xsd:attribute name="r" type="a:ST_Coordinate" use="required"/>
    <xsd:attribute name="b" type="a:ST_Coordinate" use="required"/>
  </xsd:complexType>

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

  <xsd:complexType name="CT_NonVisualGraphicFrameProperties">
    <xsd:sequence>
      <xsd:element name="graphicFrameLocks" type="CT_GraphicalObjectFrameLocking" minOccurs="0"/>
      <xsd:element name="extLst"            type="CT_OfficeArtExtensionList"      minOccurs="0"/>
    </xsd:sequence>
  </xsd:complexType>

  <xsd:complexType name="CT_GraphicalObject">
    <xsd:sequence>
      <xsd:element name="graphicData" type="CT_GraphicalObjectData"/>
    </xsd:sequence>
  </xsd:complexType>

  <xsd:complexType name="CT_GraphicalObjectData">
    <xsd:sequence>
      <xsd:any minOccurs="0" maxOccurs="unbounded" processContents="strict"/>
    </xsd:sequence>
    <xsd:attribute name="uri" type="xsd:token" use="required"/>
  </xsd:complexType>
