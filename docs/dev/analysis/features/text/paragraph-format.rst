
Paragraph formatting
====================

WordprocessingML supports a variety of paragraph formatting attributes to
control layout characteristics such as justification, indentation, line
spacing, space before and after, and widow/orphan control.


Alignment (justification)
-------------------------

In Word, each paragraph has an *alignment* attribute that specifies how to
justify the lines of the paragraph when the paragraph is laid out on the
page. Common values are left, right, centered, and justified.

Protocol
~~~~~~~~

Getting and setting paragraph alignment::

    >>> paragraph = body.add_paragraph()
    >>> paragraph.alignment
    None
    >>> paragraph.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    >>> paragraph.alignment
    RIGHT (2)
    >>> paragraph.alignment = None
    >>> paragraph.alignment
    None

XML Semantics
~~~~~~~~~~~~~

If the ``<w:jc>`` element is not present on a paragraph, the alignment value
for that paragraph is inherited from its style hierarchy. If the element is
present, its value overrides any inherited value. From the API, a value of
|None| on the ``Paragraph.alignment`` property corresponds to no ``<w:jc>``
element being present. If |None| is assigned to ``Paragraph.alignment``, the
``<w:jc>`` element is removed.


Paragraph spacing
-----------------

Spacing between subsequent paragraphs is controlled by the paragraph spacing
attributes. Spacing can be applied either before the paragraph, after it, or
both. The concept is similar to that of *padding* or *margin* in CSS.
WordprocessingML supports paragraph spacing specified as either a length
value or as a multiple of the line height; however only a length value is
supported via the Word UI. Inter-paragraph spacing "overlaps", such that the
rendered spacing between two paragraphs is the maximum of the space after the
first paragraph and the space before the second.

Protocol
~~~~~~~~

Getting and setting paragraph spacing::

    >>> paragraph_format = document.styles['Normal'].paragraph_format
    >>> paragraph_format.space_before
    None
    >>> paragraph_format.space_before = Pt(12)
    >>> paragraph_format.space_before.pt
    12.0

XML Semantics
~~~~~~~~~~~~~

* Paragraph spacing is specified using the `w:pPr/w:spacing` element, which
  also controls line spacing. Spacing is specified in twips.
* If the `w:spacing` element is not present, paragraph spacing is inherited
  from the style hierarchy.
* If not present in the style hierarchy, the paragraph will have no spacing.
* If the `w:spacing` element is present but the specific attribute (e.g.
  `w:before`) is not, its value is inherited.

Specimen XML
~~~~~~~~~~~~

.. highlight:: xml

12 pt space before, 0 after::

  <w:pPr>
    <w:spacing w:before="240" w:after="0"/>
  </w:pPr>


Line spacing
------------

Line spacing can be specified either as a specific length or as a multiple of
the line height (font size). Line spacing is specified by the combination of
values in `w:spacing/@w:line` and `w:spacing/@w:lineRule`. The
:attr:`.ParagraphFormat.line_spacing` property determines which method to use
based on whether the assigned value is an instance of |Length|.

Protocol
~~~~~~~~

.. highlight:: python

Getting and setting line spacing::

    >>> paragraph_format.line_spacing, paragraph_format.line_spacing_rule
    (None, None)

    >>> paragraph_format.line_spacing = Pt(18)
    >>> paragraph_format.line_spacing, paragraph_format.line_spacing_rule
    (228600, WD_LINE_SPACING.EXACTLY (4))

    >>> paragraph_format.line_spacing = 1
    >>> paragraph_format.line_spacing, paragraph_format.line_spacing_rule
    (152400, WD_LINE_SPACING.SINGLE (0))

    >>> paragraph_format.line_spacing = 0.9
    >>> paragraph_format.line_spacing, paragraph_format.line_spacing_rule
    (137160, WD_LINE_SPACING.MULTIPLE (5))

XML Semantics
~~~~~~~~~~~~~

* Line spacing is specified by the combination of the values in
  `w:spacing/@w:line` and `w:spacing/@w:lineRule`.
* `w:spacing/@w:line` is specified in twips. If `@w:lineRule` is 'auto' (or
  missing), `@w:line` is interpreted as 240ths of a line. For all other
  values of `@w:lineRule`, the value of `@w:line` is interpreted as
  a specific length in twips.
* If the `w:spacing` element is not present, line spacing is inherited.
* If `@w:line` is not present, line spacing is inherited.
* If not present, `@w:lineRule` defaults to 'auto'.
* If not present in the style hierarchy, line spacing defaults to single
  spaced.
