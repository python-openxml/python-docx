
Boolean Run properties
======================

Character formatting that is either on or off, such as bold, italic, and
small caps. Certain of these properties are *toggle properties* that may
cancel each other out if they appear more than once in the style hierarchy.
See §17.7.3 for more details on toggle properties. They don't affect the API
specified here.

The following run properties are boolean (tri-state) properties:

+-----------------+------------+-------------------------------------------+
| element         | spec       | name                                      |
+=================+============+===========================================+
| `<b/>`          | §17.3.2.1  | Bold                                      |
+-----------------+------------+-------------------------------------------+
| `<bCs/>`        | §17.3.2.2  | Complex Script Bold                       |
+-----------------+------------+-------------------------------------------+
| `<caps/>`       | §17.3.2.5  | Display All Characters as Capital Letters |
+-----------------+------------+-------------------------------------------+
| `<cs/>`         | §17.3.2.7  | Use Complex Script Formatting on Run      |
+-----------------+------------+-------------------------------------------+
| `<dstrike/>`    | §17.3.2.9  | Double Strikethrough                      |
+-----------------+------------+-------------------------------------------+
| `<emboss/>`     | §17.3.2.13 | Embossing                                 |
+-----------------+------------+-------------------------------------------+
| `<i/>`          | §17.3.2.16 | Italics                                   |
+-----------------+------------+-------------------------------------------+
| `<iCs/>`        | §17.3.2.17 | Complex Script Italics                    |
+-----------------+------------+-------------------------------------------+
| `<imprint/>`    | §17.3.2.18 | Imprinting                                |
+-----------------+------------+-------------------------------------------+
| `<noProof/>`    | §17.3.2.21 | Do Not Check Spelling or Grammar          |
+-----------------+------------+-------------------------------------------+
| `<oMath/>`      | §17.3.2.22 | Office Open XML Math                      |
+-----------------+------------+-------------------------------------------+
| `<outline/>`    | §17.3.2.23 | Display Character Outline                 |
+-----------------+------------+-------------------------------------------+
| `<rtl/>`        | §17.3.2.30 | Right To Left Text                        |
+-----------------+------------+-------------------------------------------+
| `<shadow/>`     | §17.3.2.31 | Shadow                                    |
+-----------------+------------+-------------------------------------------+
| `<smallCaps/>`  | §17.3.2.33 | Small Caps                                |
+-----------------+------------+-------------------------------------------+
| `<snapToGrid/>` | §17.3.2.34 | Use Document Grid Settings For Inter-     |
|                 |            | Character Spacing                         |
+-----------------+------------+-------------------------------------------+
| `<specVanish/>` | §17.3.2.36 | Paragraph Mark is Always Hidden           |
+-----------------+------------+-------------------------------------------+
| `<strike/>`     | §17.3.2.37 | Single Strikethrough                      |
+-----------------+------------+-------------------------------------------+
| `<vanish/>`     | §17.3.2.41 | Hidden Text                               |
+-----------------+------------+-------------------------------------------+
| `<webHidden/>`  | §17.3.2.44 | Web Hidden Text                           |
+-----------------+------------+-------------------------------------------+


Protocol
--------

At the API level, each of the boolean run properties is a read/write
'tri-state' property, having the possible values |True|, |False|, and |None|.

The following interactive session demonstrates the protocol for querying and
applying run-level properties::

    >>> run = p.add_run()
    >>> run.bold
    None
    >>> run.bold = True
    >>> run.bold
    True
    >>> run.bold = False
    >>> run.bold
    False
    >>> run.bold = None
    >>> run.bold
    None

The semantics of the three values are as follows:

+-------+---------------------------------------------------------------+
| value | meaning                                                       |
+=======+===============================================================+
| True  | The effective value of the property is unconditionally *on*.  |
|       | Contrary settings in the style hierarchy have no effect.      |
+-------+---------------------------------------------------------------+
| False | The effective value of the property is unconditionally *off*. |
|       | Contrary settings in the style hierarchy have no effect.      |
+-------+---------------------------------------------------------------+
| None  | The element is not present. The effective value is            |
|       | inherited from the style hierarchy. If no value for this      |
|       | property is present in the style hierarchy, the effective     |
|       | value is *off*.                                               |
+-------+---------------------------------------------------------------+


Specimen XML
------------

.. highlight:: xml

::

    <w:r w:rsidRPr="00FA3070">
      <w:rPr>
        <w:b/>
        <w:i/>
        <w:smallCaps/>
        <w:strike/>
        <w:sz w:val="28"/>
        <w:szCs w:val="28"/>
        <w:u w:val="single"/>
      </w:rPr>
      <w:t>bold, italic, small caps, strike, size, and underline, applied in
        reverse order but not to paragraph mark</w:t>
    </w:r>


Schema excerpt
--------------

.. highlight:: xml

