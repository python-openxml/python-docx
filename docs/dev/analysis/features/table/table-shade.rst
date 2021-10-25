
https://docs.microsoft.com/en-us/dotnet/api/documentformat.openxml.wordprocessing.shading?view=openxml-2.8.1

https://docs.microsoft.com/en-us/dotnet/api/documentformat.openxml.wordprocessing.shadingpatternvalues?view=openxml-2.8.1

https://docs.microsoft.com/en-us/office/vba/api/word.wdtextureindex
https://docs.microsoft.com/en-us/dotnet/api/documentformat.openxml.wordprocessing.shadingpatternvalues?view=openxml-2.8.1

Schema Definitions
------------------

.. highlight:: xml

::

  <xsd:complexType name="CT_Shd">
    <xsd:attribute name="val" type="ST_Shd" use="required"/>
    <xsd:attribute name="color" type="ST_HexColor" use="optional"/>
    <xsd:attribute name="themeColor" type="ST_ThemeColor" use="optional"/>
    <xsd:attribute name="themeTint" type="ST_UcharHexNumber" use="optional"/>
    <xsd:attribute name="themeShade" type="ST_UcharHexNumber" use="optional"/>
    <xsd:attribute name="fill" type="ST_HexColor" use="optional"/>
    <xsd:attribute name="themeFill" type="ST_ThemeColor" use="optional"/>
    <xsd:attribute name="themeFillTint" type="ST_UcharHexNumber" use="optional"/>
    <xsd:attribute name="themeFillShade" type="ST_UcharHexNumber" use="optional"/>
  </xsd:complexType>


<xsd:complexType name="CT_PPrBase">
    <xsd:sequence>
      <xsd:element name="pStyle" type="CT_String" minOccurs="0"/>
      <xsd:element name="keepNext" type="CT_OnOff" minOccurs="0"/>
      <xsd:element name="keepLines" type="CT_OnOff" minOccurs="0"/>
      <xsd:element name="pageBreakBefore" type="CT_OnOff" minOccurs="0"/>
      <xsd:element name="framePr" type="CT_FramePr" minOccurs="0"/>
      <xsd:element name="widowControl" type="CT_OnOff" minOccurs="0"/>
      <xsd:element name="numPr" type="CT_NumPr" minOccurs="0"/>
      <xsd:element name="suppressLineNumbers" type="CT_OnOff" minOccurs="0"/>
      <xsd:element name="pBdr" type="CT_PBdr" minOccurs="0"/>
      <xsd:element name="shd" type="CT_Shd" minOccurs="0"/>
      <xsd:element name="tabs" type="CT_Tabs" minOccurs="0"/>
      <xsd:element name="suppressAutoHyphens" type="CT_OnOff" minOccurs="0"/>
      <xsd:element name="kinsoku" type="CT_OnOff" minOccurs="0"/>
      <xsd:element name="wordWrap" type="CT_OnOff" minOccurs="0"/>
      <xsd:element name="overflowPunct" type="CT_OnOff" minOccurs="0"/>
      <xsd:element name="topLinePunct" type="CT_OnOff" minOccurs="0"/>
      <xsd:element name="autoSpaceDE" type="CT_OnOff" minOccurs="0"/>
      <xsd:element name="autoSpaceDN" type="CT_OnOff" minOccurs="0"/>
      <xsd:element name="bidi" type="CT_OnOff" minOccurs="0"/>
      <xsd:element name="adjustRightInd" type="CT_OnOff" minOccurs="0"/>
      <xsd:element name="snapToGrid" type="CT_OnOff" minOccurs="0"/>
      <xsd:element name="spacing" type="CT_Spacing" minOccurs="0"/>
      <xsd:element name="ind" type="CT_Ind" minOccurs="0"/>
      <xsd:element name="contextualSpacing" type="CT_OnOff" minOccurs="0"/>
      <xsd:element name="mirrorIndents" type="CT_OnOff" minOccurs="0"/>
      <xsd:element name="suppressOverlap" type="CT_OnOff" minOccurs="0"/>
      <xsd:element name="jc" type="CT_Jc" minOccurs="0"/>
      <xsd:element name="textDirection" type="CT_TextDirection" minOccurs="0"/>
      <xsd:element name="textAlignment" type="CT_TextAlignment" minOccurs="0"/>
      <xsd:element name="textboxTightWrap" type="CT_TextboxTightWrap" minOccurs="0"/>
      <xsd:element name="outlineLvl" type="CT_DecimalNumber" minOccurs="0"/>
      <xsd:element name="divId" type="CT_DecimalNumber" minOccurs="0"/>
      <xsd:element name="cnfStyle" type="CT_Cnf" minOccurs="0" maxOccurs="1"/>
    </xsd:sequence>
  </xsd:complexType>


-- New simpletypes:

  <xsd:simpleType name="ST_Shd">
    <xsd:restriction base="xsd:string">
      <xsd:enumeration value="nil"/>
      <xsd:enumeration value="clear"/>
      <xsd:enumeration value="solid"/>
      <xsd:enumeration value="horzStripe"/>
      <xsd:enumeration value="vertStripe"/>
      <xsd:enumeration value="reverseDiagStripe"/>
      <xsd:enumeration value="diagStripe"/>
      <xsd:enumeration value="horzCross"/>
      <xsd:enumeration value="diagCross"/>
      <xsd:enumeration value="thinHorzStripe"/>
      <xsd:enumeration value="thinVertStripe"/>
      <xsd:enumeration value="thinReverseDiagStripe"/>
      <xsd:enumeration value="thinDiagStripe"/>
      <xsd:enumeration value="thinHorzCross"/>
      <xsd:enumeration value="thinDiagCross"/>
      <xsd:enumeration value="pct5"/>
      <xsd:enumeration value="pct10"/>
      <xsd:enumeration value="pct12"/>
      <xsd:enumeration value="pct15"/>
      <xsd:enumeration value="pct20"/>
      <xsd:enumeration value="pct25"/>
      <xsd:enumeration value="pct30"/>
      <xsd:enumeration value="pct35"/>
      <xsd:enumeration value="pct37"/>
      <xsd:enumeration value="pct40"/>
      <xsd:enumeration value="pct45"/>
      <xsd:enumeration value="pct50"/>
      <xsd:enumeration value="pct55"/>
      <xsd:enumeration value="pct60"/>
      <xsd:enumeration value="pct62"/>
      <xsd:enumeration value="pct65"/>
      <xsd:enumeration value="pct70"/>
      <xsd:enumeration value="pct75"/>
      <xsd:enumeration value="pct80"/>
      <xsd:enumeration value="pct85"/>
      <xsd:enumeration value="pct87"/>
      <xsd:enumeration value="pct90"/>
      <xsd:enumeration value="pct95"/>
    </xsd:restriction>
  </xsd:simpleType>  