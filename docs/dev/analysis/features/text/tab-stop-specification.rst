
Tab Stop Specification
====================

WordprocessingML allows for custom specification of tab stops at the paragraph level.  Tab stop spacing is a subset of paragraph formatting in this system, so will be implemented within the docx.text.parfmt.ParagraphFormatting object.  Tab stops will be handled as a List-like TabStops object made up of TabStop objects.

A TabStop object has two properties, alignment and position.  Alignment is a WD_TAB_ALIGNMENT member and position is a Length() object.

Tab character insertion is already properly handled as part of Runs.  This feature deals with the horizontal spacing of tabs within the document only.


Protocol
~~~~~~~~

.. highlight:: python

Getting and setting tab stops::

    >>> paragraph_format.tab_stops
    None
    >>> tabStops.append(TabStop(WD_TAB_ALIGNMENT.LEFT, Inches(1)))      # 1 inch
    >>> tabStops.append(TabStop(WD_TAB_ALIGNMENT.LEFT, Twips(2880)))    # 2 inches
    >>> tabStops.append(TabStop(WD_TAB_ALIGNMENT.LEFT, Mm(76.2)))       # 3 inches
    >>> tabStops.append(TabStop(WD_TAB_ALIGNMENT.DECIMAL, Inches(4.5))) # 4.5 inches
    >>> tabStops.append(TabStop(WD_TAB_ALIGNMENT.RIGHT, Inches(7)))     # 7 inches
    >>> paragraph_format.tab_stops = tabStops
    >>> paragraph_format.tab_stops
    [(LEFT (0), 1440), (LEFT (0), 2880), (LEFT (0), 4320), (DECIMAL (3), 6480), (RIGHT (2), 10080)]
    >>> paragraph_format.tabs = None  # default tabs
    >>> paragraph_format.tabs
    None


XML Semantics
~~~~~~~~~~~~~

* Tab stops have a type (w:val), which allows the specification of left, center, right, decimal, bar, and list alignment.

* The details of the list alignment are elusive.  (I have not been able to create this type of tab stops in Word, even within lists.  Perhaps a later version of Word than I use is required.) 

* Tab stop positions (w:pos) are stored in XML in twips.

Specimen XML
~~~~~~~~~~~~

.. highlight:: xml

One inch tab stops using left alignment::

  <w:pPr> 
    <w:tabs>
      <w:tab w:val="left" w:pos="1440"/>
      <w:tab w:val="left" w:pos="2880"/>
      <w:tab w:val="left" w:pos="4320"/>
      <w:tab w:val="decimal" w:pos="6480"/>
      <w:tab w:val="right" w:pos="10080"/>
    </w:tabs>
  </w:pPr>
  

Enumerations
------------

* `WdTabAlignment Enumeration on MSDN`_
 
.. _WdTabAlignment Enumeration on MSDN:
   https://msdn.microsoft.com/EN-US/library/office/ff195609.aspx


MS API Protocol
~~~~~~~~~~~~~~~
The MS API defines a `TabStops object`_ which is made up of `TabStop objects`_.

.. _TabStops object:
  https://msdn.microsoft.com/EN-US/library/office/ff192806.aspx
  
.. _TabStop objects:
   https://msdn.microsoft.com/EN-US/library/office/ff195736.aspx

Leading character specification is possible within the MS API and within Word.  (I do not plan to implement leading character support at this time.)  
      
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
      <xsd:element name="pos" type="ST_SignedTwipsMeasure" use="required">
    </xsd:sequence>
  </xsd:complexType>

  <!-- simple types -->
  <xsd:simpleType name="ST_TabType">
    <xsd:restriction base="xsd:string">
      <xsd:enumeration value="bar">        <!-- wdAlignTabBar      4 -->
      <xsd:enumeration value="center">     <!-- wdAlignTabCenter   1 -->
      <xsd:enumeration value="decimal">    <!-- wdAlignTabDecimal  3 -->
      <xsd:enumeration value="left">       <!-- wdAlignTabLeft     0 -->
      <xsd:enumeration value="list">       <!-- wdAlignTabList     6 IMPLEMENTATION STRING NOT CONFIRMED -->
      <xsd:enumeration value="right">      <!-- wdAlignTabRight    2 -->
    </xsd:restriction>
  </xsd:simpleType>
