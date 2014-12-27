
Style objects
=============


Candidate protocols
-------------------

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
