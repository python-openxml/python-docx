Section with multiple Columns
=============================

Word provides means for the end-user to create document sections with multiple
columns. By default, all columns within a section are of the same width and
equally spaced. A user may customize width and spacing (margin-right) of all or
any individual column. Also a separator line may be displayed.

Schema analysis
---------------

In a WordprocessingML document, the number of section columns and their geometry
is defined within `w:cols` element (optional, typed as `CT_Columns`) of a
`sectPr` structure. The type spec follows:

.. highlight:: xml

::

  <xsd:complexType name="CT_Columns">
    <xsd:sequence minOccurs="0">
      <xsd:element name="col" type="CT_Column" maxOccurs="45"/>
    </xsd:sequence>
      <xsd:attribute name="equalWidth" type="s:ST_OnOff"/>
      <xsd:attribute name="space"      type="s:ST_TwipsMeasure"/>
      <xsd:attribute name="num"        type="ST_DecimalNumber"/>
      <xsd:attribute name="sep"        type="s:ST_OnOff"/>
  </xsd:complexType>

Here are the attribute details:
 *  `equalWidth` - if defined must be either `true` or `false`. When set to `true`
    or not defined the width of columns is equal (auto-calculated). When set to
    `false` the element must contain children of type `CT_Column` where the number
    of children must be equal to the value of `num` attribute and shall not
    exceed 45.
 *  `space` - defines the spacing between columns in Twips. Can exist only if
    `equalWidth` is not defined or is set to true. Seems to be present by default at
    720 Twips.
 *  `num` - defines the number of columns within a section. This attribute is
    not present by default. Also seems to be limited in range to [1 .. 45].
    Word 2010 further limits that number depending on the page orientation and
    size: for A4 portrait max is 12 while for A4 landscape max is 20.
    <b>Design Decision:</b> keep original schema limit of 45, skip page size
    checks but document observations of Word behaviors.
    <b>Alternative:</b> implement max logic based on page width.
 *  `sep` - if defined must be either `true` or `false`. When set to `true` a
    solid black line is displayed between each pair of columns. When set to `false`
    or not defined no visual separator is shown. So far I couldn't find a way to
    customize the appearance of this separator.

For individual column geometry definition `equalWidth` attribute shall be set to
`true` and the element shall contain children of `CT_Column` type.
The type specification follows: ::

  <xsd:complexType name="CT_Column">
    <xsd:attribute name="w"     type="s:ST_TwipsMeasure"/>
    <xsd:attribute name="space" type="s:ST_TwipsMeasure"/>
  </xsd:complexType>

where:
 *  `w` defines the column width (in Twips)
 *  `space` defines column spacing (in fact - margin-right), optional, Twips.
    If it is the last column this attribute shall not be used.

Candidate Protocol
------------------

Basic functionality
~~~~~~~~~~~~~~~~~~~

.. highlight:: python

:class:`docx.Section` has a columns property::

    >>> from docx import Document
    >>> from docx.section import Section, Columns
    >>> from docx.enum.section import WD_SECTION
    >>> section = Document().add_section(WD_SECTION.NEW_PAGE)
    >>> isinstance(section, Section)
    True
    >>> columns = section.columns
    >>> isinstance(columns, Columns)
    True

:class:`docx.section.Columns` has read/write :attr:`number`, :attr:`spacing`,
:attr:`equal_width` and :attr:`separator` properties.

default state of :attr:`number` is None in this case section contains a
single column:

    >>> columns.number
    None
    >>> columns.number = 3
    >>> columns.number
    3

this however shall not create children of `CT_Column` type unless
:attr:`equal_width` was set false previously.

    >>> len(columns)
    0

while :attr:`number` value is > 1 Word seems to set default spacing at 708 Twips
(libre-office sets at 0).

    >>> columns.number = None
    >>> columns.spacing
    708

Advanced functionality
~~~~~~~~~~~~~~~~~~~~~~
I can hardly imagine a use-case where a machine-generated document with
multiple columns will require individual column width setting however we should
implement this capability for the sake of consistency.

    >>> columns.number = 3
    >>> len(columns)
    None
    >>> columns.equal_width = False
    >>> len(columns)
    3
    >>> columns[0].width = Cm(3)
    >>> columns[0].spacing = Cm(2)
    >>> columns[1].width = Cm(4)
    >>> columns[1].spacing = Cm(2)
    >>> columns[2].width = Cm(5)
    >>> columns.equal_width = True
    >>> len(columns)
    0
    >>> columns[1].width
    IndexError: list index out of range

Specimen XML
------------
All xml samples within this section were obtained using Word 2010.
Implementing same cases in libre-office and then saving as .docx will result in
a slightly different xml. Re-opening in Word 2010 however shows a correct
visual result.

Case 1:
If documnt is created by Word 2010 and `columns.number` is `None` or "1" then
`w:cols` attribute is present in `sectPr`:

.. highlight:: xml

::

  <w:cols w:space="708"/>

Case 2:
If `columns.number` is 2 and the other columns properties are default then
`sectPr` shall contain the following xml: ::

    <w:cols w:num="2" w:space="708"/>

Case 3:
If `columns.number` is 3, spacing set to Cm(1) and separator set True then
`sectPr` shall contain the following xml: ::

    <w:cols w:num="3" w:space="567" w:sep="1"/>

Case 4:
If `columns.number` is 3, equal_width set to False, first column width is Cm(4),
spacing is Cm(0.2), second column width is 5, spacing is Cm(0.3) and the third
column width is Cm(7) then `sectPr` shall contain the following xml: ::

    <w:cols w:num="3" w:space="113" w:equalwidth="0">
      <w:col w:w="2268" w:space="113"/>
      <w:col w:w="2835" w:space="170"/>
      <w:col w:w="3969"/>
    </w:cols>
