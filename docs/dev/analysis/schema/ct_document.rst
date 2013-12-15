
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


attributes
----------

===========  ===  ===================
name          #   type
===========  ===  ===================
conformance   ?   ST_ConformanceClass
===========  ===  ===================


child elements
--------------

==========  ===  =============
name         #   type
==========  ===  =============
background   ?   CT_Background
body         ?   CT_Body
==========  ===  =============


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


RELAX NG Schema Excerpt
-----------------------

::

    w_CT_Body =
      w_EG_BlockLevelElts*,
      element sectPr { w_CT_SectPr }?

    w_EG_BlockLevelElts =
      w_EG_BlockLevelChunkElts*
      | element altChunk { w_CT_AltChunk }*

    w_EG_BlockLevelChunkElts = w_EG_ContentBlockContent*

    w_EG_ContentBlockContent =
      element customXml { w_CT_CustomXmlBlock }
      | element sdt { w_CT_SdtBlock }
      | element p { w_CT_P }*
      | element tbl { w_CT_Tbl }*
      | w_EG_RunLevelElts*

    w_EG_RunLevelElts =
      element proofErr { w_CT_ProofErr }?
      | element permStart { w_CT_PermStart }?
      | element permEnd { w_CT_Perm }?
      | w_EG_RangeMarkupElements*
      | element ins { w_CT_RunTrackChange }?
      | element del { w_CT_RunTrackChange }?
      | element moveFrom { w_CT_RunTrackChange }
      | element moveTo { w_CT_RunTrackChange }
      | w_EG_MathContent*

    w_EG_RangeMarkupElements =
      element bookmarkStart                 { w_CT_Bookmark }
      | element bookmarkEnd                 { w_CT_MarkupRange }
      | element moveFromRangeStart          { w_CT_MoveBookmark }
      | element moveFromRangeEnd            { w_CT_MarkupRange }
      | element moveToRangeStart            { w_CT_MoveBookmark }
      | element moveToRangeEnd              { w_CT_MarkupRange }
      | element commentRangeStart           { w_CT_MarkupRange }
      | element commentRangeEnd             { w_CT_MarkupRange }
      | element customXmlInsRangeStart      { w_CT_TrackChange } | element customXmlInsRangeEnd        { w_CT_Markup }
      | element customXmlDelRangeStart      { w_CT_TrackChange }
      | element customXmlDelRangeEnd        { w_CT_Markup }
      | element customXmlMoveFromRangeStart { w_CT_TrackChange }
      | element customXmlMoveFromRangeEnd   { w_CT_Markup }
      | element customXmlMoveToRangeStart   { w_CT_TrackChange }
      | element customXmlMoveToRangeEnd     { w_CT_Markup }

    w_EG_MathContent = m_oMathPara | m_oMath


Schema excerpt
^^^^^^^^^^^^^^

.. highlight:: xml

::

  <xsd:complexType name="CT_Document">
    <xsd:complexContent>
      <xsd:extension base="CT_DocumentBase">
        <xsd:sequence>
          <xsd:element name="body" type="CT_Body" minOccurs="0" maxOccurs="1"/>
        </xsd:sequence>
        <xsd:attribute name="conformance" type="s:ST_ConformanceClass"/>
      </xsd:extension>
    </xsd:complexContent>
  </xsd:complexType>

  <xsd:complexType name="CT_DocumentBase">
    <xsd:sequence>
      <xsd:element name="background" type="CT_Background" minOccurs="0"/>
    </xsd:sequence>
  </xsd:complexType>

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
        <xsd:any processContents="lax" namespace="urn:schemas-microsoft-com:vml" minOccurs="0" maxOccurs="unbounded"/>
        <xsd:any processContents="lax" namespace="urn:schemas-microsoft-com:office:office" minOccurs="0" maxOccurs="unbounded"/>
      </xsd:sequence>
      <xsd:element name="drawing" type="CT_Drawing" minOccurs="0"/>
    </xsd:sequence>
    <xsd:attribute name="color"      type="ST_HexColor"       use="optional"/>
    <xsd:attribute name="themeColor" type="ST_ThemeColor"     use="optional"/>
    <xsd:attribute name="themeTint"  type="ST_UcharHexNumber" use="optional"/>
    <xsd:attribute name="themeShade" type="ST_UcharHexNumber" use="optional"/>
  </xsd:complexType>

  <xsd:complexType name="CT_Body">
    <xsd:sequence>
      <xsd:group ref="EG_BlockLevelElts" minOccurs="0" maxOccurs="unbounded"/>
      <xsd:element name="sectPr" minOccurs="0" maxOccurs="1" type="CT_SectPr"/>
    </xsd:sequence>
  </xsd:complexType>

  <xsd:group name="EG_BlockLevelElts">
    <xsd:choice>
      <xsd:group   ref="EG_BlockLevelChunkElts"       minOccurs="0" maxOccurs="unbounded"/>
      <xsd:element name="altChunk" type="CT_AltChunk" minOccurs="0" maxOccurs="unbounded"/>
    </xsd:choice>
  </xsd:group>

  <xsd:group name="EG_BlockLevelChunkElts">
    <xsd:choice>
      <xsd:group ref="EG_ContentBlockContent" minOccurs="0" maxOccurs="unbounded"/>
    </xsd:choice>
  </xsd:group>

  <xsd:group name="EG_ContentBlockContent">
    <xsd:choice>
      <xsd:element name="customXml" type="CT_CustomXmlBlock"/>
      <xsd:element name="sdt"       type="CT_SdtBlock"/>
      <xsd:element name="p"         type="CT_P"   minOccurs="0" maxOccurs="unbounded"/>
      <xsd:element name="tbl"       type="CT_Tbl" minOccurs="0" maxOccurs="unbounded"/>
      <xsd:group   ref="EG_RunLevelElts"          minOccurs="0" maxOccurs="unbounded"/>
    </xsd:choice>
  </xsd:group>

  <xsd:group name="EG_RunLevelElts">
    <xsd:choice>
      <xsd:element name="proofErr"  type="CT_ProofErr"       minOccurs="0"/>
      <xsd:element name="permStart" type="CT_PermStart"      minOccurs="0"/>
      <xsd:element name="permEnd"   type="CT_Perm"           minOccurs="0"/>
      <xsd:group   ref="EG_RangeMarkupElements"              minOccurs="0" maxOccurs="unbounded"/>
      <xsd:element name="ins"       type="CT_RunTrackChange" minOccurs="0"/>
      <xsd:element name="del"       type="CT_RunTrackChange" minOccurs="0"/>
      <xsd:element name="moveFrom"  type="CT_RunTrackChange"/>
      <xsd:element name="moveTo"    type="CT_RunTrackChange"/>
      <xsd:group   ref="EG_MathContent"                      minOccurs="0" maxOccurs="unbounded"/>
    </xsd:choice>
  </xsd:group>

  <xsd:group name="EG_RangeMarkupElements">
    <xsd:choice>
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
    </xsd:choice>
  </xsd:group>

  <xsd:group name="EG_MathContent">
    <xsd:choice>
      <xsd:element ref="m:oMathPara"/>
      <xsd:element ref="m:oMath"/>
    </xsd:choice>
  </xsd:group>
