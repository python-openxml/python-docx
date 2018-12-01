
Numbering Part
==============

Here are some notes that can be used by developers as API functions
for creating bulleted or numbered lists
(including multi-level lists) are developed.

Overview
--------

The numbering part is documented in section 17.9 of ISO-29500-1.
The file **numbering.xml** contains the built-in and user-defined
list styles. Unlike paragraph, table, and character styles, list
styles need not have a string-based identifier.

At the root of **numbering.xml** is the element ``<w:numbering>``
whose children are of two main types: ``<w:abstractNum>`` and
``<w:num>``, of XML types ``CT_AbstractNum`` and ``CT_Num``,
respectively. Each is identified by a unique
attribute (``w:numId`` and ``w:abstractNumId``, respectively)
of type ``CT_DecimalNumber``.

A paragraph contained in **document.xml**
is recognized by the user agent as numbered
if its ``<w:pPr>`` element contains a ``<w:numPr>``
element which references the ``numId`` attribute
of the corresponding numbering style.

.. code-block:: xml

    <w:p>
      <w:pPr>
        <w:numPr>
          <w:ilvl w:val="0" />
          <w:numId w:val="2" />
        </w:numPr>
      </w:pPr>
      <w:r>
        <w:t>Level one</w:t>
      </w:r>
    </w:p>

The numbering style defined by a ``<w:num>`` element
is limited to :

-    A reference to an abstract numbering style; and
-    (optionally) level-specific overrides of the abstract style.

