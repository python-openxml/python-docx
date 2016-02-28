
Font highlight color
====================

Text in a Word document can be "highlighted" with a number of colors,
providing text background color. The visual effect is similar to that
produced using a highlighter (often fluorescent yellow) on a printed page.


Protocol
--------

Text is highlighted by assigning a member of `WD_COLOR_INDEX` to
`Font.highlight_color`.

    >>> font = paragraph.add_run().font
    >>> font.highlight_color
    None
    >>> font.highlight_color = WD_COLOR_INDEX.YELLOW
    >>> font.highlight_color
    YELLOW (7)
    >>> font.highlight_color = WD_COLOR_INDEX.TURQUOISE
    >>> font.highlight_color
    TURQUOISE (3)
    >>> font.highlight_color = None
    >>> font.highlight_color
    None


Enumerations
------------

* `WdColorIndex Enumeration on MSDN`_

.. _WdColorIndex Enumeration on MSDN: https://msdn.microsoft.com/EN-US/library/office/ff195343.aspx


XML Semantics
-------------

Mapping of `WD_COLOR_INDEX` members to `ST_Highlight` values::

    AUTO = 'default'
    BLACK = 'black'
    BLUE = 'blue'
    BRIGHTGREEN = 'green'
    DARKBLUE = 'darkBlue'
    DARKRED = 'darkRed'
    DARKYELLOW = 'darkYellow'
    GRAY25 = 'lightGray'
    GRAY50 = 'darkGray'
    GREEN = 'darkGreen'
    PINK = 'magenta'
    RED = 'red'
    TEAL = 'darkCyan'
    TURQUOISE = 'cyan'
    VOILET = 'darkMagenta'
    WHITE = 'white'
    YELLOW = 'yellow'


Specimen XML
------------

.. highlight:: xml

Baseline run::

  <w:r>
    <w:t>Black text on white background</w:t>
  </w:r>

Blue text, Bright Green Highlight::

  <w:r>
    <w:rPr>
      <w:highlight w:val="green"/>
    </w:rPr>
    <w:t>Blue text on bright green background</w:t>
  </w:r>

Red text, Green Highlight::

  <w:r>
    <w:rPr>
      <w:highlight w:val="darkGreen"/>
    </w:rPr>
    <w:t>Red text on green background</w:t>
  </w:r>


Schema excerpt
--------------

.. highlight:: xml

According to the schema, run properties may appear in any order and may
appear multiple times each. Not sure what the semantics of that would be or
why one would want to do it, but something to note. Word seems to place them
in the order below when it writes the file.::

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

  <!-- complex types -->

  <xsd:complexType name="CT_Highlight">
    <xsd:attribute name="val" type="ST_Highlight" use="required"/>
  </xsd:complexType>

  <!-- simple types -->

  <xsd:simpleType name="ST_Highlight">
    <xsd:restriction base="xsd:string">
      <xsd:enumeration value="default"/>
      <xsd:enumeration value="black"/>
      <xsd:enumeration value="blue"/>
      <xsd:enumeration value="green"/>
      <xsd:enumeration value="darkBlue"/>
      <xsd:enumeration value="darkRed"/>
      <xsd:enumeration value="darkYellow"/>
      <xsd:enumeration value="lightGray"/>
      <xsd:enumeration value="darkGray"/>
      <xsd:enumeration value="darkGreen"/>
      <xsd:enumeration value="magenta"/>
      <xsd:enumeration value="red"/>
      <xsd:enumeration value="darkCyan"/>
      <xsd:enumeration value="cyan"/>
      <xsd:enumeration value="darkMagenta"/>
      <xsd:enumeration value="white"/>
      <xsd:enumeration value="yellow"/>
    </xsd:restriction>
  </xsd:simpleType>