* The 'atLeast' value for `@w:lineRule` indicates the line spacing will be
  `@w:line` twips or single spaced, whichever is greater.

Specimen XML
~~~~~~~~~~~~

.. highlight:: xml

14 points::

  <w:pPr>
    <w:spacing w:line="280"/>
  </w:pPr>

double-spaced::

  <w:pPr>
    <w:spacing w:line="480" w:lineRule="exact"/>
  </w:pPr>


Indentation
-----------

Paragraph indentation is specified using the `w:pPr/w:ind` element. Left,
right, first line, and hanging indent can be specified. Indentation can be
specified as a length or in hundredths of a character width. Only length is
supported by |docx|. Both first line indent and hanging indent are specified
using the :attr:`.ParagraphFormat.first_line_indent` property. Assigning
a positive value produces an indented first line. A negative value produces
a hanging indent.

Protocol
~~~~~~~~

.. highlight:: python

Getting and setting indentation::

    >>> paragraph_format.left_indent
    None
    >>> paragraph_format.right_indent
    None
    >>> paragraph_format.first_line_indent
    None

    >>> paragraph_format.left_indent = Pt(36)
    >>> paragraph_format.left_indent.pt
    36.0

    >>> paragraph_format.right_indent = Inches(0.25)
    >>> paragraph_format.right_indent.pt
    18.0

    >>> paragraph_format.first_line_indent = Pt(-18)
    >>> paragraph_format.first_line_indent.pt
    -18.0

XML Semantics
~~~~~~~~~~~~~

* Indentation is specified by `w:ind/@w:start`, `w:ind/@w:end`,
  `w:ind/@w:firstLine`, and `w:ind/@w:hanging`.

* `w:firstLine` and `w:hanging` are mutually exclusive, if both are
  specified, `w:firstLine` is ignored.

* All four attributes are specified in twips.

* `w:start` controls left indent for a left-to-right paragraph or right
  indent for a right-to-left paragraph. `w:end` controls the other side. If
  mirrorIndents is specified, `w:start` controls the inside margin and
  `w:end` the outside. Negative values are permitted and cause the text to
  move past the text margin.

* If `w:ind` is not present, indentation is inherited.

* Any omitted attributes are inherited.

* If not present in the style hierarchy, indentation values default to zero.

Specimen XML
~~~~~~~~~~~~

.. highlight:: xml

1 inch left, 0.5 inch (additional) first line, 0.5 inch right::

  <w:pPr>
    <w:ind w:start="1440" w:end="720" w:firstLine="720"/>
  </w:pPr>

0.5 inch left, 0.5 inch hanging indent::

  <w:pPr>
    <w:ind w:start="720" w:hanging="720"/>
  </w:pPr>


Page placement
--------------

There are a handful of page placement properties that control such things as
keeping the lines of a paragraph together on the same page, keeing
a paragraph (such as a heading) on the same page as the subsequent paragraph,
and placing the paragraph at the top of a new page. Each of these are
tri-state boolean properties where |None| indicates "inherit".

Protocol
~~~~~~~~

.. highlight:: python

Getting and setting indentation::

    >>> paragraph_format.keep_with_next
    None
    >>> paragraph_format.keep_together
    None
    >>> paragraph_format.page_break_before
    None
    >>> paragraph_format.widow_control
    None

    >>> paragraph_format.keep_with_next = True
    >>> paragraph_format.keep_with_next
    True

    >>> paragraph_format.keep_together = False
    >>> paragraph_format.keep_together
    False

    >>> paragraph_format.page_break_before = True
    >>> paragraph_format.widow_control = None


XML Semantics
~~~~~~~~~~~~~

* All four elements have "On/Off" semantics.

* If not present, their value is inherited.

* If not present in the style hierarchy, values default to False.

Specimen XML
~~~~~~~~~~~~

.. highlight:: xml

keep with next, keep together, no page break before, and widow/orphan
control::

  <w:pPr>
    <w:keepNext/>
    <w:keepLines/>
    <w:pageBreakBefore w:val="0"/>
    <w:widowControl/>
  </w:pPr>


Enumerations
------------

