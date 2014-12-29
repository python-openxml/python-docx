
Run-level content
=================

A run is the object most closely associated with inline content; text,
pictures, and other items that are flowed between the block-item boundaries
within a paragraph.

main content child elements:

* <w:t>
* <w:br>
* <w:drawing>
* <w:tab>
* <w:cr>


Schema excerpt
--------------

.. highlight:: xml

::

  <xsd:complexType name="CT_R">  <!-- denormalized -->
    <xsd:sequence>
      <xsd:element name="rPr" type="CT_RPr" minOccurs="0"/>
      <xsd:group   ref="EG_RunInnerContent" minOccurs="0" maxOccurs="unbounded"/>
    </xsd:sequence>
    <xsd:attribute name="rsidRPr" type="ST_LongHexNumber"/>
    <xsd:attribute name="rsidDel" type="ST_LongHexNumber"/>
    <xsd:attribute name="rsidR"   type="ST_LongHexNumber"/>
  </xsd:complexType>

  <xsd:group name="EG_RunInnerContent">
    <xsd:choice>
      <xsd:element name="t"                     type="CT_Text"/>
      <xsd:element name="br"                    type="CT_Br"/>
      <xsd:element name="cr"                    type="CT_Empty"/>
      <xsd:element name="tab"                   type="CT_Empty"/>
      <xsd:element name="ptab"                  type="CT_PTab"/>
      <xsd:element name="sym"                   type="CT_Sym"/>
      <xsd:element name="noBreakHyphen"         type="CT_Empty"/>
      <xsd:element name="softHyphen"            type="CT_Empty"/>
      <xsd:element name="fldChar"               type="CT_FldChar"/>
      <xsd:element name="drawing"               type="CT_Drawing"/>
      <xsd:element name="object"                type="CT_Object"/>

      <xsd:element name="footnoteReference"     type="CT_FtnEdnRef"/>
      <xsd:element name="footnoteRef"           type="CT_Empty"/>
      <xsd:element name="endnoteReference"      type="CT_FtnEdnRef"/>
      <xsd:element name="endnoteRef"            type="CT_Empty"/>
      <xsd:element name="separator"             type="CT_Empty"/>
      <xsd:element name="continuationSeparator" type="CT_Empty"/>
      <xsd:element name="commentReference"      type="CT_Markup"/>
      <xsd:element name="annotationRef"         type="CT_Empty"/>

      <xsd:element name="contentPart"           type="CT_Rel"/>
      <xsd:element name="delText"               type="CT_Text"/>
      <xsd:element name="instrText"             type="CT_Text"/>
      <xsd:element name="delInstrText"          type="CT_Text"/>

      <xsd:element name="dayShort"              type="CT_Empty"/>
      <xsd:element name="monthShort"            type="CT_Empty"/>
      <xsd:element name="yearShort"             type="CT_Empty"/>
      <xsd:element name="dayLong"               type="CT_Empty"/>
      <xsd:element name="monthLong"             type="CT_Empty"/>
      <xsd:element name="yearLong"              type="CT_Empty"/>

      <xsd:element name="pgNum"                 type="CT_Empty"/>
      <xsd:element name="pict"                  type="CT_Picture"/>
      <xsd:element name="ruby"                  type="CT_Ruby"/>
      <xsd:element name="lastRenderedPageBreak" type="CT_Empty"/>
    </xsd:choice>
  </xsd:group>

  <xsd:complexType name="CT_Empty"/>
