
Table Properties
================


Alignment
---------

Word allows a table to be aligned between the page margins either left,
right, or center.

The read/write :attr:`Table.alignment` property specifies the alignment for
a table::

    >>> table = document.add_table(rows=2, cols=2)
    >>> table.alignment
    None
    >>> table.alignment = WD_TABLE_ALIGNMENT.RIGHT
    >>> table.alignment
    RIGHT (2)


Autofit
-------

Word has two algorithms for laying out a table, *fixed-width* or `autofit`.
The default is autofit. Word will adjust column widths in an autofit table
based on cell contents. A fixed-width table retains its column widths
regardless of the contents. Either algorithm will adjust column widths
proportionately when total table width exceeds page width.

The read/write :attr:`Table.allow_autofit` property specifies which algorithm
is used::

    >>> table = document.add_table(rows=2, cols=2)
    >>> table.allow_autofit
    True
    >>> table.allow_autofit = False
    >>> table.allow_autofit
    False


Specimen XML
------------

.. highlight:: xml

The following XML represents a 2x2 table::

    <w:tbl>
      <w:tblPr>
        <w:tblStyle w:val="TableGrid"/>
        <w:tblW w:type="auto" w:w="0"/>
        <w:jc w:val="right"/>
        <w:tblLook w:firstColumn="1" w:firstRow="1" w:lastColumn="0"
                   w:lastRow="0" w:noHBand="0" w:noVBand="1" w:val="04A0"/>
      </w:tblPr>
      <w:tblGrid>
        <w:gridCol w:w="4788"/>
        <w:gridCol w:w="4788"/>
      </w:tblGrid>
      <w:tr>
        <w:tc/>
          <w:tcPr>
            <w:tcW w:type="dxa" w:w="4788"/>
          </w:tcPr>
          <w:p/>
        </w:tc>
        <w:tc>
          <w:tcPr>
            <w:tcW w:type="dxa" w:w="4788"/>
          </w:tcPr>
          <w:p/>
        </w:tc>
      </w:tr>
      <w:tr>
        <w:tc>
          <w:tcPr>
            <w:tcW w:type="dxa" w:w="4788"/>
          </w:tcPr>
          <w:p/>
        </w:tc>
        <w:tc>
          <w:tcPr>
            <w:tcW w:type="dxa" w:w="4788"/>
          </w:tcPr>
          <w:p/>
        </w:tc>
      </w:tr>
    </w:tbl>


Layout behavior
---------------

Auto-layout causes actual column widths to be both unpredictable and
unstable. Changes to the content can make the table layout shift.


Semantics of CT_TblWidth element
--------------------------------