* :ref:`WdLineSpacing`
* :ref:`WdParagraphAlignment`


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

  <xsd:complexType name="CT_FramePr">
    <xsd:attribute name="dropCap"    type="ST_DropCap"/>
    <xsd:attribute name="lines"      type="ST_DecimalNumber"/>
    <xsd:attribute name="w"          type="s:ST_TwipsMeasure"/>
    <xsd:attribute name="h"          type="s:ST_TwipsMeasure"/>
    <xsd:attribute name="vSpace"     type="s:ST_TwipsMeasure"/>
    <xsd:attribute name="hSpace"     type="s:ST_TwipsMeasure"/>
    <xsd:attribute name="wrap"       type="ST_Wrap"/>
    <xsd:attribute name="hAnchor"    type="ST_HAnchor"/>
    <xsd:attribute name="vAnchor"    type="ST_VAnchor"/>
    <xsd:attribute name="x"          type="ST_SignedTwipsMeasure"/>
    <xsd:attribute name="xAlign"     type="s:ST_XAlign"/>
    <xsd:attribute name="y"          type="ST_SignedTwipsMeasure"/>
    <xsd:attribute name="yAlign"     type="s:ST_YAlign"/>
    <xsd:attribute name="hRule"      type="ST_HeightRule"/>
    <xsd:attribute name="anchorLock" type="s:ST_OnOff"/>
  </xsd:complexType>

  <xsd:complexType name="CT_Ind">
    <xsd:attribute name="start"          type="ST_SignedTwipsMeasure"/>
    <xsd:attribute name="startChars"     type="ST_DecimalNumber"/>
    <xsd:attribute name="end"            type="ST_SignedTwipsMeasure"/>
    <xsd:attribute name="endChars"       type="ST_DecimalNumber"/>
    <xsd:attribute name="left"           type="ST_SignedTwipsMeasure"/>
    <xsd:attribute name="leftChars"      type="ST_DecimalNumber"/>
    <xsd:attribute name="right"          type="ST_SignedTwipsMeasure"/>
    <xsd:attribute name="rightChars"     type="ST_DecimalNumber"/>
    <xsd:attribute name="hanging"        type="s:ST_TwipsMeasure"/>
    <xsd:attribute name="hangingChars"   type="ST_DecimalNumber"/>
    <xsd:attribute name="firstLine"      type="s:ST_TwipsMeasure"/>
    <xsd:attribute name="firstLineChars" type="ST_DecimalNumber"/>
  </xsd:complexType>

  <xsd:complexType name="CT_Jc">
    <xsd:attribute name="val" type="ST_Jc" use="required"/>
  </xsd:complexType>

  <xsd:complexType name="CT_OnOff">
    <xsd:attribute name="val" type="s:ST_OnOff"/>
  </xsd:complexType>

  <xsd:complexType name="CT_Spacing">
    <xsd:attribute name="before"            type="s:ST_TwipsMeasure"/>
    <xsd:attribute name="beforeLines"       type="ST_DecimalNumber"/>
    <xsd:attribute name="beforeAutospacing" type="s:ST_OnOff"/>
    <xsd:attribute name="after"             type="s:ST_TwipsMeasure"/>
    <xsd:attribute name="afterLines"        type="ST_DecimalNumber"/>
    <xsd:attribute name="afterAutospacing"  type="s:ST_OnOff"/>
    <xsd:attribute name="line"              type="ST_SignedTwipsMeasure"/>
    <xsd:attribute name="lineRule"          type="ST_LineSpacingRule"/>
  </xsd:complexType>

  <xsd:complexType name="CT_String">
    <xsd:attribute name="val" type="s:ST_String" use="required"/>
  </xsd:complexType>

  <xsd:complexType name="CT_Tabs">
    <xsd:sequence>
      <xsd:element name="tab" type="CT_TabStop" maxOccurs="unbounded"/>
    </xsd:sequence>
  </xsd:complexType>

  <!-- simple types -->

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

  <xsd:simpleType name="ST_LineSpacingRule">
    <xsd:restriction base="xsd:string">
      <xsd:enumeration value="auto"/>  <!-- default -->
      <xsd:enumeration value="exact"/>
      <xsd:enumeration value="atLeast"/>
    </xsd:restriction>
  </xsd:simpleType>

  <xsd:simpleType name="ST_OnOff">
    <xsd:union memberTypes="xsd:boolean ST_OnOff1"/>
  </xsd:simpleType>

  <xsd:simpleType name="ST_OnOff1">
    <xsd:restriction base="xsd:string">
      <xsd:enumeration value="on"/>
      <xsd:enumeration value="off"/>
    </xsd:restriction>
  </xsd:simpleType>
