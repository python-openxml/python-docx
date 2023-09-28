
Latent Styles
=============

Latent style definitions are a "stub" style definition specifying behavioral
(UI display) attributes for built-in styles.


Latent style collection
-----------------------

The latent style collection for a document is accessed using the
:attr:`~.Styles.latent_styles` property on |Styles|::

    >>> latent_styles = document.styles.latent_styles
    >>> latent_styles
    <docx.styles.LatentStyles object at 0x1045dd550>

**Iteration.** |LatentStyles| should support iteration of contained
|_LatentStyle| objects in document order.

**Latent style access.** A latent style can be accessed by name using
dictionary-style notation.

**len().** |LatentStyles| supports :meth:`len`, reporting the number of
|_LatentStyle| objects it contains.


|LatentStyles| properties
-------------------------


default_priority
~~~~~~~~~~~~~~~~

**XML semantics**. According to ISO 29500, the default value if the
`w:defUIPriority` attribute is omitted is 99. 99 is explictly set in the
default Word `styles.xml`, so will generally be what one finds.

**Protocol**::

    >>> # return None if attribute is omitted
    >>> latent_styles.default_priority
    None
    >>> # but expect is will almost always be explicitly 99
    >>> latent_styles.default_priority
    99
    >>> latent_styles.default_priority = 42
    >>> latent_styles.default_priority
    42


load_count
~~~~~~~~~~

**XML semantics**. No default is stated in the spec. Don't allow assignment
of |None|.

**Protocol**::

    >>> latent_styles.load_count
    276
    >>> latent_styles.load_count = 242
    >>> latent_styles.load_count
    242


Boolean properties
~~~~~~~~~~~~~~~~~~

There are four boolean properties that all share the same protocol:

* default_to_hidden
* default_to_locked
* default_to_quick_style
* default_to_unhide_when_used

**XML semantics**. Defaults to |False| if the attribute is omitted. However,
the attribute should always be written explicitly on update.

**Protocol**::

    >>> latent_styles.default_to_hidden
    False
    >>> latent_styles.default_to_hidden = True
    >>> latent_styles.default_to_hidden
    True


Specimen XML
~~~~~~~~~~~~

.. highlight:: xml

The `w:latentStyles` element used in the default Word 2011 template::

  <w:latentStyles w:defLockedState="0" w:defUIPriority="99" w:defSemiHidden="1"
                  w:defUnhideWhenUsed="1" w:defQFormat="0" w:count="276">


|_LatentStyle| properties
-------------------------

.. highlight:: python

::

    >>> latent_style = latent_styles.latent_styles[0]

    >>> latent_style.name
    'Normal'

    >>> latent_style.priority
    None
    >>> latent_style.priority = 10
    >>> latent_style.priority
    10

    >>> latent_style.locked
    None
    >>> latent_style.locked = True
    >>> latent_style.locked
    True

    >>> latent_style.quick_style
    None
    >>> latent_style.quick_style = True
    >>> latent_style.quick_style
    True


Latent style behavior
---------------------

* A style has two categories of attribute, `behavioral` and `formatting`.
  Behavioral attributes specify where and when the style should appear in the
  user interface. Behavioral attributes can be specified for latent styles
  using the ``<w:latentStyles>`` element and its ``<w:lsdException>`` child
  elements. The 5 behavioral attributes are:

  + locked
  + uiPriority
  + semiHidden
  + unhideWhenUsed
  + qFormat

* **locked**. The `locked` attribute specifies that the style should not
  appear in any list or the gallery and may not be applied to content. This
  behavior is only active when restricted formatting is turned on.

  Locking is turned on via the menu: Developer Tab > Protect Document >
  Formatting Restrictions (Windows only).

* **uiPriority**. The `uiPriority` attribute acts as a sort key for
  sequencing style names in the user interface. Both the lists in the styles
  panel and the Style Gallery are sensitive to this setting. Its effective
  value is 0 if not specified.

* **semiHidden**. The `semiHidden` attribute causes the style to be excluded
  from the recommended list. The notion of `semi` in this context is that
  while the style is hidden from the recommended list, it still appears in
  the "All Styles" list. This attribute is removed on first application of
  the style if an `unhideWhenUsed` attribute set |True| is also present.

