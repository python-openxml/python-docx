
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

It's probably not going to make a lot of sense to implement this before having
the ability to set at least a core subset of the section properties. First ones
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

The following interactive session demonstrates the protocol for working with
sections::

    >>> sections = document.sections
    >>> len(sections)
    3
    >>> first_section = sections[0]
    >>> last_section = sections[-1]

    >>> p = body.add_paragraph()
    >>> p.section_properties
    None
    >>> p.add_section_break()


Word behavior
-------------

When inserting a section break in Word, there is no dialog box presented and no
parameters are supplied. Word simply copies the section details from the
current section (the next ``<w:sectPr>`` element in the document) to provide
the starting point. Experimentation would be required to determine exactly what
items are copied, but it at least includes the page size, margins, and column
spacing.


Specimen XML
------------

.. highlight:: xml

Inserting a section break (next page) produces this XML::

    <w:p>
      <w:pPr>
        <w:sectPr>
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
      <xsd:group   ref="EG_HdrFtrReferences" minOccurs="0" maxOccurs="6"/>
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
    <xsd:attributeGroup ref="AG_SectPrAttributes"/>
  </xsd:complexType>

  <xsd:group name="EG_HdrFtrReferences">
    <xsd:choice>
      <xsd:element name="headerReference" type="CT_HdrFtrRef" minOccurs="0"/>
      <xsd:element name="footerReference" type="CT_HdrFtrRef" minOccurs="0"/>
    </xsd:choice>
  </xsd:group>

  <xsd:attributeGroup name="AG_SectPrAttributes">
    <xsd:attribute name="rsidRPr"  type="ST_LongHexNumber"/>
    <xsd:attribute name="rsidDel"  type="ST_LongHexNumber"/>
    <xsd:attribute name="rsidR"    type="ST_LongHexNumber"/>
    <xsd:attribute name="rsidSect" type="ST_LongHexNumber"/>
  </xsd:attributeGroup>