It appears the run properties may appear in any order and may appear multiple
times each. Not sure what the semantics of that would be or why one would
want to do it, but something to note. Word seems to place them in the order
below when it writes the file.::

  <xsd:complexType name="CT_R">  <!-- denormalized -->
    <xsd:sequence>
      <xsd:element name="rPr" type="CT_RPr" minOccurs="0"/>
      <xsd:group   ref="EG_RunInnerContent" minOccurs="0" maxOccurs="unbounded"/>
    </xsd:sequence>
    <xsd:attribute name="rsidRPr" type="ST_LongHexNumber"/>
    <xsd:attribute name="rsidDel" type="ST_LongHexNumber"/>
    <xsd:attribute name="rsidR"   type="ST_LongHexNumber"/>
  </xsd:complexType>

  <xsd:complexType name="CT_RPr">  <!-- denormalized -->
    <xsd:sequence>
      <xsd:choice minOccurs="0" maxOccurs="unbounded"/>
        <xsd:element name="rStyle"          type="CT_String"/>
        <xsd:element name="rFonts"          type="CT_Fonts"/>
        <xsd:element name="b"               type="CT_OnOff"/>
        <xsd:element name="bCs"             type="CT_OnOff"/>
        <xsd:element name="i"               type="CT_OnOff"/>
        <xsd:element name="iCs"             type="CT_OnOff"/>
        <xsd:element name="caps"            type="CT_OnOff"/>
        <xsd:element name="smallCaps"       type="CT_OnOff"/>
        <xsd:element name="strike"          type="CT_OnOff"/>
        <xsd:element name="dstrike"         type="CT_OnOff"/>
        <xsd:element name="outline"         type="CT_OnOff"/>
        <xsd:element name="shadow"          type="CT_OnOff"/>
        <xsd:element name="emboss"          type="CT_OnOff"/>
        <xsd:element name="imprint"         type="CT_OnOff"/>
        <xsd:element name="noProof"         type="CT_OnOff"/>
        <xsd:element name="snapToGrid"      type="CT_OnOff"/>
        <xsd:element name="vanish"          type="CT_OnOff"/>
        <xsd:element name="webHidden"       type="CT_OnOff"/>
        <xsd:element name="color"           type="CT_Color"/>
        <xsd:element name="spacing"         type="CT_SignedTwipsMeasure"/>
        <xsd:element name="w"               type="CT_TextScale"/>
        <xsd:element name="kern"            type="CT_HpsMeasure"/>
        <xsd:element name="position"        type="CT_SignedHpsMeasure"/>
        <xsd:element name="sz"              type="CT_HpsMeasure"/>
        <xsd:element name="szCs"            type="CT_HpsMeasure"/>
        <xsd:element name="highlight"       type="CT_Highlight"/>
        <xsd:element name="u"               type="CT_Underline"/>
        <xsd:element name="effect"          type="CT_TextEffect"/>
        <xsd:element name="bdr"             type="CT_Border"/>
        <xsd:element name="shd"             type="CT_Shd"/>
        <xsd:element name="fitText"         type="CT_FitText"/>
        <xsd:element name="vertAlign"       type="CT_VerticalAlignRun"/>
        <xsd:element name="rtl"             type="CT_OnOff"/>
        <xsd:element name="cs"              type="CT_OnOff"/>
        <xsd:element name="em"              type="CT_Em"/>
        <xsd:element name="lang"            type="CT_Language"/>
        <xsd:element name="eastAsianLayout" type="CT_EastAsianLayout"/>
        <xsd:element name="specVanish"      type="CT_OnOff"/>
        <xsd:element name="oMath"           type="CT_OnOff"/>
      </xsd:choice>
      <xsd:element name="rPrChange" type="CT_RPrChange" minOccurs="0"/>
    </xsd:sequence>
  </xsd:group>

  <xsd:complexType name="CT_OnOff">
    <xsd:attribute name="val" type="s:ST_OnOff"/>
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


Toggle properties
-----------------

Certain of the boolean run properties are *toggle properties*. A toggle
property is one that behaves like a *toggle* at certain places in the style
hierarchy. Toggle here means that setting the property on has the effect of
reversing the prior setting rather than unconditionally setting the property
on.

This behavior allows these properties to be overridden (turned off) in
inheriting styles. For example, consider a character style `emphasized` that
sets bold on. Another style, `strong` inherits from `emphasized`, but should
display in italic rather than bold. Setting bold off has no effect because it
is overridden by the bold in `strong` (I think). Because bold is a toggle
property, setting bold on in `emphasized` causes its value to be toggled, to
False, achieving the desired effect. See §17.7.3 for more details on toggle
properties.

The following run properties are toggle properties:

+----------------+------------+-------------------------------------------+
| element        | spec       | name                                      |
+================+============+===========================================+
| `<b/>`         | §17.3.2.1  | Bold                                      |
+----------------+------------+-------------------------------------------+
| `<bCs/>`       | §17.3.2.2  | Complex Script Bold                       |
+----------------+------------+-------------------------------------------+
| `<caps/>`      | §17.3.2.5  | Display All Characters as Capital Letters |
+----------------+------------+-------------------------------------------+
| `<emboss/>`    | §17.3.2.13 | Embossing                                 |
+----------------+------------+-------------------------------------------+
| `<i/>`         | §17.3.2.16 | Italics                                   |
+----------------+------------+-------------------------------------------+
| `<iCs/>`       | §17.3.2.17 | Complex Script Italics                    |
+----------------+------------+-------------------------------------------+
| `<imprint/>`   | §17.3.2.18 | Imprinting                                |
+----------------+------------+-------------------------------------------+
| `<outline/>`   | §17.3.2.23 | Display Character Outline                 |
+----------------+------------+-------------------------------------------+
| `<shadow/>`    | §17.3.2.31 | Shadow                                    |
+----------------+------------+-------------------------------------------+
| `<smallCaps/>` | §17.3.2.33 | Small Caps                                |
+----------------+------------+-------------------------------------------+
| `<strike/>`    | §17.3.2.37 | Single Strikethrough                      |
+----------------+------------+-------------------------------------------+
| `<vanish/>`    | §17.3.2.41 | Hidden Text                               |
+----------------+------------+-------------------------------------------+


Resources
---------

* `WdBreakType Enumeration on MSDN`_
* `Range.InsertBreak Method (Word) on MSDN`_

.. _WdBreakType Enumeration on MSDN:
   http://msdn.microsoft.com/en-us/library/office/ff195905.aspx

.. _Range.InsertBreak Method (Word) on MSDN:
   http://msdn.microsoft.com/en-us/library/office/ff835132.aspx