The standard explains the two-level scheme for defining numbering
styles as follows (terminology is introduced):[#first]_

*Abstract numbering definitions*
    define the appearance and behavior of a specific set of numbered paragraphs in
    a document. Because this construct is abstract, they are not be directly referenced by document content, but
    rather they shall be inherited by a 
*numbering definition instance,*
    which itself is referenced by document content.

A numbering definition, therefore, will usually be of simple form such as
the following, with only a **numId** attribute and an element referring
to an abstract numbering definition:

.. code-block:: xml

    <w:num w:numId="2">
      <w:abstractNumId w:val="4" />
    </w:num>

The abstract numbering definition contains the substantive styling information
for lists, namely the level-specific display of the bullet or numeral
and its placement. For example,

.. code-block:: xml

    <w:abstractNum w:abstractNumId="4">
      <w:nsid w:val="FFFFFF7F" />
      <w:multiLevelType w:val="singleLevel" />
      <w:lvl w:ilvl="0">
        <w:start w:val="1" />
        <w:lvlText w:val="%1." />
        <w:lvlJc w:val="start" />
        <w:pPr>
          <w:tabs>
            <w:tab w:val="num" w:pos="720" />
          </w:tabs>
          <w:ind w:start="720" w:hanging="360" />
        </w:pPr>
      </w:lvl>
    </w:abstractNum>

Low- to High-level support
--------------------------

The structure of the ``docx`` module can be 
profitably understood by identifying the
levels of representation that it operates
at, and the subsystem that acts upon
that representation.

We arrange them in order of increasing abstraction
from a raw WordProcessingML file.

1.  Packaged OPC file **[python-opc]**
2.  Serialized XML **[lxml]**
3.  Deserialized XML **[xmlchemy]**
4.  Module-specific primitives **[python-docx]**
5.  High-level representations **[user]**

Support for a given operation can be considered
as a gradient (not Boolean) quality: the fewer
levels of representation a user must traverse
to accomplish an operation, the more
*supported* the operation is.

Issue #122 on the master branch GitHub page
discusses difficulties with creating or styling
complex lists with the ``docx`` module.
Basically, there is no high-level support
for functions such as
creating multi-level lists, nested lists,
and restarting numbering.
The maintainer has commented that:

-   The standard itself involves a highly cumbersome
    method for achieving these kinds of effects
    (this is indeed true), making it difficult
    to decide on the best way to expose the
    various functions to users; and
-   It is, however, possible to achieve the desired
    effects with significant effort: work
    on the raw XML representation, given 
    knowledge of the standard.

The issue is also discussed on StackOverflow
at https://stackoverflow.com/questions/23446268

Currently, 
looking to the hierarchy above,
access to most parts of the structure relating
to list styles and numbering definitions is only through
a deserialized XML ("Level 3") representation.
Full API support would imply access to a "Level 5"
representation.
Decisions about simplifying the implementation of
numbered lists w/r/t the ISO standard are most
likely to come up when developing "Level 5"
support.
However, it should be uncontroversial to adhere
to the ISO standard very closely when developing
"Level 4" support. This means that the level of
*support* for advanced list operations can
be increased through some straightforward 
**xmlchemy**-based declarations,
and high-level design questions need not come
into play.

This is done through two main programming tasks:

1.  Declare relevant XML types following the ``wml.xsd`` schema
    (ISO-29500-1 Appendix A.1).
2.  Instruct ``xmlchemy`` to recognize a relevant tag 
    as an instance of the appropriate type.

If this is accomplished, various low-level methods will
be exposed which abstract the necessary XML manipulations,
allowing for improved access to desired functions for
a user familiar with the semantics of the ISO standard.

Pull Request #XX is concerned with updating the module
to declare the following types and expose them to
``xmlchemy``-based methods:

+-------------------+
|XML Type           |
+===================+
|CT_NumPicBullet    |          
+-------------------+
|CT_AbstractNum     |         
+-------------------+
|CT_LongHexNumber   |           
+-------------------+
|ST_LongHexNumber   |           
+-------------------+
|CT_MultiLevelType  |            
+-------------------+
|ST_MultiLevelType  |            
+-------------------+
|CT_Lvl             | 
+-------------------+
|CT_NumFmt          |    
+-------------------+
|ST_NumberFormat    |          
+-------------------+
|CT_LevelSuffix     |         
+-------------------+
|ST_LevelSuffix     |         
+-------------------+
|CT_LevelText       |       
+-------------------+
|CT_LvlLegacy       |       
+-------------------+
|CT_Num             | 
+-------------------+

Having defined these types and trained the parser to
associate them with elements in the namespace
(this is done through calls to ``register_element_cls``
in ``oxml.__init__``), it is possible to implement
solutions to the documented issues noted above in
a disciplined way.

Making use of low-level support
-------------------------------
Once the types listed above are defined and the **xmlchemy**
submodule methods can be used, it becomes a little less
painful to implement a solution to the StackOverflow
question referred to above.


.. code-block:: python


    #!/usr/bin/python
    
    from docx import Document
    from docx import oxml
    
    
    d = Document()
    
    
    """
    1. Create an abstract numbering definition for a multi-level numbering style.
    """
    numXML = d.part.numbering_part.numbering_definitions._numbering
    nextAbstractId = max([ J.abstractNumId for J in numXML.abstractNum_lst ] ) + 1
    l = numXML.add_abstractNum()
    l.abstractNumId = nextAbstractId
    m = l.add_multiLevelType()
    m.val = 'multiLevel'
    
    
    """
    2. Define numbering formats for each (zero-indexed)
        level. N.B. The formatting text is one-indexed.
        The user agent will accept up to nine levels.
    """
    formats = {0: "decimal", 1: "upperLetter" }
    textFmts = {0: '%1.', 1: '%2.' }
    for i in range(2):
        lvl = l.add_lvl()
        lvl.ilvl = i
        n = lvl.add_numFmt()
        n.val = formats[i]
        lt = lvl.add_lvlText()
        lt.val = textFmts[i]
    
    """
    3. Link the abstract numbering definition to a numbering definition.
    """
    n = numXML.add_num(nextAbstractId)
    
    """
    4. Define a function to set the (0-indexed) numbering level of a paragraph.
    """
    def set_ilvl(p,ilvl):
        pr = p._element._add_pPr()
        np = pr.get_or_add_numPr()
        il = np.get_or_add_ilvl()
        il.val = ilvl
        ni = np.get_or_add_numId()
        ni.val = n.numId
        return(p)
    
    """
    5. Create some content
    """
    for x in [1,2,3]:
        p = d.add_paragraph()
        set_ilvl(p,0)
        p.add_run("Question %i" % x)
        for y in [1,2,3,4]:
            p2 = d.add_paragraph()
            set_ilvl(p2,1)
            p2.add_run("Choice %i" % y)
    
    
    d.save('test.docx')

Element Semantics
-----------------

This section contains excerpts from ISO-29500-1 describing
how the user agent should handle 
``<w:numPr>``, ``<w:num>``, ``<w:abstractNum>``, and their 
descendants (section references are to parts of ISO-29500-1).

**numPr** (§17.3.1.19)
    This element specifies that the current paragraph uses numbering information that is defined by a particular
    numbering definition instance.
    The presence of this element specifies that the paragraph inherits the properties specified by the numbering
    definition in the ``num`` element (§17.9.15) at the level specified by the level specified in the ``lvl`` element (§17.9.6)
    and shall have an associated number positioned before the beginning of the text flow in this paragraph. When
    this element appears as part of the paragraph formatting for a paragraph style, then any numbering level
    defined using the ``ilvl`` element shall be ignored, and the ``pStyle`` element (§17.9.23) on the associated abstract
    numbering definition shall be used instead.
``ilvl`` (§17.9.3)
    This element specifies the numbering level of the numbering definition instance which shall be applied to the
    parent paragraph. Its ``val`` attribute is a zero-based index.
``numId`` (§17.9.18)
    This element specifies the numbering definition instance which shall be used for the given parent numbered
    paragraph in the WordprocessingML document.
``numberingChange``
    Removed. Previously defined in ECMA-376:2006.
``ins`` (§17.13.5.19)
    This element specifies that the numbering information defined by the parent element shall be treated as
    numbering information which was recorded as an insertion using revisions.
**num** (§17.9.15)
    This element specifies a unique instance of numbering information that can be referenced by zero or more
    paragraphs within the parent WordprocessingML document.
    This instance requires the referencing of a base abstract numbering definition through the ``abstractNumId`` child
    element (§17.9.2). This element also can be used to specify a set of optional overrides applied to zero or more
    levels from the abstract numbering definition inherited by this instance through the optional ``lvlOverride``
    child elements (§17.9.8).
``abstractNumId`` (§17.9.2)
    This element specifies the abstract numbering definition information whose properties shall be inherited by the
    parent numbering definition instance.
``lvlOverride`` (§17.9.8)
    This element specifies an optional override which shall be applied in place of zero or more levels from the
    abstract numbering definition for a given numbering definition instance. Each instance of this element is used to
    override the appearance and behavior of a given numbering level definition within the given abstract numbering
    definition.
**abstractNum** (§17.9.1)
    This element specifies a set of properties which shall dictate the appearance and behavior of a set of numbered
    paragraphs in a WordprocessingML document. These properties are collectively called an *abstract numbering
    definition*, and are the basis for all numbering information in a WordprocessingML document.
    Although an abstract numbering definition contains a complete set of numbering, it shall not be directly
    referenced by content (hence the use of abstract). Instead, these properties shall be inherited by a numbering
    definition instance using the ``num`` element (§17.9.15), which can then itself be referenced by content.
``nsid`` (§17.9.14)
    This element associates a unique hexadecimal ID to the parent abstract numbering definition. This number shall
    be identical for two abstract numbering definitions that are based from the same initial numbering definition --- if
    a document is repurposed and the underlying numbering definition is changed, it shall maintain its original ``nsid``.
    If this element is omitted, then the list shall have no nsid and one can be added by a producer arbitrarily.
``multiLevelType`` (§17.9.12)
    This element specifies the type of numbering defined by a given abstract numbering type. This information shall
    only be used by a consumer to determine user interface behaviors for this numbering definition, and shall not
    be used to limit the behavior of the list (i.e. a list with multiple levels marked as ``singleLevel`` shall not be
    prevented from using levels 2 through 9).
    If this element is omitted, then the list shall be assumed to be of any numbering type desired by the consumer.
``tmpl`` (§17.9.29)
    This element specifies a unique hexadecimal code which can be used to determine a location within application
    user interface in which this abstract numbering definition shall be displayed.
    If this element is omitted, then this abstract numbering definition can be displayed in any location chosen by the
    consumer.
``name`` (§17.9.13)
    This element specifies the name of a given abstract numbering definition. This name can be surfaced in order to
    provide a user friendly alias for a given numbering definition, but shall not influence the behavior of the list -
    two identical definitions with different name elements shall behave identically.
    If this element is omitted, then this abstract numbering definition shall have no name.
``styleLink`` (§17.9.27)
    This element specifies that the parent abstract numbering definition is the base numbering definition for the
    specified numbering style referenced in its ``val`` attribute.
    If this element is omitted, or it references a style which does not exist, then this numbering definition shall not
    be the underlying properties for a numbering style.
``numStyleLink`` (§17.9.21)
    This element specifies an abstract numbering that does not contain the actual numbering properties for its
    numbering type, but rather serves as a reference to a numbering style stored in the document, which shall be
    applied when this abstract numbering definition is referenced, and itself points at the actual underlying abstract
    numbering definition to be used.
    The numbering style that is to be applied when this abstract numbering definition is referenced is identified by
    the string contained in ``numStyleLink``'s ``val`` attribute.
**lvl**  (§17.9.6)
    This element specifies the appearance and behavior of a numbering level within a given abstract numbering
    definition. A numbering level contains a set of properties for the display of the numbering for a given numbering
    level within an abstract numbering definition.
    A numbering level definition is identical to a numbering level override definition, except for the fact that it is
    defined as part of a numbering definition instance using the ``abstractNum`` element (§17.9.1) rather than as part
    of an abstract numbering definition using the ``num`` element (§17.9.15).
``start`` (§17.9.25)
    This element specifies the starting value for the numbering used by the parent numbering level within a given
    numbering level definition. This value is used when this level initially starts in a document, as well as whenever it
    is restarted via the properties set in the ``lvlRestart`` element (§17.9.10).
    If this element is omitted, then the starting value shall be zero ( 0 ).
``numFmt`` (§17.9.17)
    This element specifies the number format that shall be used to display all numbering at this level in the
    numbering definition. This information is used to replace the level text string %x , where x is a particular one-
    based level index, with the appropriate value unless the ``numFmt`` value is bullet , in which case the literal text
    of the level text string is used. This value shall be calculated by counting the number of paragraphs at this level
    since the last restart using the numbering system defined in the val attribute.
    When a document has a custom number format specified by the format attribute, it shall use the referenced
    number format. If the referenced number format cannot be resolved as a number format the consumer shall
    use the number format specified by the value of the val attribute. If the corresponding value of the val attribute
    is custom , the result is implementation-defined.
    If this element is omitted, the level shall be assumed to be of level type ``decimal``.
``lvlRestart`` (§17.9.10)
    This element specifies a one-based index which determines when a numbering level should restart to its ``start``
    value (§17.9.25). A numbering level restarts when an instance of the specified numbering level, which shall be
    higher (earlier than this level) or any earlier level is used in the given document's contents. [Example: If this
    value is 2, then both level two and level one reset this value. end example]
    If this element is omitted, the numbering level shall restart each time the previous numbering level or any
    earlier level is used. If the specified level is higher than the current level, then this element shall be ignored. As
    well, a value of 0 shall specify that this level shall never restart.
