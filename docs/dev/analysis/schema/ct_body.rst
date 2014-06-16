
``CT_Body``
===========

.. highlight:: xml

.. csv-table::
   :header-rows: 0
   :stub-columns: 1
   :widths: 15, 50

   Schema Name  , CT_Body
   Spec Name    , Document Body
   Tag(s)       , w:body
   Namespace    , wordprocessingml (wml.xsd)
   Spec Section , 17.2.2


Spec text
---------

    This element specifies the contents of the body of the document -- the main
    document editing surface.

    The document body contains what is referred to as *block-level markup* --
    markup which can exist as a sibling element to paragraphs in a
    WordprocessingML document.

    Example: Consider a document with a single paragraph in the main document
    story. This document would require the following WordprocessingML in its
    main document part::

        <w:document>
          <w:body>
            <w:p/>
          </w:body>
        </w:document>

    The fact that the paragraph is inside the body element makes it part of the
    main document story.


Schema excerpt
--------------

::

  <xsd:complexType name="CT_Body">
    <xsd:sequence>
      <xsd:choice minOccurs="0" maxOccurs="unbounded">
        <xsd:element name="p"                           type="CT_P"/>
        <xsd:element name="tbl"                         type="CT_Tbl"/>
        <xsd:element name="customXml"                   type="CT_CustomXmlBlock"/>
        <xsd:element name="sdt"                         type="CT_SdtBlock"/>
        <xsd:element name="proofErr"                    type="CT_ProofErr"/>
        <xsd:element name="permStart"                   type="CT_PermStart"/>
        <xsd:element name="permEnd"                     type="CT_Perm"/>
        <xsd:element name="ins"                         type="CT_RunTrackChange"/>
        <xsd:element name="del"                         type="CT_RunTrackChange"/>
        <xsd:element name="moveFrom"                    type="CT_RunTrackChange"/>
        <xsd:element name="moveTo"                      type="CT_RunTrackChange"/>
        <xsd:element  ref="m:oMathPara"                 type="CT_OMathPara"/>
        <xsd:element  ref="m:oMath"                     type="CT_OMath"/>
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
        <xsd:element name="altChunk"                    type="CT_AltChunk"/>
      </xsd:choice>
      <xsd:element name="sectPr" type="CT_SectPr" minOccurs="0" maxOccurs="1"/>
    </xsd:sequence>
  </xsd:complexType>

  <xsd:complexType name="CT_Body">
    <xsd:sequence>
      <xsd:group   ref="EG_BlockLevelElts"        minOccurs="0" maxOccurs="unbounded"/>
      <xsd:element name="sectPr" type="CT_SectPr" minOccurs="0" maxOccurs="1"/>
    </xsd:sequence>
  </xsd:complexType>

  <xsd:complexType name="CT_SectPr">
    <xsd:sequence>
      <xsd:group   ref="EG_HdrFtrReferences"                  minOccurs="0" maxOccurs="6"/>
      <xsd:group   ref="EG_SectPrContents"                    minOccurs="0"/>
      <xsd:element name="sectPrChange" type="CT_SectPrChange" minOccurs="0"/>
    </xsd:sequence>
    <xsd:attributeGroup ref="AG_SectPrAttributes"/>
  </xsd:complexType>

  <xsd:group name="EG_BlockLevelElts">
    <xsd:choice>
      <xsd:group    ref="EG_BlockLevelChunkElts"/>
      <xsd:element name="altChunk"               type="CT_AltChunk"/>
    </xsd:choice>
  </xsd:group>

  <xsd:group name="EG_BlockLevelChunkElts">
    <xsd:choice>
      <xsd:group ref="EG_ContentBlockContent"/>
    </xsd:choice>
  </xsd:group>

  <xsd:group name="EG_ContentBlockContent">
    <xsd:choice>
      <xsd:element name="customXml"       type="CT_CustomXmlBlock"/>
      <xsd:element name="sdt"             type="CT_SdtBlock"/>
      <xsd:element name="p"               type="CT_P"/>
      <xsd:element name="tbl"             type="CT_Tbl"/>
      <xsd:group    ref="EG_RunLevelElts"/>
    </xsd:choice>
  </xsd:group>

  <xsd:group name="EG_RunLevelElts">
    <xsd:choice>
      <xsd:element name="proofErr"               type="CT_ProofErr"/>
      <xsd:element name="permStart"              type="CT_PermStart"/>
      <xsd:element name="permEnd"                type="CT_Perm"/>
      <xsd:element name="ins"                    type="CT_RunTrackChange"/>
      <xsd:element name="del"                    type="CT_RunTrackChange"/>
      <xsd:element name="moveFrom"               type="CT_RunTrackChange"/>
      <xsd:element name="moveTo"                 type="CT_RunTrackChange"/>
      <xsd:group    ref="EG_MathContent"/>
      <xsd:group    ref="EG_RangeMarkupElements"/>
    </xsd:choice>
  </xsd:group>

  <xsd:group name="EG_MathContent">
    <xsd:choice>
      <xsd:element ref="m:oMathPara" type="CT_OMathPara"/>
      <xsd:element ref="m:oMath"     type="CT_OMath"/>
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
