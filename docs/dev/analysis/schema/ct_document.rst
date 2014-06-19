
``CT_Document``
===============

.. csv-table::
   :header-rows: 0
   :stub-columns: 1
   :widths: 15, 50

   Spec Name    , Document
   Tag(s)       , w:document
   Namespace    , wordprocessingml (wml.xsd)
   Spec Section , 17.2.3


Spec text
---------

    This element specifies the contents of a main document part in
    a WordprocessingML document.

    Consider the basic structure of the main document part in a basic
    WordprocessingML document, as follows::

        <w:document>
          <w:body>
            <w:p/>
          </w:body>
        </w:document>

    All of the contents of the main document part are contained beneath the
    document element.


Schema excerpt
--------------

.. highlight:: xml

::

  <xsd:complexType name="CT_Document">
    <xsd:sequence>
      <xsd:element name="background" type="CT_Background" minOccurs="0"/>
      <xsd:element name="body"       type="CT_Body"       minOccurs="0" maxOccurs="1"/>
    </xsd:sequence>
    <xsd:attribute name="conformance" type="s:ST_ConformanceClass"/>
  </xsd:complexType>

  <xsd:simpleType name="ST_ConformanceClass">
    <xsd:restriction base="xsd:string">
      <xsd:enumeration value="strict"/>
      <xsd:enumeration value="transitional"/>
    </xsd:restriction>
  </xsd:simpleType>

  <xsd:complexType name="CT_Background">
    <xsd:sequence>
      <xsd:sequence maxOccurs="unbounded">
        <xsd:any processContents="lax" namespace="urn:schemas-microsoft-com:vml"
                 minOccurs="0" maxOccurs="unbounded"/>
        <xsd:any processContents="lax" namespace="urn:schemas-microsoft-com:office:office"
                 minOccurs="0" maxOccurs="unbounded"/>
      </xsd:sequence>
      <xsd:element name="drawing" type="CT_Drawing" minOccurs="0"/>
    </xsd:sequence>
    <xsd:attribute name="color"      type="ST_HexColor"       use="optional"/>
    <xsd:attribute name="themeColor" type="ST_ThemeColor"     use="optional"/>
    <xsd:attribute name="themeTint"  type="ST_UcharHexNumber" use="optional"/>
    <xsd:attribute name="themeShade" type="ST_UcharHexNumber" use="optional"/>
  </xsd:complexType>

  <xsd:complexType name="CT_Body">  <!-- denormalized -->
    <xsd:sequence>
      <xsd:choice minOccurs="0" maxOccurs="unbounded">
        <xsd:element name="p"                           type="CT_P"/>
        <xsd:element name="tbl"                         type="CT_Tbl"/>
        <xsd:element name="sdt"                         type="CT_SdtBlock"/>
        <xsd:element name="customXml"                   type="CT_CustomXmlBlock"/>
        <xsd:element name="altChunk"                    type="CT_AltChunk"/>
        <xsd:element name="proofErr"                    type="CT_ProofErr"/>
        <xsd:element name="permStart"                   type="CT_PermStart"/>
        <xsd:element name="permEnd"                     type="CT_Perm"/>
        <xsd:element name="bookmarkStart"               type="CT_Bookmark"/>
        <xsd:element name="bookmarkEnd"                 type="CT_MarkupRange"/>
        <xsd:element name="moveFromRangeStart"          type="CT_MoveBookmark"/>
        <xsd:element name="moveFromRangeEnd"            type="CT_MarkupRange"/>
        <xsd:element name="moveToRangeStart"            type="CT_MoveBookmark"/>
        <xsd:element name="moveToRangeEnd"              type="CT_MarkupRange"/>
        <xsd:element name="commentRangeStart"           type="CT_MarkupRange"/>
        <xsd:element name="commentRangeEnd"             type="CT_MarkupRange"/>
        <xsd:element name="customXmlInsRangeStart"      type="CT_TrackChange"/>
        <xsd:element name="customXmlInsRangeEnd"        type="CT_Markup"/>
        <xsd:element name="customXmlDelRangeStart"      type="CT_TrackChange"/>
        <xsd:element name="customXmlDelRangeEnd"        type="CT_Markup"/>
        <xsd:element name="customXmlMoveFromRangeStart" type="CT_TrackChange"/>
        <xsd:element name="customXmlMoveFromRangeEnd"   type="CT_Markup"/>
        <xsd:element name="customXmlMoveToRangeStart"   type="CT_TrackChange"/>
        <xsd:element name="customXmlMoveToRangeEnd"     type="CT_Markup"/>
        <xsd:element name="ins"                         type="CT_RunTrackChange"/>
        <xsd:element name="del"                         type="CT_RunTrackChange"/>
        <xsd:element name="moveFrom"                    type="CT_RunTrackChange"/>
        <xsd:element name="moveTo"                      type="CT_RunTrackChange"/>
        <xsd:element ref="m:oMathPara"/>
        <xsd:element ref="m:oMath"/>
      </xsd:choice>
      <xsd:element name="sectPr" minOccurs="0" maxOccurs="1" type="CT_SectPr"/>
    </xsd:sequence>
  </xsd:complexType>