``pStyle`` (§17.9.23)
    This element specifies the name of a paragraph style which shall automatically apply to this numbering level when
    applied to the contents of the document. When a paragraph style is defined to include a numbering definition,
    any numbering level defined by the ``numPr`` element (§17.3.1.19) shall be ignored, and instead this element shall
    specify the numbering level associated with that paragraph style.
    If this element references a style which does not exist, or is not a paragraph style, then it can be ignored.
``isLgl`` (§17.9.4)
    This element specifies whether or not all levels displayed for a given numbering level's text shall be displayed
    using the decimal number format, regardless of the actual number format of that level in the list. [Note: This
    numbering style is often referred to as the legal numbering style. end note]
    If this element is present, then all numbering levels present in the ``lvlTxt`` element (§17.9.11) shall be converted
    to their decimal equivalents when they are displayed in this level in the numbering format. If this element is
    omitted, then each level is displayed using the ``numFmt`` (§17.9.17) of that level.
``suff`` (§17.9.28)
    This element specifies the content which shall be added between a given numbering level's text and the text of
    every numbered paragraph which references that numbering level.
    If this element is omitted, then its value shall be assumed to be tab.
``lvlText`` (§17.9.11)
    This element specifies the textual content which shall be displayed when displaying a paragraph with the given
    numbering level.
    All text in this element's val attribute shall be taken as literal text to be repeated in each instance of this
    numbering level, except for any use of the percent symbol (%) followed by a number, which shall be used to
    indicate the one-based index of the number to be used at this level. Any number of a level higher than this level
    shall be ignored.
    When the % syntax is used, the number shall be incremented for each subsequent paragraph of that level
    (sequential or not), until the restart level is seen between two subsequent paragraphs of this level.
