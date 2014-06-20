
Sections
========

Word supports the notion of a *section*, having distinct page layout settings.
This is how, for example, a document can contain some pages in portrait layout
and others in landscape. Section breaks are implemented completely differently
from line, page, and column breaks. The former adds a ``<w:pPr><w:sectPr>``
element to the last paragraph in the new section. The latter inserts
a ``<w:br>`` element in a run.


Implementation notes
--------------------

Implementing adding a section break should probably wait until after the
ability to set at least a core subset of the section properties. First ones
are probably:

* page size 
* margins

The other thing it will entail is locating the next ``<w:sectPr>`` element in
document order and copying its child elements.

I'm thinking the sequence is:

1. document.sections
2. section page setup properties
3. paragraph.make_section_break() (or whatever, something better perhaps)


Candidate protocol
------------------

The following interactive session demonstrates the proposed protocol for
working with sections::

    >>> sections = document.sections
    >>> sections
    <docx.parts.document.Sections object at 0x1deadbeef>
    >>> len(sections)
    3
    >>> section = sections[-1]  # the sentinel section
    >>> section
    <docx.section.Section object at 0x1deadbeef>
    >>> section.section_start
    WD_SECTION.CONTINUOUS (0)
    >>> page_setup = section.page_setup
    >>> page_setup
    <docx.section.PageSetup object at 0x1deadbeef>
    >>> page_setup.page_width
    7772400  # Inches(8.5)
    >>> page_setup.page_height
    10058400  # Inches(11)
    >>> page_setup.orientation
    WD_ORIENT.PORTRAIT
    >>> page_setup.left_margin  # and .right_, .top_, .bottom_
    914400
    >>> page_setup.header_distance  # and .footer_distance
    457200  # Inches(0.5)
    >>> page_setup.gutter
    0


Word behavior
-------------

When inserting a section break in Word, there is no dialog box presented and no
parameters are supplied. Word simply copies the section details from the
current section (the next ``<w:sectPr>`` element in the document) to provide
the starting point. Experimentation would be required to determine exactly what
items are copied, but it at least includes the page size, margins, and column
spacing.


Enumerations
------------

* `WdSectionStart Enumeration on MSDN`_

.. _WdSectionStart Enumeration on MSDN:
   http://msdn.microsoft.com/en-us/library/office/bb238171.aspx

::

    @alias(WD_SECTION)
    class WD_SECTION_START(Enumeration):

CONTINUOUS (0)
    Continuous section break.

EVENPAGE (3)
    Even pages section break.

NEWCOLUMN (1)
    New column section break.

NEWPAGE (2)
    New page section break.

ODDPAGE (4)
    Odd pages section break.


* `WdOrientation Enumeration on MSDN`_

.. _WdOrientation Enumeration on MSDN:
   http://msdn.microsoft.com/en-us/library/office/ff837902.aspx

::

    @alias(WD_ORIENT)
    class WD_ORIENTATION(Enumeration):

LANDSCAPE (1)
    Landscape orientation.

PORTRAIT (0)
    Portrait orientation.


Specimen XML
------------

.. highlight:: xml

Inserting a section break (next page) produces this XML::

    <w:p>
      <w:pPr>
        <w:sectPr>
          <w:type w:val="oddPage"/>
          <w:pgSz w:w="12240" w:h="15840"/>
          <w:pgMar w:top="1440" w:right="1800" w:bottom="1440" w:left="1800" w:header="720" w:footer="720" w:gutter="0"/>
          <w:cols w:space="720"/>
          <w:docGrid w:linePitch="360"/>
        </w:sectPr>
      </w:pPr>
      <w:r>
        <w:t>Text before section break insertion point}</w:t>
      </w:r>
    </w:p>


Schema excerpt
--------------

.. highlight:: xml