e.g. ``tcW``::

    <w:tcW w:w="42.4mm"/>

    <w:tcW w:w="1800" w:type="dxa"/>

    <w:tcW w:w="20%" w:type="pct"/>

    <w:tcW w:w="0" w:type="auto"/>

    <w:tcW w:type="nil"/>


    ST_MeasurementOrPercent
    |
    +-- ST_DecimalNumberOrPercent
    |   |
    |   +-- ST_UnqualifiedPercentage
    |   |   |
    |   |   +-- XsdInteger e.g. '1440'
    |   |
    |   +-- ST_Percentage e.g. '-07.43%'
    |
    +-- ST_UniversalMeasure  e.g. '-04.34mm'


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

  <xsd:complexType name="CT_TblPr">  <!-- denormalized -->
    <xsd:sequence>
      <xsd:element name="tblStyle"            type="CT_String"        minOccurs="0"/>
      <xsd:element name="tblpPr"              type="CT_TblPPr"        minOccurs="0"/>
      <xsd:element name="tblOverlap"          type="CT_TblOverlap"    minOccurs="0"/>
      <xsd:element name="bidiVisual"          type="CT_OnOff"         minOccurs="0"/>
      <xsd:element name="tblStyleRowBandSize" type="CT_DecimalNumber" minOccurs="0"/>
      <xsd:element name="tblStyleColBandSize" type="CT_DecimalNumber" minOccurs="0"/>
      <xsd:element name="tblW"                type="CT_TblWidth"      minOccurs="0"/>
      <xsd:element name="jc"                  type="CT_JcTable"       minOccurs="0"/>
      <xsd:element name="tblCellSpacing"      type="CT_TblWidth"      minOccurs="0"/>
      <xsd:element name="tblInd"              type="CT_TblWidth"      minOccurs="0"/>
      <xsd:element name="tblBorders"          type="CT_TblBorders"    minOccurs="0"/>
      <xsd:element name="shd"                 type="CT_Shd"           minOccurs="0"/>
      <xsd:element name="tblLayout"           type="CT_TblLayoutType" minOccurs="0"/>
      <xsd:element name="tblCellMar"          type="CT_TblCellMar"    minOccurs="0"/>
      <xsd:element name="tblLook"             type="CT_TblLook"       minOccurs="0"/>
      <xsd:element name="tblCaption"          type="CT_String"        minOccurs="0"/>
      <xsd:element name="tblDescription"      type="CT_String"        minOccurs="0"/>
      <xsd:element name="tblPrChange"         type="CT_TblPrChange"   minOccurs="0"/>
    </xsd:sequence>

  <!-- table alignment --------------------------------- -->

  <xsd:complexType name="CT_JcTable">
    <xsd:attribute name="val" type="ST_JcTable" use="required"/>
  </xsd:complexType>

  <xsd:simpleType name="ST_JcTable">
    <xsd:restriction base="xsd:string">
      <xsd:enumeration value="center"/>
      <xsd:enumeration value="end"/>
      <xsd:enumeration value="left"/>
      <xsd:enumeration value="right"/>
      <xsd:enumeration value="start"/>
    </xsd:restriction>
  </xsd:simpleType>

  <!-- table width ------------------------------------- -->

  <xsd:complexType name="CT_TblWidth">
    <xsd:attribute name="w"    type="ST_MeasurementOrPercent"/>
    <xsd:attribute name="type" type="ST_TblWidth"/>
  </xsd:complexType>

  <xsd:simpleType name="ST_MeasurementOrPercent">
    <xsd:union memberTypes="ST_DecimalNumberOrPercent s:ST_UniversalMeasure"/>
  </xsd:simpleType>

  <xsd:simpleType name="ST_DecimalNumberOrPercent">
    <xsd:union memberTypes="ST_UnqualifiedPercentage s:ST_Percentage"/>
  </xsd:simpleType>

  <xsd:simpleType name="ST_UniversalMeasure">
    <xsd:restriction base="xsd:string">
      <xsd:pattern value="-?[0-9]+(\.[0-9]+)?(mm|cm|in|pt|pc|pi)"/>
    </xsd:restriction>
  </xsd:simpleType>

  <xsd:simpleType name="ST_UnqualifiedPercentage">
    <xsd:restriction base="xsd:integer"/>
  </xsd:simpleType>

  <xsd:simpleType name="ST_Percentage">
    <xsd:restriction base="xsd:string">
      <xsd:pattern value="-?[0-9]+(\.[0-9]+)?%"/>
    </xsd:restriction>
  </xsd:simpleType>

  <xsd:simpleType name="ST_TblWidth">
    <xsd:restriction base="xsd:string">
      <xsd:enumeration value="nil"/>
      <xsd:enumeration value="pct"/>
      <xsd:enumeration value="dxa"/>
      <xsd:enumeration value="auto"/>
    </xsd:restriction>
  </xsd:simpleType>

  <!-- table layout ------------------------------------ -->

  <xsd:complexType name="CT_TblLayoutType">
    <xsd:attribute name="type" type="ST_TblLayoutType"/>
  </xsd:complexType>

  <xsd:simpleType name="ST_TblLayoutType">
    <xsd:restriction base="xsd:string">
      <xsd:enumeration value="fixed"/>
      <xsd:enumeration value="autofit"/>
    </xsd:restriction>
  </xsd:simpleType>

  <!-- table look -------------------------------------- -->

  <xsd:complexType name="CT_TblLook">
    <xsd:attribute name="firstRow"    type="s:ST_OnOff"/>
    <xsd:attribute name="lastRow"     type="s:ST_OnOff"/>
    <xsd:attribute name="firstColumn" type="s:ST_OnOff"/>
    <xsd:attribute name="lastColumn"  type="s:ST_OnOff"/>
    <xsd:attribute name="noHBand"     type="s:ST_OnOff"/>
    <xsd:attribute name="noVBand"     type="s:ST_OnOff"/>
    <xsd:attribute name="val"         type="ST_ShortHexNumber"/>
  </xsd:complexType>