``lvlPicBulletId`` (§17.9.9)
    This element specifies a picture which shall be used as a numbering symbol for a given numbering level by
    referring to a picture numbering symbol definition's ``numPictBullet`` element (§17.9.20). This reference is made
    through this element's ``val`` attribute.
    The picture shall be added to the numbering level by replacing each character in the ``lvlText`` with one instance
    of this image.
``legacy`` 
    not in current standard
``lvlJc`` (§17.9.7)
    This element specifies the type of justification used on a numbering level's text within a given numbering level.
    This justification is applied relative to the text margin of the parent numbered paragraph in the document.
    If omitted, the paragraph shall have left justification relative to the text margin in left-to-right paragraphs, and
    right justification relative to the text margin in right-to-left paragraphs.
    A numbering level's text is the numeral, symbol, character, graphic, etc. used to create a numbered paragraph as
    defined by the lvlText element (§17.9.11).
``pPr`` (§17.9.22)
    This element specifies the paragraph properties which shall be applied as part of a given numbering level within
    the parent numbering definition. These paragraph properties are applied to any numbered paragraph that
    references the given numbering definition and numbering level.
    Paragraph properties specified on the numbered paragraph itself override the paragraph properties specified by
    ``pPr`` elements within a numbering ``lvl`` element (§17.9.5, §17.9.6).
