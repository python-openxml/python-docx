
Styles collection
=================


Candidate protocols
-------------------

Access::

    >>> styles = document.styles  # default styles part added if not present
    >>> styles
    <docx.styles.styles.Styles object at 0x1045dd550>

Iteration and length::

    >>> len(styles)
    10
    >>> list_styles = [s for s in styles if s.type == WD_STYLE_TYPE.LIST]
    >>> len(list_styles)
    3

Access style by name (or style id)::

    >>> styles['Normal']
    <docx.styles.style._ParagraphStyle object at 0x1045dd550>

    >>> styles['undefined-style']
    KeyError: no style with id or name 'undefined-style'

:meth:`.Styles.add_style()`::

    >>> style = styles.add_style('Citation', WD_STYLE_TYPE.PARAGRAPH)
    >>> style.name
    'Citation'
    >>> style.type
    PARAGRAPH (1)
    >>> style.builtin
    False


Feature Notes
-------------

* could add a default builtin style from known specs on first access via
  WD_BUILTIN_STYLE enumeration::

      >>> style = document.styles['Heading1']
      KeyError: no style with id or name 'Heading1'
      >>> style = document.styles[WD_STYLE.HEADING_1]
      >>> assert style == document.styles['Heading1']


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
