
Tab Stops
=========

WordprocessingML allows for custom specification of tab stops at the
paragraph level.  Tab stop spacing is a subset of paragraph formatting in
this system, so will be implemented within the
docx.text.parfmt.ParagraphFormatting object.  Tab stops will be handled as
a List-like TabStops object made up of TabStop objects.

A TabStop object has three properties, alignment, leader, and position.
Alignment is a WD_TAB_ALIGNMENT member and position is a Length() object.

Tab stops are always sorted in position order.  Alignment defaults to
WD_TAB_ALIGNMENT.LEFT, and leader defaults to WD_TAB_LEADER.SPACES.

Tab stops specify how tab characters in a paragraph are rendered. Insertion
of tab characters is accomplished using the Run object.


Protocol
--------

.. highlight:: python

Getting and setting tab stops::

    >>> tab_stops = paragraph.paragraph_format.tab_stops
    >>> tab_stops
    <docx.text.parfmt.TabStops object at 0x104ea8c30>

    >>> tab_stop = tab_stops.add_tab_stop(Inches(2), WD_TAB_ALIGNMENT.LEFT, WD_TAB_LEADER.DOTS)

    # add_tab_stop defaults to WD_TAB_ALIGNMENT.LEFT, WD_TAB_LEADER.SPACES

    >>> tab_stop = tab_stops.add_tab_stop(Inches(0.5))
    >>> tab_stop.alignment
    WD_TAB_ALIGNMENT.LEFT
    >>> tab_stop.leader
    WD_TAB_LEADER.SPACES

    # TabStop properties are read/write

    >>> tab_stop.position = Inches(2.5)
    >>> tab_stop.alignment = WD_TAB_ALIGNMENT.CENTER
    >>> tab_stop.leader = WD_TAB_LEADER.DASHES

    # Tab stops are sorted into position order as created or modified

    >>> [(t.position, t.alignment) for t in tab_stops]
    [(914400, WD_TAB_ALIGNMENT.LEFT), (2286000, WD_TAB_ALIGNMENT.CENTER)]

    # A tab stop is deleted using del statement

    >>> len(tab_stops)
    2
    >>> del tab_stops[1]
    >>> len(tab_stops)
    1

    # Restore default tabs

    >>> tab_stops.clear()


Word Behavior
-------------

When the w:tabs element is empty or not present, Word uses default tab stops
(typically every half inch).

Word resumes using default tab stops following the last specified tab stop.

TabStops must be in position order within the XML.  If they are not, the out-
of-order tab stop will appear in the ruler and in the properties dialog, but
will not actually be used by Word.


XML Semantics
-------------

* Both "num" and "list" alignment are a legacy from early versions of Word
  before hanging indents were available. Both are deprecated.

* "start" alignment is equivalent to "left", and "end" alignment are equivalent
  to "right". (Confirmed with manually edited XML.)

* A "clear" tab stop is not shown in Word's tab bar and default tab behavior
  is followed in the document.  That is, Word ignores that tab stop
  specification completely, acting as if it were not there at all.  This
  allows a tab stop inherited from a style, for example, to be ignored.

* The w:pos attribute uses twips rather than EMU.

* The w:tabs element must be removed when empty. If present, it must contain
  at least one w:tab element.


Specimen XML
------------

.. highlight:: xml

::

  <w:pPr>
    <w:tabs>
      <w:tab w:val="left" w:leader="dot" w:pos="2880"/>
      <w:tab w:val="decimal" w:pos="6480"/>
    </w:tabs>
  </w:pPr>


Enumerations
------------

* `WdTabAlignment Enumeration on MSDN`_

.. _WdTabAlignment Enumeration on MSDN:
   https://msdn.microsoft.com/EN-US/library/office/ff195609.aspx

=================   ========  =====
Name                XML       Value
=================   ========  =====
wdAlignTabBar       bar         4
wdAlignTabCenter    center      1
wdAlignTabDecimal   decimal     3
wdAlignTabLeft      left        0
wdAlignTabList      list        6
wdAlignTabRight     right       2
=================   ========  =====

Additional Enumeration values not appearing in WdTabAlignment

===============   ========  =====
Name              XML       Value
===============   ========  =====
wdAlignTabClear   clear      101
wdAlignTabEnd     end        102
wdAlignTabNum     num        103
wdAlignTabStart   start      104
===============   ========  =====


* `WdTabLeader Enumeration on MSDN`_

.. _WdTabLeader Enumeration on MSDN:
   https://msdn.microsoft.com/en-us/library/office/ff845050.aspx

====================   ==========  =====
Name                   XML         Value
====================   ==========  =====
wdTabLeaderDashes      hyphen        2
wdTabLeaderDots        dot           1
wdTabLeaderHeavy       heavy         4
wdTabLeaderLines       underscore    3
wdTabLeaderMiddleDot   middleDot     5
wdTabLeaderSpaces      none          0
====================   ==========  =====


MS API Protocol
---------------

The MS API defines a `TabStops object`_ which is a collection of
`TabStop objects`_.

.. _TabStops object:
  https://msdn.microsoft.com/EN-US/library/office/ff192806.aspx

.. _TabStop objects:
   https://msdn.microsoft.com/EN-US/library/office/ff195736.aspx


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
    <xsd:attribute name="val"    type="ST_TabJc"              use="required"/>
    <xsd:attribute name="leader" type="ST_TabTlc"             use="optional"/>
    <xsd:attribute name="pos"    type="ST_SignedTwipsMeasure" use="required"/>
  </xsd:complexType>

  <xsd:simpleType name="ST_TabJc">
    <xsd:restriction base="xsd:string">
      <xsd:enumeration value="clear"/>
      <xsd:enumeration value="start"/>
      <xsd:enumeration value="center"/>
      <xsd:enumeration value="end"/>
      <xsd:enumeration value="decimal"/>
      <xsd:enumeration value="bar"/>
      <xsd:enumeration value="num"/>
      <xsd:enumeration value="left"/>
      <xsd:enumeration value="right"/>
    </xsd:restriction>
  </xsd:simpleType>

  <xsd:simpleType name="ST_TabTlc">
    <xsd:restriction base="xsd:string">
      <xsd:enumeration value="none"/>
      <xsd:enumeration value="dot"/>
      <xsd:enumeration value="hyphen"/>
      <xsd:enumeration value="underscore"/>
      <xsd:enumeration value="heavy"/>
      <xsd:enumeration value="middleDot"/>
    </xsd:restriction>
  </xsd:simpleType>