``rPr`` (§17.9.24)
    This element specifies the run properties which shall be applied to the numbering level's text specified in the
    ``lvlText`` element (§17.9.11) when it is applied to paragraphs in this document.
    These run properties are applied to all numbering level text used by a given abstract numbering definition and
    numbering level. It should be noted that run properties specified on a numbered paragraph itself, or on text
    runs within a numbered paragraph, are separate from the run properties specified by ``rPr`` elements within a
    numbering level, as the latter affects only the numbering text itself, not the remainder of runs in the numbered
    paragraph.
    

Applicable Schema Definitions
-----------------------------

This section contains excerpts from the schema **wmd.xsd**
which will be necessary to develop basic support for
parsing **numbering.xml** files and enabling **xmlchemy**
functionality for numbering definitions.

Once a type is appropriately defined in the source
and the parser is given instructions on which tags
to associate it with, then low-level **xmlchemy**
methods can be used to manipulate the XML directly
or write API functions.

Schemata are given in the remainder of this
section for the 
unimplemented (as of version 0.8.7) types which are necessary to
implement suport for numbering styles.


**<w:numbering>** ``CT_Numbering``

.. code-block:: xml

  <xsd:complexType name="CT_Numbering">
    <xsd:sequence>
      <xsd:element name="numPicBullet" type="CT_NumPicBullet" minOccurs="0" maxOccurs="unbounded"/>
      <xsd:element name="abstractNum" type="CT_AbstractNum" minOccurs="0" maxOccurs="unbounded"/>
      <xsd:element name="num" type="CT_Num" minOccurs="0" maxOccurs="unbounded"/>
      <xsd:element name="numIdMacAtCleanup" type="CT_DecimalNumber" minOccurs="0"/>
    </xsd:sequence>
  </xsd:complexType>

**<w:numPicBullet>** ``CT_NumPicBullet``

.. code-block:: xml

  <xsd:complexType name="CT_NumPicBullet">
    <xsd:choice>
      <xsd:element name="pict" type="CT_Picture"/>
      <xsd:element name="drawing" type="CT_Drawing"/>
    </xsd:choice>
    <xsd:attribute name="numPicBulletId" type="ST_DecimalNumber" use="required"/>
  </xsd:complexType>

**<w:abstractNum>** ``CT_AbstractNum``

.. code-block:: xml

  <xsd:complexType name="CT_AbstractNum">
    <xsd:sequence>
      <xsd:element name="nsid" type="CT_LongHexNumber" minOccurs="0"/>
      <xsd:element name="multiLevelType" type="CT_MultiLevelType" minOccurs="0"/>
      <xsd:element name="tmpl" type="CT_LongHexNumber" minOccurs="0"/>
      <xsd:element name="name" type="CT_String" minOccurs="0"/>
      <xsd:element name="styleLink" type="CT_String" minOccurs="0"/>
      <xsd:element name="numStyleLink" type="CT_String" minOccurs="0"/>
      <xsd:element name="lvl" type="CT_Lvl" minOccurs="0" maxOccurs="9"/>
    </xsd:sequence>
    <xsd:attribute name="abstractNumId" type="ST_DecimalNumber" use="required"/>
  </xsd:complexType>

