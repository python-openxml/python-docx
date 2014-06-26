
``CT_P``
========

.. csv-table::
   :header-rows: 0
   :stub-columns: 1
   :widths: 15, 50

   Spec Name    , Paragraph
   Tag(s)       , w:p
   Namespace    , wordprocessingml (wml.xsd)
   Spec Section , 17.3.1.22


Schema excerpt
--------------

.. highlight:: xml

::

  <xsd:complexType name="CT_P">
    <xsd:sequence>
      <xsd:element name="pPr" type="CT_PPr" minOccurs="0"/>
      <xsd:group   ref="EG_PContent"        minOccurs="0" maxOccurs="unbounded"/>
    </xsd:sequence>
    <xsd:attribute name="rsidRPr"      type="ST_LongHexNumber"/>
    <xsd:attribute name="rsidR"        type="ST_LongHexNumber"/>
    <xsd:attribute name="rsidDel"      type="ST_LongHexNumber"/>
    <xsd:attribute name="rsidP"        type="ST_LongHexNumber"/>
    <xsd:attribute name="rsidRDefault" type="ST_LongHexNumber"/>
  </xsd:complexType>

  <xsd:group name="EG_PContent">  <!-- denormalized -->
    <xsd:choice>
      <xsd:element name="r"               type="CT_R"/>
      <xsd:element name="hyperlink"       type="CT_Hyperlink"/>
      <xsd:element name="fldSimple"       type="CT_SimpleField"/>
      <xsd:element name="sdt"             type="CT_SdtRun"/>
      <xsd:element name="customXml"       type="CT_CustomXmlRun"/>
      <xsd:element name="smartTag"        type="CT_SmartTagRun"/>
      <xsd:element name="dir"             type="CT_DirContentRun"/>
      <xsd:element name="bdo"             type="CT_BdoContentRun"/>
      <xsd:element name="subDoc"          type="CT_Rel"/>
      <xsd:group    ref="EG_RunLevelElts"/>
    </xsd:choice>
  </xsd:group>

  <xsd:group name="EG_RunLevelElts">
    <xsd:choice>
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
      <xsd:group   ref="EG_MathContent" minOccurs="0" maxOccurs="unbounded"/>
    </xsd:choice>
  </xsd:group>

  <xsd:complexType name="CT_R">
    <xsd:sequence>
      <xsd:group ref="EG_RPr"             minOccurs="0"/>
      <xsd:group ref="EG_RunInnerContent" minOccurs="0" maxOccurs="unbounded"/>
    </xsd:sequence>
    <xsd:attribute name="rsidRPr" type="ST_LongHexNumber"/>
    <xsd:attribute name="rsidDel" type="ST_LongHexNumber"/>
    <xsd:attribute name="rsidR"   type="ST_LongHexNumber"/>
  </xsd:complexType>

  <xsd:group name="EG_RunInnerContent">
    <xsd:choice>
      <xsd:element name="t"                     type="CT_Text"/>
      <xsd:element name="tab"                   type="CT_Empty"/>
      <xsd:element name="br"                    type="CT_Br"/>
      <xsd:element name="cr"                    type="CT_Empty"/>
      <xsd:element name="sym"                   type="CT_Sym"/>
      <xsd:element name="ptab"                  type="CT_PTab"/>
      <xsd:element name="softHyphen"            type="CT_Empty"/>
      <xsd:element name="contentPart"           type="CT_Rel"/>
      <xsd:element name="noBreakHyphen"         type="CT_Empty"/>
      <xsd:element name="fldChar"               type="CT_FldChar"/>
      <xsd:element name="instrText"             type="CT_Text"/>
      <xsd:element name="dayShort"              type="CT_Empty"/>
      <xsd:element name="monthShort"            type="CT_Empty"/>
      <xsd:element name="yearShort"             type="CT_Empty"/>
      <xsd:element name="dayLong"               type="CT_Empty"/>
      <xsd:element name="monthLong"             type="CT_Empty"/>
      <xsd:element name="yearLong"              type="CT_Empty"/>
      <xsd:element name="annotationRef"         type="CT_Empty"/>
      <xsd:element name="footnoteReference"     type="CT_FtnEdnRef"/>
      <xsd:element name="footnoteRef"           type="CT_Empty"/>
      <xsd:element name="endnoteReference"      type="CT_FtnEdnRef"/>
      <xsd:element name="endnoteRef"            type="CT_Empty"/>
      <xsd:element name="commentReference"      type="CT_Markup"/>
      <xsd:element name="separator"             type="CT_Empty"/>
      <xsd:element name="continuationSeparator" type="CT_Empty"/>
      <xsd:element name="pgNum"                 type="CT_Empty"/>
      <xsd:element name="object"                type="CT_Object"/>
      <xsd:element name="pict"                  type="CT_Picture"/>
      <xsd:element name="ruby"                  type="CT_Ruby"/>
      <xsd:element name="drawing"               type="CT_Drawing"/>
      <xsd:element name="delText"               type="CT_Text"/>
      <xsd:element name="delInstrText"          type="CT_Text"/>
      <xsd:element name="lastRenderedPageBreak" type="CT_Empty"/>
    </xsd:choice>
  </xsd:group>

  <xsd:complexType name="CT_Text">
    <xsd:simpleContent>
      <xsd:extension base="s:ST_String">
        <xsd:attribute ref="xml:space" use="optional"/>
      </xsd:extension>
    </xsd:simpleContent>
  </xsd:complexType>
