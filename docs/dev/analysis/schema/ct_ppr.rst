##########
``CT_PPr``
##########

.. highlight:: xml

.. csv-table::
   :header-rows: 0
   :stub-columns: 1
   :widths: 15, 50

   Schema Name  , CT_PPr
   Spec Name    , Paragraph Properties
   Tag(s)       , w:pPr
   Namespace    , wordprocessingml (wml.xsd)
   Spec Section , 17.3.1.26


Analysis
========



attributes
^^^^^^^^^^

None.


child elements
^^^^^^^^^^^^^^

=========  ===  ================
name        #   type
=========  ===  ================
xyz         ?   CT_abc
abc         ?   CT_TextListStyle
p           ?   CT_TextParagraph
=========  ===  ================


Spec text
^^^^^^^^^

    This element specifies a set of paragraph properties which shall be applied
    to the contents of the parent paragraph after all style/numbering/table
    properties have been applied to the text. These properties are defined as
    direct formatting, since they are directly applied to the paragraph and
    supersede any formatting from styles.

    Consider a paragraph which should have a set of paragraph formatting
    properties. This set of properties is specified in the paragraph properties
    as follows::

        <w:p>
          <w:pPr>
            <w:pBdr>
              <w:bottom w:val="single" w:sz="8" w:space="4" w:color="4F81BD"/>
            </w:pBdr>
            <w:spacing w:after="300"/>
            <w:contextualSpacing/>
          </w:pPr>
        </w:p>

    The pPr element specifies the properties which are applied to the current
    paragraph - in this case, a bottom paragraph border using the bottom
    element (§17.3.1.7), spacing after the paragraph using the spacing element
    (§17.3.1.33), and that spacing should be ignored for paragraphs above/below
    of the same style using the contextualSpacing element (§17.3.1.9).


Schema excerpt
^^^^^^^^^^^^^^

