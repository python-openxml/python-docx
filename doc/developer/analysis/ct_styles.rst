#############
``CT_Styles``
#############

.. highlight:: xml

.. csv-table::
   :header-rows: 0
   :stub-columns: 1
   :widths: 15, 50

   Schema Name,  CT_Styles
   Spec Name,    Styles
   Tag(s),       w:styles
   Namespace,    wordprocessingml (wml.xsd)
   Spec Section, 17.7.4.18


Analysis
========

Only styles with an explicit ``<w:style>`` definition affect the formatting
of paragraphs that are assigned that style.

Word includes behavior definitions (``<w:lsdException>`` elements) for the
"latent" styles that are built in to the Word client. These are present in a
new document created from install defaults.

Word does not add a formatting definition (``<w:style>`` element) for a
built-in style until it is used.

Once present in ``styles.xml``, Word does not remove a style element when it
is no longer used by any paragraphs. The definition of each of the styles
ever used in a document are accumulated in ``styles.xml``.


attributes
^^^^^^^^^^

None.


child elements
^^^^^^^^^^^^^^

============  ====  ================
name            #   type
============  ====  ================
docDefaults     ?   CT_DocDefaults
latentStyles    ?   CT_LatentStyles
style          \*   CT_TextParagraph
============  ====  ================


Spec text
^^^^^^^^^

   This element specifies all of the style information stored in the
   WordprocessingML document: style definitions as well as latent style
   information.

   Example: The Normal paragraph style in a word processing document can have
   any number of formatting properties, e.g. font face = Times New Roman; font
   size = 12pt; paragraph justification = left. All paragraphs which reference
   this paragraph style would automatically inherit these properties.


Schema excerpt
^^^^^^^^^^^^^^

::

  <xsd:complexType name="CT_Styles">
    <xsd:sequence>
      <xsd:element name="docDefaults"  type="CT_DocDefaults"  minOccurs="0"/>
      <xsd:element name="latentStyles" type="CT_LatentStyles" minOccurs="0" maxOccurs="1"/>
      <xsd:element name="style"        type="CT_Style"        minOccurs="0" maxOccurs="unbounded"/>
    </xsd:sequence>
  </xsd:complexType>

  <xsd:complexType name="CT_DocDefaults">
    <xsd:sequence>
      <xsd:element name="rPrDefault" type="CT_RPrDefault" minOccurs="0"/>
      <xsd:element name="pPrDefault" type="CT_PPrDefault" minOccurs="0"/>
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

  <xsd:complexType name="CT_Style">
    <xsd:sequence>
      <xsd:element name="name"            type="CT_String"        minOccurs="0" maxOccurs="1"/>
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
      <xsd:element name="pPr"             type="CT_PPrGeneral"    minOccurs="0" maxOccurs="1"/>
      <xsd:element name="rPr"             type="CT_RPr"           minOccurs="0" maxOccurs="1"/>
      <xsd:element name="tblPr"           type="CT_TblPrBase"     minOccurs="0" maxOccurs="1"/>
      <xsd:element name="trPr"            type="CT_TrPr"          minOccurs="0" maxOccurs="1"/>
      <xsd:element name="tcPr"            type="CT_TcPr"          minOccurs="0" maxOccurs="1"/>
      <xsd:element name="tblStylePr"      type="CT_TblStylePr"    minOccurs="0" maxOccurs="unbounded"/>
    </xsd:sequence>
    <xsd:attribute name="type"        type="ST_StyleType" use="optional"/>
    <xsd:attribute name="styleId"     type="s:ST_String"  use="optional"/>
    <xsd:attribute name="default"     type="s:ST_OnOff"   use="optional"/>
    <xsd:attribute name="customStyle" type="s:ST_OnOff"   use="optional"/>
  </xsd:complexType>

  <xsd:complexType name="CT_LsdException">
    <xsd:attribute name="name"           type="s:ST_String" use="required"/>
    <xsd:attribute name="locked"         type="s:ST_OnOff"/>
    <xsd:attribute name="uiPriority"     type="ST_DecimalNumber"/>
    <xsd:attribute name="semiHidden"     type="s:ST_OnOff"/>
    <xsd:attribute name="unhideWhenUsed" type="s:ST_OnOff"/>
    <xsd:attribute name="qFormat"        type="s:ST_OnOff"/>
  </xsd:complexType>
