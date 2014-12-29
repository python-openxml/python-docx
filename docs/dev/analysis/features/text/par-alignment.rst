
Paragraph alignment
===================

In Word, each paragraph has an *alignment* attribute that specifies how to
justify the lines of the paragraph when the paragraph is laid out on the
page. Common values are left, right, centered, and justified.


Protocol
--------

The protocol for getting and setting paragraph alignment is illustrated in
this interactive session::

    >>> paragraph = body.add_paragraph()
    >>> paragraph.alignment
    None
    >>> paragraph.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    >>> paragraph.alignment
    RIGHT (2)
    >>> paragraph.alignment = None
    >>> paragraph.alignment
    None


Semantics
---------

If the ``<w:jc>`` element is not present on a paragraph, the alignment value
for that paragraph is inherited from its style hierarchy. If the element is
present, its value overrides any inherited value. From the API, a value of
|None| on the ``Paragraph.alignment`` property corresponds to no ``<w:jc>``
element being present. If |None| is assigned to ``Paragraph.alignment``, the
``<w:jc>`` element is removed.


Enumerations
------------

WD_ALIGN_PARAGRAPH
~~~~~~~~~~~~~~~~~~

`WdParagraphAlignment Enumeration on MSDN`_

+--------------+------+----------------+
| Name         | enum | attr           |
+==============+======+================+
| LEFT         |  0   | left           |
+--------------+------+----------------+
| CENTER       |  1   | center         |
+--------------+------+----------------+
| RIGHT        |  2   | right          |
+--------------+------+----------------+
| JUSTIFY      |  3   | both           |
+--------------+------+----------------+
| DISTRIBUTE   |  4   | distribute     |
+--------------+------+----------------+
| JUSTIFY_MED  |  5   | mediumKashida  |
+--------------+------+----------------+
| JUSTIFY_HI   |  7   | highKashida    |
+--------------+------+----------------+
| JUSTIFY_LOW  |  8   | lowKashida     |
+--------------+------+----------------+
| THAI_JUSTIFY |  9   | thaiDistribute |
+--------------+------+----------------+

.. _WdParagraphAlignment Enumeration on MSDN:
   http://msdn.microsoft.com/en-us/library/office/ff835817(v=office.15).aspx


Specimen XML
------------

.. highlight:: xml

A paragraph with inherited alignment::

  <w:p>
    <w:r>
      <w:t>Inherited paragraph alignment.</w:t>
    </w:r>
  </w:p>

A right-aligned paragraph::

  <w:p>
    <w:pPr>
      <w:jc w:val="right"/>
    </w:pPr>
    <w:r>
      <w:t>Right-aligned paragraph.</w:t>
    </w:r>
  </w:p>


Schema excerpt
--------------

::

  <xsd:complexType name="CT_P">
    <xsd:sequence>
      <xsd:element name="pPr"         type="CT_PPr" minOccurs="0"/>
      <xsd:group    ref="EG_PContent"               minOccurs="0" maxOccurs="unbounded"/>
    </xsd:sequence>
      <xsd:attribute name="rsidRPr"      type="ST_LongHexNumber"/>
      <xsd:attribute name="rsidR"        type="ST_LongHexNumber"/>
      <xsd:attribute name="rsidDel"      type="ST_LongHexNumber"/>
      <xsd:attribute name="rsidP"        type="ST_LongHexNumber"/>
      <xsd:attribute name="rsidRDefault" type="ST_LongHexNumber"/>
  </xsd:complexType>

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

  <xsd:complexType name="CT_Jc">
    <xsd:attribute name="val" type="ST_Jc" use="required"/>
  </xsd:complexType>

  <xsd:simpleType name="ST_Jc">
    <xsd:restriction base="xsd:string">
      <xsd:enumeration value="start"/>
      <xsd:enumeration value="center"/>
      <xsd:enumeration value="end"/>
      <xsd:enumeration value="both"/>
      <xsd:enumeration value="mediumKashida"/>
      <xsd:enumeration value="distribute"/>
      <xsd:enumeration value="numTab"/>
      <xsd:enumeration value="highKashida"/>
      <xsd:enumeration value="lowKashida"/>
      <xsd:enumeration value="thaiDistribute"/>
      <xsd:enumeration value="left"/>
      <xsd:enumeration value="right"/>
    </xsd:restriction>
  </xsd:simpleType>
