
Highlight
=========

Text in a Word document can be "highlighted" with a number of colors, providing text background color.


Protocol
--------

The call protocol for highlight involves manipulating the font highlight (background color) by assigning a string value from a fixed, case-sensitive list.

    >>> run = paragraph.add_run()
    >>> font = run.font
    >>> font.highlight
    None
    >>> font.highlight = 'yellow'
    >>> font.highlight
    'yellow'
    >>> font.highlight = 'cyan'
    >>> font.highlight
    'cyan'
    >>> font.highlight = None
    >>> font.highlight
    None
    >>> font.highlight = 'noHighlight'
    >>> font.highlight
    None


Enumerations
------------

* `WdColorIndex Enumeration on MSDN`_

.. _WdColorIndex Enumeration on MSDN: https://msdn.microsoft.com/EN-US/library/office/ff195343.aspx

Text representation is rigid, but do not match the enumeration names.  From exhaustive selection in Word 2010, I have come up with the following list of usable values::

wdAuto = ???  ('default')
wdBlack = 'black'
wdBlue = 'blue' 
wdBrightGreen = 'green'
wdByAuthor = ?? 
wdDarkBlue = 'darkBlue'
wdDarkRed = 'darkRed'
wdDarkYellow = 'darkYellow'
wdGray25 = 'lightGray'
wdGray50 = 'darkGray'
wdGreen = 'darkGreen'    
wdNoHighlight = ??  ('noHighlight')
wdPink = 'magenta' 
wdRed = 'red'
wdTeal = 'darkCyan'
wdTurquoise = 'cyan'
wdViolet = 'darkMagenta'    
wdWhite = ??   ('white')
wdYellow = 'yellow' 
           
These values ARE case-sensitive.  Other variations cause an error when the resulting document is loaded in Word. 


Specimen XML
------------

.. highlight:: xml

Baseline run::

  <w:r>
    <w:t xml:space="preserve">Black text, White background </w:t>
  </w:r>

Blue text, Bright Green Highlight::

  <w:r>
    <w:rPr>
      <w:rFonts w:ascii="Courier New" w:hAnsi="Courier New" w:cs="Courier New"/>
      <w:color w:val="0000FF"/>
      <w:sz w:val="24"/>
      <w:szCs w:val="24"/>
      <w:highlight w:val="green"/>
    </w:rPr>
    <w:t xml:space="preserve">Blue text on Bright Green background </w:t>
  </w:r>

Red text, Green Highlight::

  <w:r>
    <w:rPr>
      <w:rFonts w:ascii="Courier New" w:hAnsi="Courier New" w:cs="Courier New"/>
      <w:color w:val="FF0000"/>
      <w:sz w:val="24"/>
      <w:szCs w:val="24"/>
      <w:highlight w:val="darkGreen"/>
    </w:rPr>
    <w:t xml:space="preserve">Blue text on Bright Green background </w:t>
  </w:r>
  
NOTE the difference between the color enumeration name and the text that must be used.

Schema excerpt
--------------

The base Schema presented is from the font Analysis Document.

.. highlight:: xml

It appears the run properties may appear in any order and may appear multiple
times each. Not sure what the semantics of that would be or why one would
want to do it, but something to note. Word seems to place them in the order
below when it writes the file.::

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
    <xsd:attribute name="val"        type="ST_Highlight"/>
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
      <xsd:enumeration value="noHighlight"/>
      <xsd:enumeration value="magenta"/>
      <xsd:enumeration value="red"/>
      <xsd:enumeration value="darkCyan"/>
      <xsd:enumeration value="cyan"/>
      <xsd:enumeration value="darkMagenta"/>
      <xsd:enumeration value="white"/>
      <xsd:enumeration value="yellow"/>
    </xsd:restriction>
  </xsd:simpleType>




