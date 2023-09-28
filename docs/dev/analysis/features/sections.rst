
Sections
========

Word supports the notion of a `section`, having distinct page layout settings.
This is how, for example, a document can contain some pages in portrait layout
and others in landscape. Section breaks are implemented completely differently
from line, page, and column breaks. The former adds a ``<w:pPr><w:sectPr>``
element to the last paragraph in the new section. The latter inserts
a ``<w:br>`` element in a run.

The last section in a document is specified by a ``<w:sectPr>`` element
appearing as the last child of the ``<w:body>`` element. While this element
is optional, it appears that Word creates it for all files. Since most files
have only a single section, the most common case is where this is the only
``<w:sectPr>`` element.

Additional sections are specified by a ``w:p/w:pPr/w:sectPr`` element in the
last paragraph of the section. Any content in that paragraph is part of the
section defined by its ``<w:sectPr>`` element. The subsequent section begins
with the following paragraph.

When a section break is inserted using the Word UI, the following steps
occur:

1. The next-occurring ``<w:sectPr>`` element is copied and added to the
   current paragraph. (It would be interesting to see what happens when that
   paragraph already has a ``<w:sectPr>`` element.)
2. A new paragraph is inserted after the current paragraph. The text occuring
   after the cursor position is moved to the new paragraph.
3. The start-type (e.g. next page) of the next-occuring ``<w:sectPr>``
   element is changed to reflect the type chosen by the user from the UI.


Word behavior
-------------

* A paragraph containing a section break (<w:sectPr> element) does not
  produce a ¶ glyph in the Word UI.
* The section break indicator/double-line appears directly after the text of
  the paragraph in which the <w:sectPr> appears. If the section break
  paragraph has no text, the indicator line appears immediately after the
  paragraph mark of the prior paragraph.


Before and after analysis
~~~~~~~~~~~~~~~~~~~~~~~~~

.. highlight:: xml

Baseline document containing two paragraphs::

  <w:body>
    <w:p>
      <w:r>
        <w:t>Paragraph 1</w:t>
      </w:r>
    </w:p>
    <w:p>
      <w:r>
        <w:t>Paragraph 2</w:t>
      </w:r>
    </w:p>
    <w:sectPr>
      <w:pgSz w:w="12240" w:h="15840"/>
      <w:pgMar w:top="1440" w:right="1800" w:bottom="1440" w:left="1800"
               w:header="720" w:footer="720" w:gutter="0"/>
      <w:cols w:space="720"/>
      <w:docGrid w:linePitch="360"/>
    </w:sectPr>
  </w:body>


Odd-page section inserted before paragraph mark in Paragraph 1::

  <w:body>
    <w:p>
      <w:pPr>
        <w:sectPr>
          <w:pgSz w:w="12240" w:h="15840"/>
          <w:pgMar w:top="1440" w:right="1800" w:bottom="1440" w:left="1800"
                   w:header="720" w:footer="720" w:gutter="0"/>
          <w:cols w:space="720"/>
          <w:docGrid w:linePitch="360"/>
        </w:sectPr>
      </w:pPr>
      <w:r>
        <w:t>Paragraph 1</w:t>
      </w:r>
    </w:p>
    <w:p/>
    <w:p>
      <w:r>
        <w:t>Paragraph 2</w:t>
      </w:r>
    </w:p>
    <w:sectPr w:rsidR="00F039D0" w:rsidSect="006006E7">
      <w:type w:val="oddPage"/>
      <w:pgSz w:w="12240" w:h="15840"/>
      <w:pgMar w:top="1440" w:right="1800" w:bottom="1440" w:left="1800"
               w:header="720" w:footer="720" w:gutter="0"/>
      <w:cols w:space="720"/>
      <w:docGrid w:linePitch="360"/>
    </w:sectPr>
  </w:body>

UI shows empty ¶ mark in first position of new next page. Section break
indicator appears directly after Paragraph 1 text, with no intervening
¶ mark.


Even-page section break inserted before first character in Paragraph 2::

  <w:body>
    <w:p>
      <w:r>
        <w:t>Paragraph 1</w:t>
      </w:r>
    </w:p>
    <w:p>
      <w:pPr>
        <w:sectPr>
          <w:type w:val="oddPage"/>
          <w:pgSz w:w="12240" w:h="15840"/>
          <w:pgMar w:top="1440" w:right="1800" w:bottom="1440" w:left="1800"
                   w:header="720" w:footer="720" w:gutter="0"/>
          <w:cols w:space="720"/>
          <w:docGrid w:linePitch="360"/>
        </w:sectPr>
      </w:pPr>
    </w:p>
    <w:p>
      <w:r>
        <w:lastRenderedPageBreak/>
        <w:t>Paragraph 2</w:t>
      </w:r>
    </w:p>
    <w:sectPr>
      <w:type w:val="evenPage"/>
      <w:pgSz w:w="12240" w:h="15840"/>
      <w:pgMar w:top="1440" w:right="1800" w:bottom="1440" w:left="1800"
               w:header="720" w:footer="720" w:gutter="0"/>
      <w:cols w:space="720"/>
      <w:docGrid w:linePitch="360"/>
    </w:sectPr>
  </w:body>


Enumerations
------------

WD_SECTION_START
~~~~~~~~~~~~~~~~

alias: **WD_SECTION**

`WdSectionStart Enumeration on MSDN`_

.. _WdSectionStart Enumeration on MSDN:
   http://msdn.microsoft.com/en-us/library/office/bb238171.aspx

CONTINUOUS (0)
    Continuous section break.

NEW_COLUMN (1)
    New column section break.

NEW_PAGE (2)
    New page section break.

EVEN_PAGE (3)
    Even pages section break.

ODD_PAGE (4)
    Odd pages section break.


WD_ORIENTATION
~~~~~~~~~~~~~~

alias: **WD_ORIENT**

`WdOrientation Enumeration on MSDN`_

.. _WdOrientation Enumeration on MSDN:
   http://msdn.microsoft.com/en-us/library/office/ff837902.aspx

LANDSCAPE (1)
    Landscape orientation.

PORTRAIT (0)
    Portrait orientation.


Schema excerpt
--------------

.. highlight:: xml

::

  <xsd:complexType name="CT_PPr">  <!-- denormalized -->
    <xsd:sequence>
      <!-- 34 others ... -->
      <xsd:element name="sectPr"    type="CT_SectPr"    minOccurs="0"/>
      <xsd:element name="pPrChange" type="CT_PPrChange" minOccurs="0"/>
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