* **unhideWhenUsed**. The `unhideWhenUsed` attribute causes any `semiHidden`
  attribute to be removed when the style is first applied to content. Word
  does `not` remove the `semiHidden` attribute just because there exists an
  object in the document having that style. The `unhideWhenUsed` attribute is
  not removed along with the `semiHidden` attribute when the style is
  applied.

  The `semiHidden` and `unhideWhenUsed` attributes operate in combination to
  produce *hide-until-used* behavior.

  *Hypothesis.* The persistance of the `unhideWhenUsed` attribute after
  removing the `semiHidden` attribute on first application of the style is
  necessary to produce appropriate behavior in style inheritance situations.
  In that case, the `semiHidden` attribute may be explictly set to |False| to
  override an inherited value. Or it could allow the `semiHidden` attribute
  to be re-set to |True| later while preserving the hide-until-used behavior.

* **qFormat**. The `qFormat` attribute specifies whether the style should
  appear in the Style Gallery when it appears in the recommended list.
  A style will never appear in the gallery unless it also appears in the
  recommended list.

* Latent style attributes are only operative for latent styles. Once a style
  is defined, the attributes of the definition exclusively determine style
  behavior; no attributes are inherited from its corresponding latent style
  definition.


Specimen XML
------------

.. highlight:: xml

::

  <w:latentStyles w:defLockedState="0" w:defUIPriority="99" w:defSemiHidden="1"
                  w:defUnhideWhenUsed="1" w:defQFormat="0" w:count="276">
    <w:lsdException w:name="Normal" w:semiHidden="0" w:uiPriority="0"
                    w:unhideWhenUsed="0" w:qFormat="1"/>
    <w:lsdException w:name="heading 1" w:semiHidden="0" w:uiPriority="9"
                    w:unhideWhenUsed="0" w:qFormat="1"/>
    <w:lsdException w:name="caption" w:uiPriority="35" w:qFormat="1"/>
    <w:lsdException w:name="Default Paragraph Font" w:uiPriority="1"/>
    <w:lsdException w:name="Bibliography" w:uiPriority="37"/>
    <w:lsdException w:name="TOC Heading" w:uiPriority="39" w:qFormat="1"/>
  </w:latentStyles>


Schema excerpt
--------------

.. highlight:: xml

::

  <xsd:complexType name="CT_Styles">
    <xsd:sequence>
      <xsd:element name="docDefaults"  type="CT_DocDefaults"  minOccurs="0"/>
      <xsd:element name="latentStyles" type="CT_LatentStyles" minOccurs="0"/>
      <xsd:element name="style"        type="CT_Style"        minOccurs="0" maxOccurs="unbounded"/>
    </xsd:sequence>
  </xsd:complexType>

  <xsd:complexType name="CT_LatentStyles">
    <xsd:sequence>
      <xsd:element name="lsdException" type="CT_LsdException" minOccurs="0" maxOccurs="unbounded"/>
    </xsd:sequence>
    <xsd:attribute name="defLockedState"    type="s:ST_OnOff"/>
    <xsd:attribute name="defUIPriority"     type="ST_DecimalNumber"/>
    <xsd:attribute name="defSemiHidden"     type="s:ST_OnOff"/>
    <xsd:attribute name="defUnhideWhenUsed" type="s:ST_OnOff"/>
    <xsd:attribute name="defQFormat"        type="s:ST_OnOff"/>
    <xsd:attribute name="count"             type="ST_DecimalNumber"/>
  </xsd:complexType>

  <xsd:complexType name="CT_LsdException">
    <xsd:attribute name="name"           type="s:ST_String"   use="required"/>
    <xsd:attribute name="locked"         type="s:ST_OnOff"/>
    <xsd:attribute name="uiPriority"     type="ST_DecimalNumber"/>
    <xsd:attribute name="semiHidden"     type="s:ST_OnOff"/>
    <xsd:attribute name="unhideWhenUsed" type="s:ST_OnOff"/>
    <xsd:attribute name="qFormat"        type="s:ST_OnOff"/>
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
