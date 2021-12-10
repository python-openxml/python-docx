
Style objects
=============

A style is one of four types; character, paragraph, table, or numbering. All
style objects have behavioral properties and formatting properties. The set of
formatting properties varies depending on the style type. In general,
formatting properties are inherited along this hierarchy: character ->
paragraph -> table. A numbering style has no formatting properties and does
not inherit.

Behavioral properties
---------------------

There are six behavior properties:

hidden
    Style operates to assign formatting properties, but does not appear in
    the UI under any circumstances. Used for *internal* styles assigned by an
    application that should not be under the control of an end-user.

priority
    Determines the sort order of the style in sequences presented by the UI.

semi-hidden
    The style is hidden from the so-called "main" user interface. In Word
    this means the *recommended list* and the style gallery. The style still
    appears in the *all styles* list.

unhide_when_used
    Flag to the application to set semi-hidden False when the style is next
    used.

quick_style
    Show the style in the style gallery when it is not hidden.

locked
    Style is hidden and cannot be applied when document formatting protection
    is active.


hidden
------

The `hidden` attribute doesn't work on built-in styles and its behavior on
custom styles is spotty. Skipping this attribute for now. Will reconsider if
someone requests it and can provide a specific use case.

Behavior
~~~~~~~~

**Scope.** `hidden` doesn't work at all on 'Normal' or 'Heading 1' style. It
doesn't work on Salutation either. There is no `w:defHidden` attribute on
`w:latentStyles`, lending credence to the hypothesis it is not enabled for
built-in styles. *Hypothesis:* Doesn't work on built-in styles.

**UI behavior.** A custom style having `w:hidden` set |True| is hidden from
the gallery and all styles pane lists. It does however appear in the "Current
style of selected text" box in the styles pane when the cursor is on
a paragraph of that style. The style can be modified by the user from this
current style UI element. The user can assign a new style to a paragraph
having a hidden style.


priority
--------

The `priority` attribute is the integer primary sort key determining the
position of a style in a UI list. The secondary sort is alphabetical by name.
Negative values are valid, although not assigned by Word itself and appear to
be treated as 0.

Behavior
~~~~~~~~

**Default.** Word behavior appears to default priority to 0 for custom
styles. The spec indicates the effective default value is conceptually
infinity, such that the style appears at the end of the styles list,
presumably alphabetically among other styles having no priority assigned.

Candidate protocol
~~~~~~~~~~~~~~~~~~

::

    >>> style = document.styles['Foobar']
    >>> style.priority
    None
    >>> style.priority = 7
    >>> style.priority
    7
    >>> style.priority = -42
    >>> style.priority
    0


semi-hidden
-----------

The `w:semiHidden` element specifies visibility of the style in the so-called
*main* user interface. For Word, this means the style gallery and the
recommended, styles-in-use, and in-current-document lists. The all-styles
list and current-style dropdown in the styles pane would then be considered
part of an *advanced* user interface.

Behavior
~~~~~~~~

**Default.** If the `w:semiHidden` element is omitted, its effective value is
|False|. There is no inheritance of this value.

**Scope.** Works on both built-in and custom styles.

**Word behavior.** Word does not use the `@w:val` attribute. It writes
`<w:semiHidden/>` for |True| and omits the element for |False|.

Candidate protocol
~~~~~~~~~~~~~~~~~~

::

    >>> style = document.styles['Foo']
    >>> style.hidden
    False
    >>> style.hidden = True
    >>> style.hidden
    True

Example XML
~~~~~~~~~~~

.. highlight:: xml

style.hidden = True::

  <w:style w:type="paragraph" w:styleId="Foo">
    <w:name w:val="Foo"/>
    <w:semiHidden/>
  </w:style>

style.hidden = False::

  <w:style w:type="paragraph" w:styleId="Foo">
    <w:name w:val="Foo"/>
  </w:style>

