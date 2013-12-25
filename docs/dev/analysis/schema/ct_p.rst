
CT_P
====

.. csv-table::
   :header-rows: 0
   :stub-columns: 1
   :widths: 15, 50

   Spec Name    , Paragraph
   Tag(s)       , w:p
   Namespace    , wordprocessingml (wml.xsd)
   Spec Section , 17.3.1.22


Schema excerpt
--------------

.. highlight:: xml

::

  <xsd:complexType name="CT_P">
    <xsd:sequence>
      <xsd:element name="pPr" type="CT_PPr" minOccurs="0"/>
      <xsd:group   ref="EG_PContent"        minOccurs="0" maxOccurs="unbounded"/>
    </xsd:sequence>
    <xsd:attribute name="rsidRPr"      type="ST_LongHexNumber"/>
    <xsd:attribute name="rsidR"        type="ST_LongHexNumber"/>
    <xsd:attribute name="rsidDel"      type="ST_LongHexNumber"/>
    <xsd:attribute name="rsidP"        type="ST_LongHexNumber"/>
    <xsd:attribute name="rsidRDefault" type="ST_LongHexNumber"/>
  </xsd:complexType>

  <xsd:complexType name="CT_Text">
    <xsd:simpleContent>
      <xsd:extension base="s:ST_String">
        <xsd:attribute ref="xml:space" use="optional"/>
      </xsd:extension>
    </xsd:simpleContent>
  </xsd:complexType>

  <xsd:group name="EG_PContent">
    <xsd:choice>
      <xsd:group   ref="EG_ContentRunContent"             minOccurs="0" maxOccurs="unbounded"/>
      <xsd:element name="fldSimple" type="CT_SimpleField" minOccurs="0" maxOccurs="unbounded"/>
      <xsd:element name="hyperlink" type="CT_Hyperlink"/>
      <xsd:element name="subDoc"    type="CT_Rel"/>
    </xsd:choice>
  </xsd:group>

  <xsd:group name="EG_ContentRunContent">
    <xsd:choice>
      <xsd:element name="customXml" type="CT_CustomXmlRun"/>
      <xsd:element name="smartTag"  type="CT_SmartTagRun"/>
      <xsd:element name="sdt"       type="CT_SdtRun"/>
      <xsd:element name="dir"       type="CT_DirContentRun"/>
      <xsd:element name="bdo"       type="CT_BdoContentRun"/>
      <xsd:element name="r"         type="CT_R"/>
      <xsd:group ref="EG_RunLevelElts" minOccurs="0" maxOccurs="unbounded"/>
    </xsd:choice>
  </xsd:group>

  <xsd:complexType name="CT_R">
    <xsd:sequence>
      <xsd:group ref="EG_RPr"             minOccurs="0"/>
      <xsd:group ref="EG_RunInnerContent" minOccurs="0" maxOccurs="unbounded"/>
    </xsd:sequence>
    <xsd:attribute name="rsidRPr" type="ST_LongHexNumber"/>
    <xsd:attribute name="rsidDel" type="ST_LongHexNumber"/>
    <xsd:attribute name="rsidR"   type="ST_LongHexNumber"/>
  </xsd:complexType>

  <xsd:group name="EG_RunInnerContent">
    <xsd:choice>
      <xsd:element name="br"                    type="CT_Br"/>
      <xsd:element name="t"                     type="CT_Text"/>
      <xsd:element name="contentPart"           type="CT_Rel"/>
      <xsd:element name="delText"               type="CT_Text"/>
      <xsd:element name="instrText"             type="CT_Text"/>
      <xsd:element name="delInstrText"          type="CT_Text"/>
      <xsd:element name="noBreakHyphen"         type="CT_Empty"/>
      <xsd:element name="softHyphen"            type="CT_Empty"  minOccurs="0"/>
      <xsd:element name="dayShort"              type="CT_Empty"  minOccurs="0"/>
      <xsd:element name="monthShort"            type="CT_Empty"  minOccurs="0"/>
      <xsd:element name="yearShort"             type="CT_Empty"  minOccurs="0"/>
      <xsd:element name="dayLong"               type="CT_Empty"  minOccurs="0"/>
      <xsd:element name="monthLong"             type="CT_Empty"  minOccurs="0"/>
      <xsd:element name="yearLong"              type="CT_Empty"  minOccurs="0"/>
      <xsd:element name="annotationRef"         type="CT_Empty"  minOccurs="0"/>
      <xsd:element name="footnoteRef"           type="CT_Empty"  minOccurs="0"/>
      <xsd:element name="endnoteRef"            type="CT_Empty"  minOccurs="0"/>
      <xsd:element name="separator"             type="CT_Empty"  minOccurs="0"/>
      <xsd:element name="continuationSeparator" type="CT_Empty"  minOccurs="0"/>
      <xsd:element name="sym"                   type="CT_Sym"    minOccurs="0"/>
      <xsd:element name="pgNum"                 type="CT_Empty"  minOccurs="0"/>
      <xsd:element name="cr"                    type="CT_Empty"  minOccurs="0"/>
      <xsd:element name="tab"                   type="CT_Empty"  minOccurs="0"/>
      <xsd:element name="object"                type="CT_Object"/>
      <xsd:element name="pict"                  type="CT_Picture"/>
      <xsd:element name="fldChar"               type="CT_FldChar"/>
      <xsd:element name="ruby"                  type="CT_Ruby"/>
      <xsd:element name="footnoteReference"     type="CT_FtnEdnRef"/>
      <xsd:element name="endnoteReference"      type="CT_FtnEdnRef"/>
      <xsd:element name="commentReference"      type="CT_Markup"/>
      <xsd:element name="drawing"               type="CT_Drawing"/>
      <xsd:element name="ptab"                  type="CT_PTab"   minOccurs="0"/>
      <xsd:element name="lastRenderedPageBreak" type="CT_Empty"  minOccurs="0" maxOccurs="1"/>
    </xsd:choice>
  </xsd:group>