::

  <xsd:complexType name="CT_PPr">  <!-- denormalized -->
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
      <xsd:element name="cnfStyle"            type="CT_Cnf"              minOccurs="0"/>
      <xsd:element name="rPr"                 type="CT_ParaRPr"          minOccurs="0"/>
      <xsd:element name="sectPr"              type="CT_SectPr"           minOccurs="0"/>
      <xsd:element name="pPrChange"           type="CT_PPrChange"        minOccurs="0"/>
    </xsd:sequence>
  </xsd:complexType>

  <xsd:complexType name="CT_SectPr">  <!-- denormalized -->
    <xsd:sequence>
      <xsd:choice minOccurs="0" maxOccurs="6"/>
        <xsd:element name="headerReference" type="CT_HdrFtrRef"/>
        <xsd:element name="footerReference" type="CT_HdrFtrRef"/>
      </xsd:choice>
      <xsd:element name="footnotePr"      type="CT_FtnProps"      minOccurs="0"/>
      <xsd:element name="endnotePr"       type="CT_EdnProps"      minOccurs="0"/>
      <xsd:element name="type"            type="CT_SectType"      minOccurs="0"/>
      <xsd:element name="pgSz"            type="CT_PageSz"        minOccurs="0"/>
      <xsd:element name="pgMar"           type="CT_PageMar"       minOccurs="0"/>
      <xsd:element name="paperSrc"        type="CT_PaperSource"   minOccurs="0"/>
      <xsd:element name="pgBorders"       type="CT_PageBorders"   minOccurs="0"/>
      <xsd:element name="lnNumType"       type="CT_LineNumber"    minOccurs="0"/>
      <xsd:element name="pgNumType"       type="CT_PageNumber"    minOccurs="0"/>
      <xsd:element name="cols"            type="CT_Columns"       minOccurs="0"/>
      <xsd:element name="formProt"        type="CT_OnOff"         minOccurs="0"/>
      <xsd:element name="vAlign"          type="CT_VerticalJc"    minOccurs="0"/>
      <xsd:element name="noEndnote"       type="CT_OnOff"         minOccurs="0"/>
      <xsd:element name="titlePg"         type="CT_OnOff"         minOccurs="0"/>
      <xsd:element name="textDirection"   type="CT_TextDirection" minOccurs="0"/>
      <xsd:element name="bidi"            type="CT_OnOff"         minOccurs="0"/>
      <xsd:element name="rtlGutter"       type="CT_OnOff"         minOccurs="0"/>
      <xsd:element name="docGrid"         type="CT_DocGrid"       minOccurs="0"/>
      <xsd:element name="printerSettings" type="CT_Rel"           minOccurs="0"/>
      <xsd:element name="sectPrChange"    type="CT_SectPrChange"  minOccurs="0"/>
    </xsd:sequence>
    <xsd:attribute name="rsidRPr"  type="ST_LongHexNumber"/>
    <xsd:attribute name="rsidDel"  type="ST_LongHexNumber"/>
    <xsd:attribute name="rsidR"    type="ST_LongHexNumber"/>
    <xsd:attribute name="rsidSect" type="ST_LongHexNumber"/>
  </xsd:complexType>

  <xsd:complexType name="CT_HdrFtrRef">
    <xsd:attribute  ref="r:id"                  use="required"/>
    <xsd:attribute name="type" type="ST_HdrFtr" use="required"/>
  </xsd:complexType>

  <xsd:simpleType name="ST_HdrFtr">
    <xsd:restriction base="xsd:string">
      <xsd:enumeration value="even"/>
      <xsd:enumeration value="default"/>
      <xsd:enumeration value="first"/>
    </xsd:restriction>
  </xsd:simpleType>

  <xsd:complexType name="CT_SectType">
    <xsd:attribute name="val" type="ST_SectionMark"/>
  </xsd:complexType>

  <xsd:simpleType name="ST_SectionMark">
    <xsd:restriction base="xsd:string">
      <xsd:enumeration value="nextPage"/>
      <xsd:enumeration value="nextColumn"/>
      <xsd:enumeration value="continuous"/>
      <xsd:enumeration value="evenPage"/>
      <xsd:enumeration value="oddPage"/>
    </xsd:restriction>
  </xsd:simpleType>

  <xsd:complexType name="CT_PageSz">
    <xsd:attribute name="w"      type="s:ST_TwipsMeasure"/>
    <xsd:attribute name="h"      type="s:ST_TwipsMeasure"/>
    <xsd:attribute name="orient" type="ST_PageOrientation"/>
    <xsd:attribute name="code"   type="ST_DecimalNumber"/>
  </xsd:complexType>

  <xsd:simpleType name="ST_PageOrientation">
    <xsd:restriction base="xsd:string">
      <xsd:enumeration value="portrait"/>
      <xsd:enumeration value="landscape"/>
    </xsd:restriction>
  </xsd:simpleType>

  <xsd:complexType name="CT_PageMar">
    <xsd:attribute name="top"    type="ST_SignedTwipsMeasure" use="required"/>
    <xsd:attribute name="right"  type="s:ST_TwipsMeasure"     use="required"/>
    <xsd:attribute name="bottom" type="ST_SignedTwipsMeasure" use="required"/>
    <xsd:attribute name="left"   type="s:ST_TwipsMeasure"     use="required"/>
    <xsd:attribute name="header" type="s:ST_TwipsMeasure"     use="required"/>
    <xsd:attribute name="footer" type="s:ST_TwipsMeasure"     use="required"/>
    <xsd:attribute name="gutter" type="s:ST_TwipsMeasure"     use="required"/>
  </xsd:complexType>

  <xsd:simpleType name="ST_SignedTwipsMeasure">
    <xsd:union memberTypes="xsd:integer s:ST_UniversalMeasure"/>
  </xsd:simpleType>

  <xsd:complexType name="CT_Columns">
    <xsd:sequence minOccurs="0">
      <xsd:element name="col" type="CT_Column" maxOccurs="45"/>
    </xsd:sequence>
      <xsd:attribute name="equalWidth" type="s:ST_OnOff"/>
      <xsd:attribute name="space"      type="s:ST_TwipsMeasure"/>
      <xsd:attribute name="num"        type="ST_DecimalNumber"/>
      <xsd:attribute name="sep"        type="s:ST_OnOff"/>
  </xsd:complexType>

  <xsd:complexType name="CT_Column">
    <xsd:attribute name="w"     type="s:ST_TwipsMeasure"/>
    <xsd:attribute name="space" type="s:ST_TwipsMeasure"/>
  </xsd:complexType>