Alternate constructions should also report the proper value but not be
used when writing XML::

  <w:style w:type="paragraph" w:styleId="Foo">
    <w:name w:val="Foo"/>
    <w:semiHidden w:val="0"/>  <!-- style.hidden is False -->
  </w:style>

  <w:style w:type="paragraph" w:styleId="Foo">
    <w:name w:val="Foo"/>
    <w:semiHidden w:val="1"/>  <!-- style.hidden is True -->
  </w:style>


unhide-when-used
----------------

The `w:unhideWhenUsed` element signals an application that this style should
be made visibile the next time it is used.

Behavior
~~~~~~~~

**Default.** If the `w:unhideWhenUsed` element is omitted, its effective
value is |False|. There is no inheritance of this value.

**Word behavior.** The `w:unhideWhenUsed` element is not changed or removed
when the style is next used. Only the `w:semiHidden` element is affected, if
present. Presumably this is so a style can be re-hidden, to be unhidden on
the subsequent use.

Note that this behavior in Word is only triggered by a user actually applying
a style. Merely loading a document having the style applied somewhere in its
contents does not cause the `w:semiHidden` element to be removed.

Candidate protocol
~~~~~~~~~~~~~~~~~~

.. highlight:: python

::

    >>> style = document.styles['Foo']
    >>> style.unhide_when_used
    False
    >>> style.unhide_when_used = True
    >>> style.unhide_when_used
    True

Example XML
~~~~~~~~~~~

.. highlight:: xml

style.unhide_when_used = True::

  <w:style w:type="paragraph" w:styleId="Foo">
    <w:name w:val="Foo"/>
    <w:semiHidden/>
    <w:unhideWhenUsed/>
  </w:style>

style.unhide_when_used = False::

  <w:style w:type="paragraph" w:styleId="Foo">
    <w:name w:val="Foo"/>
  </w:style>

Alternate constructions should also report the proper value but not be
used when writing XML::

  <w:style w:type="paragraph" w:styleId="Foo">
    <w:name w:val="Foo"/>
    <w:unhideWhenUsed w:val="0"/>  <!-- style.unhide_when_used is False -->
  </w:style>

  <w:style w:type="paragraph" w:styleId="Foo">
    <w:name w:val="Foo"/>
    <w:unhideWhenUsed w:val="1"/>  <!-- style.unhide_when_used is True -->
  </w:style>


quick-style
-----------

The `w:qFormat` element specifies whether Word should display this style in
the style gallery. In order to appear in the gallery, this attribute must be
|True| and `hidden` must be |False|.

Behavior
~~~~~~~~

**Default.** If the `w:qFormat` element is omitted, its effective value is
|False|. There is no inheritance of this value.

**Word behavior.** If `w:qFormat` is |True| and the style is not hidden, it
will appear in the gallery in the order specified by `w:uiPriority`.

Candidate protocol
~~~~~~~~~~~~~~~~~~

.. highlight:: python

::

    >>> style = document.styles['Foo']
    >>> style.quick_style
    False
    >>> style.quick_style = True
    >>> style.quick_style
    True

Example XML
~~~~~~~~~~~

.. highlight:: xml

style.quick_style = True::

  <w:style w:type="paragraph" w:styleId="Foo">
    <w:name w:val="Foo"/>
    <w:qFormat/>
  </w:style>

style.quick_style = False::

  <w:style w:type="paragraph" w:styleId="Foo">
    <w:name w:val="Foo"/>
  </w:style>

Alternate constructions should also report the proper value but not be
used when writing XML::

  <w:style w:type="paragraph" w:styleId="Foo">
    <w:name w:val="Foo"/>
    <w:qFormat w:val="0"/>  <!-- style.quick_style is False -->
  </w:style>

  <w:style w:type="paragraph" w:styleId="Foo">
    <w:name w:val="Foo"/>
    <w:qFormat w:val="1"/>  <!-- style.quick_style is True -->
  </w:style>


locked
------

The `w:locked` element specifies whether Word should prevent this style from
being applied to content. This behavior is only active if formatting
protection is turned on.

Behavior
~~~~~~~~

**Default.** If the `w:locked` element is omitted, its effective value is
|False|. There is no inheritance of this value.

Candidate protocol
~~~~~~~~~~~~~~~~~~

.. highlight:: python

