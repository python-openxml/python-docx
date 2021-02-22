
Table Row
=========

A table row has certain properties such as height.


Row.height
----------

Candidate protocol::

    >>> from docx.enum.table import WD_ROW_HEIGHT
    >>> row = table.add_row()
    >>> row
    <docx.table._Row object at 0x...>
    >>> row.height_rule
    None
    >>> row.height_rule = WD_ROW_HEIGHT.EXACTLY
    >>> row.height
    None
    >>> row.height = Pt(24)


MS API
------

https://msdn.microsoft.com/en-us/library/office/ff193915.aspx

Methods
~~~~~~~

* Delete()
* SetHeight()
* SetLeftIndent()

Properties
~~~~~~~~~~

* Alignment
* AllowBreakAcrossPages
* Borders
* Cells
* HeadingFormat
* Height
* HeightRule
* Index
* IsFirst
* IsLast
* LeftIndent
* NestingLevel
* Next
* Previous
* Shading
* SpaceBetweenColumns


WD_ROW_HEIGHT_RULE Enumeration
------------------------------

Alias: WD_ROW_HEIGHT

* wdRowHeightAtLeast (1) The row height is at least a minimum specified value.
* wdRowHeightAuto (0) The row height is adjusted to accommodate the tallest
  value in the row.
* wdRowHeightExactly (2) The row height is an exact value.


Schema Definitions
------------------

.. highlight:: xml

::

  <xsd:complexType name="CT_Tbl">  <!-- denormalized -->
    <xsd:sequence>
      <xsd:group    ref="EG_RangeMarkupElements"        minOccurs="0" maxOccurs="unbounded"/>
      <xsd:element name="tblPr"       type="CT_TblPr"/>
      <xsd:element name="tblGrid"     type="CT_TblGrid"/>
      <xsd:choice                                       minOccurs="0" maxOccurs="unbounded">
        <xsd:element name="tr"        type="CT_Row"/>
        <xsd:element name="customXml" type="CT_CustomXmlRow"/>
        <xsd:element name="sdt"       type="CT_SdtRow"/>
        <xsd:group    ref="EG_RunLevelElts"             minOccurs="0" maxOccurs="unbounded"/>
      </xsd:choice>
    </xsd:sequence>
  </xsd:complexType>

  <xsd:complexType name="CT_Row">
    <xsd:sequence>
      <xsd:element name="tblPrEx" type="CT_TblPrEx" minOccurs="0"/>
      <xsd:element name="trPr"    type="CT_TrPr"    minOccurs="0"/>
      <xsd:group    ref="EG_ContentCellContent"     minOccurs="0" maxOccurs="unbounded"/>
    </xsd:sequence>
    <xsd:attribute name="rsidRPr" type="ST_LongHexNumber"/>
    <xsd:attribute name="rsidR"   type="ST_LongHexNumber"/>
    <xsd:attribute name="rsidDel" type="ST_LongHexNumber"/>
    <xsd:attribute name="rsidTr"  type="ST_LongHexNumber"/>
  </xsd:complexType>

  <xsd:complexType name="CT_TrPr">  <!-- denormalized -->
    <xsd:sequence>
      <xsd:element name="cnfStyle"       type="CT_Cnf"           minOccurs="0"/>
      <xsd:element name="divId"          type="CT_DecimalNumber" minOccurs="0"/>
      <xsd:element name="gridBefore"     type="CT_DecimalNumber" minOccurs="0"/>
      <xsd:element name="gridAfter"      type="CT_DecimalNumber" minOccurs="0"/>
      <xsd:element name="wBefore"        type="CT_TblWidth"      minOccurs="0"/>
      <xsd:element name="wAfter"         type="CT_TblWidth"      minOccurs="0"/>
      <xsd:element name="cantSplit"      type="CT_OnOff"         minOccurs="0"/>
      <xsd:element name="trHeight"       type="CT_Height"        minOccurs="0"/>
      <xsd:element name="tblHeader"      type="CT_OnOff"         minOccurs="0"/>
      <xsd:element name="tblCellSpacing" type="CT_TblWidth"      minOccurs="0"/>
      <xsd:element name="jc"             type="CT_JcTable"       minOccurs="0"/>
      <xsd:element name="hidden"         type="CT_OnOff"         minOccurs="0"/>
      <xsd:element name="ins"            type="CT_TrackChange"   minOccurs="0"/>
      <xsd:element name="del"            type="CT_TrackChange"   minOccurs="0"/>
      <xsd:element name="trPrChange"     type="CT_TrPrChange"    minOccurs="0"/>
    </xsd:sequence>
  </xsd:complexType>

  <xsd:complexType name="CT_Height">
    <xsd:attribute name="val"   type="s:ST_TwipsMeasure"/>
    <xsd:attribute name="hRule" type="ST_HeightRule"/>
  </xsd:complexType>

  <xsd:simpleType name="ST_HeightRule">
    <xsd:restriction base="xsd:string">
      <xsd:enumeration value="auto"/>
      <xsd:enumeration value="exact"/>
      <xsd:enumeration value="atLeast"/>
    </xsd:restriction>
  </xsd:simpleType>