``CT_LongHexNumber``

.. code-block:: xml

  <xsd:complexType name="CT_LongHexNumber">
    <xsd:attribute name="val" type="ST_LongHexNumber" use="required"/>
  </xsd:complexType>

  <xsd:simpleType name="ST_LongHexNumber">
    <xsd:restriction base="xsd:hexBinary">
      <xsd:length value="4"/>
    </xsd:restriction>
  </xsd:simpleType>

**<w:multiLevelType>** ``CT_MultiLevelType``

.. code-block:: xml

  <xsd:complexType name="CT_MultiLevelType">
    <xsd:attribute name="val" type="ST_MultiLevelType" use="required"/>
  </xsd:complexType>

  <xsd:simpleType name="ST_MultiLevelType">
    <xsd:restriction base="xsd:string">
      <xsd:enumeration value="singleLevel"/>
      <xsd:enumeration value="multilevel"/>
      <xsd:enumeration value="hybridMultilevel"/>
    </xsd:restriction>
  </xsd:simpleType>

**<w:lvl>** ``CT_Lvl``

.. code-block:: xml

  <xsd:complexType name="CT_Lvl">
    <xsd:sequence>
      <xsd:element name="start" type="CT_DecimalNumber" minOccurs="0"/>
      <xsd:element name="numFmt" type="CT_NumFmt" minOccurs="0"/>
      <xsd:element name="lvlRestart" type="CT_DecimalNumber" minOccurs="0"/>
      <xsd:element name="pStyle" type="CT_String" minOccurs="0"/>
      <xsd:element name="isLgl" type="CT_OnOff" minOccurs="0"/>
      <xsd:element name="suff" type="CT_LevelSuffix" minOccurs="0"/>
      <xsd:element name="lvlText" type="CT_LevelText" minOccurs="0"/>
      <xsd:element name="lvlPicBulletId" type="CT_DecimalNumber" minOccurs="0"/>
      <xsd:element name="legacy" type="CT_LvlLegacy" minOccurs="0"/>
      <xsd:element name="lvlJc" type="CT_Jc" minOccurs="0"/>
      <xsd:element name="pPr" type="CT_PPrGeneral" minOccurs="0"/>
      <xsd:element name="rPr" type="CT_RPr" minOccurs="0"/>
    </xsd:sequence>
    <xsd:attribute name="ilvl" type="ST_DecimalNumber" use="required"/>
    <xsd:attribute name="tplc" type="ST_LongHexNumber" use="optional"/>
    <xsd:attribute name="tentative" type="s:ST_OnOff" use="optional"/>
  </xsd:complexType>

**<w:numFmt>** ``CT_NumFmt``

