
Tab Stop Specification
====================

WordprocessingML allows for custom specification of tab stops at the paragraph level.  Tab stop spacing is a subset of paragraph formatting in this system, so will be implemented within the docx.text.parfmt.ParagraphFormatting object.  Tab stops will be handled as a python List of integer (twip) values.

Tab character insertion is already properly handled as part of Runs.  This feature deals with the horizontal spacing of tabs within the document only.


Protocol
~~~~~~~~

.. highlight:: python

Getting and setting tab stops::

    >>> paragraph_format.tabs
    None
    >>> paragraph_format.tabs = [1440, 2880, 4320, 5760, 7200, 8640, 10080, 11520]  # One inch tab stops
    >>> paragraph_format.tabs
    [1440, 2880, 4320, 5760, 7200, 8640, 10080, 11520]
    >>> paragraph_format.tabs = None  # default tabs
    >>> paragraph_format.tabs
    None
    >>> paragraph_format.tabs = []   # no tabs  (as distinct from default tabs)
    >>> paragraph_format.tabs
    []


XML Semantics
~~~~~~~~~~~~~

* Tab stops have a type (w:val), which allows the specification of left, center, right, decimal, bar, and list (implementation unknown) alignment.

* Tab stop positions (w:pos) are stored in XML in units of 1,440ths of an inch, units called "twips."

Specimen XML
~~~~~~~~~~~~

.. highlight:: xml

One inch tab stops using left alignment::

  <w:pPr> 
    <w:tabs>
      <w:tab w:val="left" w:pos="1440"/>
      <w:tab w:val="left" w:pos="2880"/>
      <w:tab w:val="left" w:pos="4320"/>
      <w:tab w:val="left" w:pos="5760"/>
      <w:tab w:val="left" w:pos="7200"/>
      <w:tab w:val="left" w:pos="8640"/>
      <w:tab w:val="left" w:pos="10080"/>
      <w:tab w:val="left" w:pos="11520"/>
    </w:tabs>
  </w:pPr>
  

Enumerations
------------

* `WdTabAlignment Enumeration on MSDN`_
 
.. _WdTabAlignment Enumeration on MSDN:
   https://msdn.microsoft.com/EN-US/library/office/ff195609.aspx



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

 
  <xsd:complexType name="CT_Tabs">
    <xsd:sequence>
      <xsd:element name="tab" type="CT_TabStop" maxOccurs="unbounded"/>
    </xsd:sequence>
  </xsd:complexType>
  
  <xsd:complexType name="CT_TabStop">
    <xsd:sequence>
      <xsd:element name="val" type="ST_TabType" use="required">
      <xsd:element name="pos" type="ST_Integer" use="required">
    </xsd:sequence>
  </xsd:complexType>

  <!-- simple types -->
  <xsd:simpleType name="ST_TabType">
    <xsd:restriction base="xsd:string">
      <xsd:enumeration value="bar">        <!-- wdAlignTabBar      4 -->
      <xsd:enumeration value="center">     <!-- wdAlignTabCenter   1 -->
      <xsd:enumeration value="decimal">    <!-- wdAlignTabDecimal  3 -->
      <xsd:enumeration value="left">       <!-- wdAlignTabLeft     0 -->
      <xsd:enumeration value="list">       <!-- wdAlignTabList     6 IMPLEMENTATION NOT CONFIRMED -->
      <xsd:enumeration value="right">      <!-- wdAlignTabRight    2 -->
    </xsd:restriction>
  </xsd:simpleType>