::

  <xsd:complexType name="CT_PPr">
    <xsd:complexContent>
      <xsd:extension base="CT_PPrBase">
        <xsd:sequence>
          <xsd:element name="rPr" type="CT_ParaRPr" minOccurs="0"/>
          <xsd:element name="sectPr" type="CT_SectPr" minOccurs="0"/>
          <xsd:element name="pPrChange" type="CT_PPrChange" minOccurs="0"/>
        </xsd:sequence>
      </xsd:extension>
    </xsd:complexContent>
  </xsd:complexType>

  <xsd:complexType name="CT_PPrBase">
    <xsd:sequence>
      <xsd:element name="pStyle"              type="CT_String"           minOccurs="0"/>
      <xsd:element name="keepNext"            type="CT_OnOff"            minOccurs="0"/>
      <xsd:element name="keepLines"           type="CT_OnOff"            minOccurs="0"/>
      <xsd:element name="pageBreakBefore"     type="CT_OnOff"            minOccurs="0"/>
      <xsd:element name="framePr"             type="CT_FramePr"          minOccurs="0"/>
      <xsd:element name="widowControl"        type="CT_OnOff"            minOccurs="0"/>
      <xsd:element name="numPr"               type="CT_NumPr"            minOccurs="0"/>
      <xsd:element name="suppressLineNumbers" type="CT_OnOff"            minOccurs="0"/>
      <xsd:element name="pBdr"                type="CT_PBdr"             minOccurs="0"/>
      <xsd:element name="shd"                 type="CT_Shd"              minOccurs="0"/>
      <xsd:element name="tabs"                type="CT_Tabs"             minOccurs="0"/>
      <xsd:element name="suppressAutoHyphens" type="CT_OnOff"            minOccurs="0"/>
      <xsd:element name="kinsoku"             type="CT_OnOff"            minOccurs="0"/>
      <xsd:element name="wordWrap"            type="CT_OnOff"            minOccurs="0"/>
      <xsd:element name="overflowPunct"       type="CT_OnOff"            minOccurs="0"/>
      <xsd:element name="topLinePunct"        type="CT_OnOff"            minOccurs="0"/>
      <xsd:element name="autoSpaceDE"         type="CT_OnOff"            minOccurs="0"/>
      <xsd:element name="autoSpaceDN"         type="CT_OnOff"            minOccurs="0"/>
      <xsd:element name="bidi"                type="CT_OnOff"            minOccurs="0"/>
      <xsd:element name="adjustRightInd"      type="CT_OnOff"            minOccurs="0"/>
      <xsd:element name="snapToGrid"          type="CT_OnOff"            minOccurs="0"/>
      <xsd:element name="spacing"             type="CT_Spacing"          minOccurs="0"/>
      <xsd:element name="ind"                 type="CT_Ind"              minOccurs="0"/>
      <xsd:element name="contextualSpacing"   type="CT_OnOff"            minOccurs="0"/>
      <xsd:element name="mirrorIndents"       type="CT_OnOff"            minOccurs="0"/>
      <xsd:element name="suppressOverlap"     type="CT_OnOff"            minOccurs="0"/>
      <xsd:element name="jc"                  type="CT_Jc"               minOccurs="0"/>
      <xsd:element name="textDirection"       type="CT_TextDirection"    minOccurs="0"/>
      <xsd:element name="textAlignment"       type="CT_TextAlignment"    minOccurs="0"/>
      <xsd:element name="textboxTightWrap"    type="CT_TextboxTightWrap" minOccurs="0"/>
      <xsd:element name="outlineLvl"          type="CT_DecimalNumber"    minOccurs="0"/>
      <xsd:element name="divId"               type="CT_DecimalNumber"    minOccurs="0"/>
      <xsd:element name="cnfStyle"            type="CT_Cnf"              minOccurs="0" maxOccurs="1"/>
    </xsd:sequence>
  </xsd:complexType>

  <xsd:complexType name="CT_FramePr">
    <xsd:attribute name="dropCap"    type="ST_DropCap"            use="optional"/>
    <xsd:attribute name="lines"      type="ST_DecimalNumber"      use="optional"/>
    <xsd:attribute name="w"          type="s:ST_TwipsMeasure"     use="optional"/>
    <xsd:attribute name="h"          type="s:ST_TwipsMeasure"     use="optional"/>
    <xsd:attribute name="vSpace"     type="s:ST_TwipsMeasure"     use="optional"/>
    <xsd:attribute name="hSpace"     type="s:ST_TwipsMeasure"     use="optional"/>
    <xsd:attribute name="wrap"       type="ST_Wrap"               use="optional"/>
    <xsd:attribute name="hAnchor"    type="ST_HAnchor"            use="optional"/>
    <xsd:attribute name="vAnchor"    type="ST_VAnchor"            use="optional"/>
    <xsd:attribute name="x"          type="ST_SignedTwipsMeasure" use="optional"/>
    <xsd:attribute name="xAlign"     type="s:ST_XAlign"           use="optional"/>
    <xsd:attribute name="y"          type="ST_SignedTwipsMeasure" use="optional"/>
    <xsd:attribute name="yAlign"     type="s:ST_YAlign"           use="optional"/>
    <xsd:attribute name="hRule"      type="ST_HeightRule"         use="optional"/>
    <xsd:attribute name="anchorLock" type="s:ST_OnOff"            use="optional"/>
  </xsd:complexType>

  <xsd:complexType name="CT_Ind">
    <xsd:attribute name="start"          type="ST_SignedTwipsMeasure" use="optional"/>
    <xsd:attribute name="startChars"     type="ST_DecimalNumber"      use="optional"/>
    <xsd:attribute name="end"            type="ST_SignedTwipsMeasure" use="optional"/>
    <xsd:attribute name="endChars"       type="ST_DecimalNumber"      use="optional"/>
    <xsd:attribute name="left"           type="ST_SignedTwipsMeasure" use="optional"/>
    <xsd:attribute name="leftChars"      type="ST_DecimalNumber"      use="optional"/>
    <xsd:attribute name="right"          type="ST_SignedTwipsMeasure" use="optional"/>
    <xsd:attribute name="rightChars"     type="ST_DecimalNumber"      use="optional"/>
    <xsd:attribute name="hanging"        type="s:ST_TwipsMeasure"     use="optional"/>
    <xsd:attribute name="hangingChars"   type="ST_DecimalNumber"      use="optional"/>
    <xsd:attribute name="firstLine"      type="s:ST_TwipsMeasure"     use="optional"/>
    <xsd:attribute name="firstLineChars" type="ST_DecimalNumber"      use="optional"/>
  </xsd:complexType>

  <xsd:complexType name="CT_Jc">
    <xsd:attribute name="val" type="ST_Jc" use="required"/>
  </xsd:complexType>

  <xsd:complexType name="CT_OnOff">
    <xsd:attribute name="val" type="s:ST_OnOff"/>
  </xsd:complexType>

  <xsd:complexType name="CT_Spacing">
    <xsd:attribute name="before"            type="s:ST_TwipsMeasure"     use="optional"/>
    <xsd:attribute name="beforeLines"       type="ST_DecimalNumber"      use="optional"/>
    <xsd:attribute name="beforeAutospacing" type="s:ST_OnOff"            use="optional"/>
    <xsd:attribute name="after"             type="s:ST_TwipsMeasure"     use="optional"/>
    <xsd:attribute name="afterLines"        type="ST_DecimalNumber"      use="optional"/>
    <xsd:attribute name="afterAutospacing"  type="s:ST_OnOff"            use="optional"/>
    <xsd:attribute name="line"              type="ST_SignedTwipsMeasure" use="optional"/>
    <xsd:attribute name="lineRule"          type="ST_LineSpacingRule"    use="optional"/>
  </xsd:complexType>

  <xsd:complexType name="CT_String">
    <xsd:attribute name="val" type="s:ST_String" use="required"/>
  </xsd:complexType>

  <xsd:complexType name="CT_Tabs">
    <xsd:sequence>
      <xsd:element name="tab" type="CT_TabStop" minOccurs="1" maxOccurs="unbounded"/>
    </xsd:sequence>
  </xsd:complexType>

  <xsd:simpleType name="ST_OnOff">
    <xsd:union memberTypes="xsd:boolean ST_OnOff1"/>
  </xsd:simpleType>

  <xsd:simpleType name="ST_OnOff1">
    <xsd:restriction base="xsd:string">
      <xsd:enumeration value="on"/>
      <xsd:enumeration value="off"/>
    </xsd:restriction>
  </xsd:simpleType>