::

    >>> style = document.styles['Foo']
    >>> style.locked
    False
    >>> style.locked = True
    >>> style.locked
    True

Example XML
~~~~~~~~~~~

.. highlight:: xml

style.locked = True::

  <w:style w:type="paragraph" w:styleId="Foo">
    <w:name w:val="Foo"/>
    <w:locked/>
  </w:style>

style.locked = False::

  <w:style w:type="paragraph" w:styleId="Foo">
    <w:name w:val="Foo"/>
  </w:style>

Alternate constructions should also report the proper value but not be
used when writing XML::

  <w:style w:type="paragraph" w:styleId="Foo">
    <w:name w:val="Foo"/>
    <w:locked w:val="0"/>  <!-- style.locked is False -->
  </w:style>

  <w:style w:type="paragraph" w:styleId="Foo">
    <w:name w:val="Foo"/>
    <w:locked w:val="1"/>  <!-- style.locked is True -->
  </w:style>


Candidate protocols
-------------------

.. highlight:: python

Identification::

    >>> style = document.styles['Body Text']
    >>> style.name
    'Body Text'
    >>> style.style_id
    'BodyText'
    >>> style.type
    WD_STYLE_TYPE.PARAGRAPH (1)

`delete()`::

    >>> len(styles)
    6
    >>> style.delete()
    >>> len(styles)
    5
    >>> styles['Citation']
    KeyError: no style with id or name 'Citation'

Style.base_style::

    >>> style = styles.add_style('Citation', WD_STYLE_TYPE.PARAGRAPH)
    >>> style.base_style
    None
    >>> style.base_style = styles['Normal']
    >>> style.base_style
    <docx.styles.style._ParagraphStyle object at 0x10a7a9550>
    >>> style.base_style.name
    'Normal'


Example XML
-----------

.. highlight:: xml

::

  <w:styles>

    <!-- ... -->

    <w:style w:type="paragraph" w:default="1" w:styleId="Normal">
      <w:name w:val="Normal"/>
      <w:qFormat/>
    </w:style>
    <w:style w:type="character" w:default="1" w:styleId="DefaultParagraphFont">
      <w:name w:val="Default Paragraph Font"/>
      <w:uiPriority w:val="1"/>
      <w:semiHidden/>
      <w:unhideWhenUsed/>
    </w:style>
    <w:style w:type="table" w:default="1" w:styleId="TableNormal">
      <w:name w:val="Normal Table"/>
      <w:uiPriority w:val="99"/>
      <w:semiHidden/>
      <w:unhideWhenUsed/>
      <w:tblPr>
        <w:tblInd w:w="0" w:type="dxa"/>
        <w:tblCellMar>
          <w:top w:w="0" w:type="dxa"/>
          <w:left w:w="108" w:type="dxa"/>
          <w:bottom w:w="0" w:type="dxa"/>
          <w:right w:w="108" w:type="dxa"/>
        </w:tblCellMar>
      </w:tblPr>
    </w:style>
    <w:style w:type="numbering" w:default="1" w:styleId="NoList">
      <w:name w:val="No List"/>
      <w:uiPriority w:val="99"/>
      <w:semiHidden/>
      <w:unhideWhenUsed/>
    </w:style>

    <w:style w:type="paragraph" w:customStyle="1" w:styleId="Foobar">
      <w:name w:val="Foobar"/>
      <w:basedOn w:val="Normal"/>
      <w:qFormat/>
    </w:style>

  </w:styles>


Schema excerpt
--------------

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

  <xsd:complexType name="CT_OnOff">
    <xsd:attribute name="val" type="s:ST_OnOff"/>
  </xsd:complexType>

  <xsd:complexType name="CT_String">
    <xsd:attribute name="val" type="s:ST_String" use="required"/>
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

  <xsd:simpleType name="ST_StyleType">
    <xsd:restriction base="xsd:string">
      <xsd:enumeration value="paragraph"/>
      <xsd:enumeration value="character"/>
      <xsd:enumeration value="table"/>
      <xsd:enumeration value="numbering"/>
    </xsd:restriction>
  </xsd:simpleType>
