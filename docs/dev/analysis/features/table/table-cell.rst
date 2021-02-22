
Table Cell
==========

All content in a table is contained in a cell. A cell also has several
properties affecting its size, appearance, and how the content it contains is
formatted.


Candidate protocol
------------------

Cell.vertical_alignment::

    >>> from docx.enum.table import WD_CELL_ALIGN_VERTICAL
    >>> cell = table.add_row().cells[0]
    >>> cell
    <docx.table._Cell object at 0x...>
    >>> cell.vertical_alignment
    None
    >>> cell.vertical_alignment = WD_CELL_ALIGN_VERTICAL.CENTER
    >>> print(cell.vertical_alignment)
    CENTER (1)


MS API - Partial Summary
------------------------

* Merge()
* Split()
* Borders
* BottomPadding (and Left, Right, Top)
* Column
* ColumnIndex
* FitText
* Height
* HeightRule (one of WdRowHeightRule_ enumeration)
* Preferred Width
* Row
* RowIndex
* Shading
* Tables
* VerticalAlignment
* Width
* WordWrap


WD_ALIGN_VERTICAL Enumeration
---------------------------------

wdAlignVerticalBoth (101)
    This is an option in the OpenXml spec, but not in Word itself. It's not
    clear what Word behavior this setting produces. If you find out please let
    us know and we'll update the documentation. Otherwise, probably best to
    avoid this option.

wdAlignVerticalBottom (3)
    Text is aligned to the bottom border of the cell.

wdAlignVerticalCenter (1)
    Text is aligned to the center of the cell.

wdAlignVerticalTop (0)
    Text is aligned to the top border of the cell.


Specimen XML
------------

.. highlight:: xml

::

  <w:tc>
    <w:tcPr>
      <w:tcW w:w="7038" w:type="dxa"/>
      <w:vAlign w:val="bottom"/>
    </w:tcPr>
    <w:p>
      <w:pPr>
        <w:pStyle w:val="ListBullet"/>
      </w:pPr>
      <w:r>
        <w:t>Amy earned her BA in American Studies</w:t>
      </w:r>
    </w:p>
  </w:tc>


Schema Definitions
------------------

.. highlight:: xml

::

  <xsd:complexType name="CT_Tc">  <!-- denormalized -->
    <xsd:sequence>
      <xsd:element name="tcPr" type="CT_TcPr" minOccurs="0"/>
      <xsd:choice minOccurs="1" maxOccurs="unbounded">
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
    </xsd:sequence>
    <xsd:attribute name="id" type="s:ST_String" use="optional"/>
  </xsd:complexType>

  <xsd:complexType name="CT_TcPr">  <!-- denormalized -->
    <xsd:sequence>
      <xsd:element name="cnfStyle"             type="CT_Cnf"           minOccurs="0"/>
      <xsd:element name="tcW"                  type="CT_TblWidth"      minOccurs="0"/>
      <xsd:element name="gridSpan"             type="CT_DecimalNumber" minOccurs="0"/>
      <xsd:element name="hMerge"               type="CT_HMerge"        minOccurs="0"/>
      <xsd:element name="vMerge"               type="CT_VMerge"        minOccurs="0"/>
      <xsd:element name="tcBorders"            type="CT_TcBorders"     minOccurs="0"/>
      <xsd:element name="shd"                  type="CT_Shd"           minOccurs="0"/>
      <xsd:element name="noWrap"               type="CT_OnOff"         minOccurs="0"/>
      <xsd:element name="tcMar"                type="CT_TcMar"         minOccurs="0"/>
      <xsd:element name="textDirection"        type="CT_TextDirection" minOccurs="0"/>
      <xsd:element name="tcFitText"            type="CT_OnOff"         minOccurs="0"/>
      <xsd:element name="vAlign"               type="CT_VerticalJc"    minOccurs="0"/>
      <xsd:element name="hideMark"             type="CT_OnOff"         minOccurs="0"/>
      <xsd:element name="headers"              type="CT_Headers"       minOccurs="0"/>
      <xsd:choice                                                      minOccurs="0"/>
        <xsd:element name="cellIns"            type="CT_TrackChange"/>
        <xsd:element name="cellDel"            type="CT_TrackChange"/>
        <xsd:element name="cellMerge"          type="CT_CellMergeTrackChange"/>
      </xsd:choice>
      <xsd:element name="tcPrChange"           type="CT_TcPrChange"    minOccurs="0"/>
    </xsd:sequence>
  </xsd:complexType>

  <xsd:complexType name="CT_TblWidth">
    <xsd:attribute name="w"    type="ST_MeasurementOrPercent"/>
    <xsd:attribute name="type" type="ST_TblWidth"/>
  </xsd:complexType>

  <xsd:complexType name="CT_VerticalJc">
    <xsd:attribute name="val" type="ST_VerticalJc" use="required"/>
  </xsd:complexType>

  <!-- simple types -->

  <xsd:simpleType name="ST_DecimalNumberOrPercent">
    <xsd:union memberTypes="ST_UnqualifiedPercentage s:ST_Percentage"/>
  </xsd:simpleType>

  <xsd:simpleType name="ST_MeasurementOrPercent">
    <xsd:union memberTypes="ST_DecimalNumberOrPercent s:ST_UniversalMeasure"/>
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

  <xsd:simpleType name="ST_UniversalMeasure">
    <xsd:restriction base="xsd:string">
      <xsd:pattern value="-?[0-9]+(\.[0-9]+)?(mm|cm|in|pt|pc|pi)"/>
    </xsd:restriction>
  </xsd:simpleType>

  <xsd:simpleType name="ST_UnqualifiedPercentage">
    <xsd:restriction base="xsd:integer"/>
  </xsd:simpleType>

  <xsd:simpleType name="ST_VerticalJc">
    <xsd:restriction base="xsd:string">
      <xsd:enumeration value="top"/>
      <xsd:enumeration value="center"/>
      <xsd:enumeration value="both"/>
      <xsd:enumeration value="bottom"/>
    </xsd:restriction>
  </xsd:simpleType>


.. _`WdRowHeightRule`:
   http://msdn.microsoft.com/en-us/library/office/ff193620(v=office.15).aspx
