
Run-properties
==============

Character formatting such as font typeface, size, bold, and italic are applied
at the run level.


Candidate protocol
------------------

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


Acceptance tests
----------------

::

  Feature: Apply bold or italic to run
    In order to apply emphasis to a particular word or phrase in a paragraph
    As a python-docx developer
    I need a way to query and set bold and italic on a run

  Scenario: Apply bold to a run
    Given a run
     When I assign True to its bold property
     Then the run appears in bold typeface

  Scenario: Remove bold from a run
    Given a run having bold set on
     When I assign None to its bold property
     Then the run appears with its inherited bold setting

  Scenario: Set bold off unconditionally
    Given a run
     When I assign False to its bold property
     Then the run appears without bold regardless of its style hierarchy


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
      <xsd:group   ref="EG_RunInnerContent"   minOccurs="0" maxOccurs="unbounded"/>
    </xsd:sequence>
    <xsd:attribute name="rsidRPr" type="ST_LongHexNumber"/>
    <xsd:attribute name="rsidDel" type="ST_LongHexNumber"/>
    <xsd:attribute name="rsidR"   type="ST_LongHexNumber"/>
  </xsd:complexType>

  <xsd:complexType name="CT_RPr">
    <xsd:sequence>
      <xsd:group ref="EG_RPrContent" minOccurs="0"/>
    </xsd:sequence>
  </xsd:complexType>

  <xsd:group name="EG_RPrContent">
    <xsd:sequence>
      <xsd:group   ref="EG_RPrBase" minOccurs="0" maxOccurs="unbounded"/>
      <xsd:element name="rPrChange" type="CT_RPrChange" minOccurs="0"/>
    </xsd:sequence>
  </xsd:group>

  <xsd:group name="EG_RPrBase">
    <xsd:choice>
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


Resources
---------

* `WdBreakType Enumeration on MSDN`_
* `Range.InsertBreak Method (Word) on MSDN`_

.. _WdBreakType Enumeration on MSDN:
   http://msdn.microsoft.com/en-us/library/office/ff195905.aspx

.. _Range.InsertBreak Method (Word) on MSDN:
   http://msdn.microsoft.com/en-us/library/office/ff835132.aspx
