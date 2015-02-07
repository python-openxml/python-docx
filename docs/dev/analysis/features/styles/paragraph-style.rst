
Paragraph Style
===============

A paragraph style provides character formatting (font) as well as paragraph
formatting properties. Character formatting is inherited from
|_CharacterStyle| and is predominantly embodied in the :attr:`font` property.
Likewise, most paragraph-specific properties come from the |ParagraphFormat|
object available on the :attr:`paragraph_format` property.

A handful of other properties are specific to a paragraph style.


next_paragraph_style
--------------------

The `next_paragraph_style` property provides access to the style that will
automatically be assigned by Word to a new paragraph inserted after
a paragraph with this style. This property is most useful for a style that
would normally appear only once in a sequence, such as a heading.

The default is to use the same style for an inserted paragraph. This
addresses the most common case; for example, a body paragraph having `Body
Text` style would normally be followed by a paragraph of the same style.


Expected usage
~~~~~~~~~~~~~~

The priority use case for this property is to provide a working style that
can be assigned to a paragraph. The property will always provide a valid
paragraph style, defaulting to the current style whenever a more specific one
cannot be determined.

While this obscures some specifics of the situation from the API, it
addresses the expected most common use case. Developers needing to detect,
for example, missing styles can readily use the oxml layer to inspect the
XML and further features can be added if those use cases turn out to be more
common than expected.


Behavior
~~~~~~~~

**Default.** The default next paragraph style is the same paragraph style.

The default is used whenever the next paragraph style is not specified or is
invalid, including these conditions:

* No `w:next` child element is present
* A style having the styleId specified in `w:next/@w:val` is not present in
  the document.
* The style specified in `w:next/@w:val` is not a paragraph style.

In all these cases the current style (`self`) is returned.


Example XML
~~~~~~~~~~~

.. highlight:: xml

paragraph_style.next_paragraph_style is styles['Bar']::

  <w:style w:type="paragraph" w:styleId="Foo">
    <w:name w:val="Foo"/>
    <w:next w:val="Bar"/>
  </w:style>

**Semantics.** The `w:next` child element is optional.

* When omitted, the next style is the same as the current style.
* If no style with a matching styleId exists, the `w:next` element is ignored
  and the next style is the same as the current style.
* If a style is found but is of a style type other than paragraph, the
  `w:next` element is ignored and the next style is the same as the current
  style.


Candidate protocol
~~~~~~~~~~~~~~~~~~

.. highlight:: python

::

    >>> styles = document.styles

    >>> paragraph_style = styles['Foo']
    >>> paragraph_style.next_paragraph_style == paragraph_style
    True

    >>> paragraph_style.next_paragraph_style = styles['Bar']
    >>> paragraph_style.next_paragraph_style == styles['Bar']
    True

    >>> paragraph_style.next_paragraph_style = None
    >>> paragraph_style.next_paragraph_style == paragraph_style
    True


Schema excerpt
--------------

.. highlight:: xml

::

  <xsd:complexType name="CT_Style">
    <xsd:sequence>
      <xsd:element name="name"            type="CT_String"        minOccurs="0"/>
      <xsd:element name="aliases"         type="CT_String"        minOccurs="0"/>
      <xsd:element name="basedOn"         type="CT_String"        minOccurs="0"/>
      <xsd:element name="next"            type="CT_String"        minOccurs="0"/>
      <xsd:element name="link"            type="CT_String"        minOccurs="0"/>
      <xsd:element name="autoRedefine"    type="CT_OnOff"         minOccurs="0"/>
      <xsd:element name="hidden"          type="CT_OnOff"         minOccurs="0"/>
      <xsd:element name="uiPriority"      type="CT_DecimalNumber" minOccurs="0"/>
      <xsd:element name="semiHidden"      type="CT_OnOff"         minOccurs="0"/>
      <xsd:element name="unhideWhenUsed"  type="CT_OnOff"         minOccurs="0"/>
      <xsd:element name="qFormat"         type="CT_OnOff"         minOccurs="0"/>
      <xsd:element name="locked"          type="CT_OnOff"         minOccurs="0"/>
      <xsd:element name="personal"        type="CT_OnOff"         minOccurs="0"/>
      <xsd:element name="personalCompose" type="CT_OnOff"         minOccurs="0"/>
      <xsd:element name="personalReply"   type="CT_OnOff"         minOccurs="0"/>
      <xsd:element name="rsid"            type="CT_LongHexNumber" minOccurs="0"/>
      <xsd:element name="pPr"             type="CT_PPrGeneral"    minOccurs="0"/>
      <xsd:element name="rPr"             type="CT_RPr"           minOccurs="0"/>
      <xsd:element name="tblPr"           type="CT_TblPrBase"     minOccurs="0"/>
      <xsd:element name="trPr"            type="CT_TrPr"          minOccurs="0"/>
      <xsd:element name="tcPr"            type="CT_TcPr"          minOccurs="0"/>
      <xsd:element name="tblStylePr"      type="CT_TblStylePr"    minOccurs="0" maxOccurs="unbounded"/>
    </xsd:sequence>
    <xsd:attribute name="type"        type="ST_StyleType"/>
    <xsd:attribute name="styleId"     type="s:ST_String"/>
    <xsd:attribute name="default"     type="s:ST_OnOff"/>
    <xsd:attribute name="customStyle" type="s:ST_OnOff"/>
  </xsd:complexType>

  <xsd:complexType name="CT_String">
    <xsd:attribute name="val" type="s:ST_String" use="required"/>
  </xsd:complexType>