.. code-block:: xml

  <xsd:complexType name="CT_NumFmt">
    <xsd:attribute name="val" type="ST_NumberFormat" use="required"/>
    <xsd:attribute name="format" type="s:ST_String" use="optional"/>
  </xsd:complexType>

  <xsd:simpleType name="ST_NumberFormat">
    <xsd:restriction base="xsd:string">
      <xsd:enumeration value="decimal"/>
      <xsd:enumeration value="upperRoman"/>
      <xsd:enumeration value="lowerRoman"/>
      <xsd:enumeration value="upperLetter"/>
      <xsd:enumeration value="lowerLetter"/>
      <xsd:enumeration value="ordinal"/>
      <xsd:enumeration value="cardinalText"/>
      <xsd:enumeration value="ordinalText"/>
      <xsd:enumeration value="hex"/>
      <xsd:enumeration value="chicago"/>
      <xsd:enumeration value="ideographDigital"/>
      <xsd:enumeration value="japaneseCounting"/>
      <xsd:enumeration value="aiueo"/>
      <xsd:enumeration value="iroha"/>
      <xsd:enumeration value="decimalFullWidth"/>
      <xsd:enumeration value="decimalHalfWidth"/>
      <xsd:enumeration value="japaneseLegal"/>
      <xsd:enumeration value="japaneseDigitalTenThousand"/>
      <xsd:enumeration value="decimalEnclosedCircle"/>
      <xsd:enumeration value="decimalFullWidth2"/>
      <xsd:enumeration value="aiueoFullWidth"/>
      <xsd:enumeration value="irohaFullWidth"/>
      <xsd:enumeration value="decimalZero"/>
      <xsd:enumeration value="bullet"/>
      <xsd:enumeration value="ganada"/>
      <xsd:enumeration value="chosung"/>
      <xsd:enumeration value="decimalEnclosedFullstop"/>
      <xsd:enumeration value="decimalEnclosedParen"/>
      <xsd:enumeration value="decimalEnclosedCircleChinese"/>
      <xsd:enumeration value="ideographEnclosedCircle"/>
      <xsd:enumeration value="ideographTraditional"/>
      <xsd:enumeration value="ideographZodiac"/>
      <xsd:enumeration value="ideographZodiacTraditional"/>
      <xsd:enumeration value="taiwaneseCounting"/>
      <xsd:enumeration value="ideographLegalTraditional"/>
      <xsd:enumeration value="taiwaneseCountingThousand"/>
      <xsd:enumeration value="taiwaneseDigital"/>
      <xsd:enumeration value="chineseCounting"/>
      <xsd:enumeration value="chineseLegalSimplified"/>
      <xsd:enumeration value="chineseCountingThousand"/>
      <xsd:enumeration value="koreanDigital"/>
      <xsd:enumeration value="koreanCounting"/>
      <xsd:enumeration value="koreanLegal"/>
      <xsd:enumeration value="koreanDigital2"/>
      <xsd:enumeration value="vietnameseCounting"/>
      <xsd:enumeration value="russianLower"/>
      <xsd:enumeration value="russianUpper"/>
      <xsd:enumeration value="none"/>
      <xsd:enumeration value="numberInDash"/>
      <xsd:enumeration value="hebrew1"/>
      <xsd:enumeration value="hebrew2"/>
      <xsd:enumeration value="arabicAlpha"/>
      <xsd:enumeration value="arabicAbjad"/>
      <xsd:enumeration value="hindiVowels"/>
      <xsd:enumeration value="hindiConsonants"/>
      <xsd:enumeration value="hindiNumbers"/>
      <xsd:enumeration value="hindiCounting"/>
      <xsd:enumeration value="thaiLetters"/>
      <xsd:enumeration value="thaiNumbers"/>
      <xsd:enumeration value="thaiCounting"/>
      <xsd:enumeration value="bahtText"/>
      <xsd:enumeration value="dollarText"/>
      <xsd:enumeration value="custom"/>
    </xsd:restriction>
  </xsd:simpleType>

**<w:suff>** ``CT_LevelSuffix``

.. code-block:: xml

  <xsd:complexType name="CT_LevelSuffix">
    <xsd:attribute name="val" type="ST_LevelSuffix" use="required"/>
  </xsd:complexType>

  <xsd:simpleType name="ST_LevelSuffix">
    <xsd:restriction base="xsd:string">
      <xsd:enumeration value="tab"/>
      <xsd:enumeration value="space"/>
      <xsd:enumeration value="nothing"/>
    </xsd:restriction>
  </xsd:simpleType>

**<w:lvlText>** ``CT_LevelText``

.. code-block:: xml

  <xsd:complexType name="CT_LevelText">
    <xsd:attribute name="val" type="s:ST_String" use="optional"/>
    <xsd:attribute name="null" type="s:ST_OnOff" use="optional"/>
  </xsd:complexType>

**<w:legacy>** ``CT_LvlLegacy``

.. code-block:: xml

  <xsd:complexType name="CT_LvlLegacy">
    <xsd:attribute name="legacy" type="s:ST_OnOff" use="optional"/>
    <xsd:attribute name="legacySpace" type="s:ST_TwipsMeasure" use="optional"/>
    <xsd:attribute name="legacyIndent" type="ST_SignedTwipsMeasure" use="optional"/>
  </xsd:complexType>


**<w:num>** ``CT_Num``

.. code-block:: xml

  <xsd:complexType name="CT_Num">
    <xsd:sequence>
      <xsd:element name="abstractNumId" type="CT_DecimalNumber" minOccurs="1"/>
      <xsd:element name="lvlOverride" type="CT_NumLvl" minOccurs="0" maxOccurs="9"/>
    </xsd:sequence>
    <xsd:attribute name="numId" type="ST_DecimalNumber" use="required"/>
  </xsd:complexType>


.. [#first] ISO/IEC 29500-1:2012(E) at 684.
