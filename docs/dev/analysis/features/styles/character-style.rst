
Character Style
===============

Word allows a set of run-level properties to be given a name. The set of
properties is called a *character style*. All the settings may be applied to
a run in a single action by setting the style of the run.


Protocol
--------

There are two call protocols related to character style: getting and setting
the character style of a run, and specifying a style when creating a run.

Get run style::

    >>> run = p.add_run()

    >>> run.style
    <docx.styles.style._CharacterStyle object at 0x1053ab5d0>
    >>> run.style.name
    'Default Paragraph Font'

Set run style using character style name::

    >>> run.style = 'Emphasis'
    >>> run.style.name
    'Emphasis'

Set run style using character style object::

    >>> run.style = document.styles['Strong']
    >>> run.style.name
    'Strong'

Assigning |None| to :attr:`.Run.style` causes any applied character style to
be removed. A run without a character style inherits the default character
style of the document::

    >>> run.style = None
    >>> run.style.name
    'Default Paragraph Font'

Specifying the style of a run on creation::

    >>> run = p.add_run(style='Strong')
    >>> run.style.name
    'Strong'


Specimen XML
------------

.. highlight:: xml

A baseline regular run::

  <w:p>
    <w:r>
      <w:t>This is a regular paragraph.</w:t>
    </w:r>
  </w:p>

Adding `Emphasis` character style::

  <w:p>
    <w:r>
      <w:rPr>
        <w:rStyle w:val="Emphasis"/>
      </w:rPr>
      <w:t>This paragraph appears in Emphasis character style.</w:t>
    </w:r>
  </w:p>

A style that appears in the Word user interface (UI) with one or more spaces
in its name, such as "Subtle Emphasis", will generally have a style ID with
those spaces removed. In this example, "Subtle Emphasis" becomes
"SubtleEmphasis"::

  <w:p>
    <w:r>
      <w:rPr>
        <w:rStyle w:val="SubtleEmphasis"/>
      </w:rPr>
      <w:t>a few words in Subtle Emphasis style</w:t>
    </w:r>
  </w:p>


Schema excerpt
--------------

.. highlight:: xml

::

  <xsd:complexType name="CT_R">  <!-- flattened for readibility -->
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

  <xsd:complexType name="CT_String">
    <xsd:attribute name="val" type="s:ST_String" use="required"/>
  </xsd:complexType>

  <xsd:simpleType name="ST_String">
    <xsd:restriction base="xsd:string"/>
  </xsd:simpleType>
