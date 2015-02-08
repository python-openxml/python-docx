
Styles
======

.. toctree::
   :titlesonly:

   styles
   style
   paragraph-style
   character-style
   latent-styles

Word supports the definition of *styles* to allow a group of formatting
properties to be easily and consistently applied to a paragraph, run, table,
or numbering scheme, all at once. The mechanism is similar to how Cascading
Style Sheets (CSS) works with HTML.

Styles are defined in the ``styles.xml`` package part and are keyed to
a paragraph, run, or table using the `styleId` string.

Style visual behavior
---------------------

* **Sort order.** Built-in styles appear in order of the effective value of
  their `uiPriority` attribute. By default, a custom style will not receive
  a `uiPriority` attribute, causing its effective value to default to 0. This
  will generlly place custom styles at the top of the sort order. A set of
  styles having the same `uiPriority` value will be sub-sorted in
  alphabetical order.

  If a `uiPriority` attribute is defined for a custom style, that style is
  interleaved with the built-in styles, according to their `uiPriority`
  value. The `uiPriority` attribute takes a signed integer, and accepts
  negative numbers. Note that Word does not allow the use of negative
  integers via its UI; rather it allows the `uiPriority` number of built-in
  types to be increased to produce the desired sorting behavior.

* **Identification.** A style is identified by its name, not its styleId
  attribute. The styleId is used only for internal linking of an object like
  a paragraph to a style. The styleId may be changed by the application, and
  in fact is routinely changed by Word on each save to be a transformation of
  the name.

  *Hypothesis.* Word calculates the `styleId` by removing all spaces from the
  style name.

* **List membership.** There are four style list options in the styles panel:

  + *Recommended.* The recommended list contains all latent and defined
    styles that have `semiHidden` == |False|.

  + *Styles in Use.* The styles-in-use list contains all styles that have
    been applied to content in the document (implying they are defined) that
    also have `semiHidden` == |False|.

  + *In Current Document.* The in-current-document list contains all defined
    styles in the document having `semiHidden` == |False|.

  + *All Styles.* The all-styles list contains all latent and defined
    styles in the document.

* **Definition of built-in style.** When a built-in style is added to
  a document (upon first use), the value of each of the `locked`,
  `uiPriority` and `qFormat` attributes from its latent style definition (the
  `latentStyles` attributes overridden by those of any `lsdException`
  element) is used to override the corresponding value in the inserted style
  definition from their built-in defaults.

* Each built-in style has default attributes that can be revealed by setting
  the `latentStyles/@count` attribute to 0 and inspecting the style in the
  style manager. This may include default behavioral properties.

* Anomaly. Style "No Spacing" does not appear in the recommended list even
  though its behavioral attributes indicate it should. (Google indicates it
  may be a legacy style from Word 2003).

* Word has 267 built-in styles, listed here:
  http://www.thedoctools.com/downloads/DocTools_List_Of_Built-in_Style_English_Danish_German_French.pdf

  Note that at least one other sources has the number at 276 rather than 267.

* **Appearance in the Style Gallery.** A style appears in the style gallery
  when: `semiHidden` == |False| and `qFormat` == |True|


Glossary
--------

built-in style
    One of a set of standard styles known to Word, such as "Heading 1".
    Built-in styles are presented in Word's style panel whether or not they
    are actually defined in the styles part.

latent style
    A built-in style having no definition in a particular document is known
    as a *latent style* in that document.

style definition
    A ``<w:style>`` element in the styles part that explicitly defines the
    attributes of a style.

recommended style list
    A list of styles that appears in the styles toolbox or panel when
    "Recommended" is selected from the "List:" dropdown box.


Word behavior
-------------

If no style having an assigned style id is defined in the styles part, the
style application has no effect.

Word does not add a formatting definition (``<w:style>`` element) for a
built-in style until it is used.

Once present in the styles part, Word does not remove a built-in style
definition if it is no longer applied to any content. The definition of each
of the styles ever used in a document are accumulated in its ``styles.xml``.


Related MS API *(partial)*
--------------------------

* Document.Styles
* Styles.Add, .Item, .Count, access by name, e.g. Styles("Foobar")
* Style.BaseStyle
* Style.Builtin
* Style.Delete()
* Style.Description
* Style.Font
* Style.Linked
* Style.LinkStyle
* Style.LinkToListTemplate()
* Style.ListLevelNumber
* Style.ListTemplate
* Style.Locked
* Style.NameLocal
* Style.NameParagraphStyle
* Style.NoSpaceBetweenParagraphsOfSameStyle
* Style.ParagraphFormat
* Style.Priority
* Style.QuickStyle
* Style.Shading
* Style.Table(Style)
* Style.Type
* Style.UnhideWhenUsed
* Style.Visibility


Enumerations
------------

* WdBuiltinStyle


Example XML
-----------

.. highlight:: xml

::

   <?xml version='1.0' encoding='UTF-8' standalone='yes'?>
   <w:styles
       xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006"
       xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"
       xmlns:w14="http://schemas.microsoft.com/office/word/2010/wordml"
       xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"
       mc:Ignorable="w14"
       >
     <w:docDefaults>
       <w:rPrDefault>
         <w:rPr>
           <w:rFonts w:asciiTheme="minorHAnsi" w:eastAsiaTheme="minorEastAsia"
                     w:hAnsiTheme="minorHAnsi" w:cstheme="minorBidi"/>
           <w:sz w:val="24"/>
           <w:szCs w:val="24"/>
           <w:lang w:val="en-US" w:eastAsia="en-US" w:bidi="ar-SA"/>
         </w:rPr>
       </w:rPrDefault>
       <w:pPrDefault/>
     </w:docDefaults>
     <w:latentStyles w:defLockedState="0" w:defUIPriority="99" w:defSemiHidden="1"
                     w:defUnhideWhenUsed="1" w:defQFormat="0" w:count="276">
       <w:lsdException w:name="Normal" w:semiHidden="0" w:uiPriority="0"
                       w:unhideWhenUsed="0" w:qFormat="1"/>
       <w:lsdException w:name="heading 1" w:semiHidden="0" w:uiPriority="9"
                       w:unhideWhenUsed="0" w:qFormat="1"/>
       <w:lsdException w:name="heading 2" w:uiPriority="9" w:qFormat="1"/>
       <w:lsdException w:name="Default Paragraph Font" w:uiPriority="1"/>
     </w:latentStyles>
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
       <w:qFormat/>
       <w:rsid w:val="004B54E0"/>
     </w:style>
   </w:styles>


Schema excerpt
--------------

::

  <xsd:complexType name="CT_Styles">
    <xsd:sequence>
      <xsd:element name="docDefaults"  type="CT_DocDefaults"  minOccurs="0"/>
      <xsd:element name="latentStyles" type="CT_LatentStyles" minOccurs="0"/>
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

  <xsd:simpleType name="ST_StyleType">
    <xsd:restriction base="xsd:string">
      <xsd:enumeration value="paragraph"/>
      <xsd:enumeration value="character"/>
      <xsd:enumeration value="table"/>
      <xsd:enumeration value="numbering"/>
    </xsd:restriction>
  </xsd:simpleType>
