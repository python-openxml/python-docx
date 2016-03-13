
Hyperlink
=========

Word allows hyperlinks to be placed in the document.

Hyperlink may link to a external location, for example, as an url. It may link to
a location within the document, for example, as a bookmark. These two cases are
handled differently.

Hyperlinks can contain multiple runs of text.

Candidate protocol
------------------

The hyperlink feature supports only external links today (03/2016).

Add a simple hyperlink with text and url:

    >>> hyperlink = paragraph.add_hyperlink(text='Google', address='https://google.com')
    >>> hyperlink
    <docx.text.hyperlink.Hyperlink at 0x7f...>
    >>> hyperlink.text
    'Google'
    >>> hyperlink.address
    'https://google.com'
    >>> hyperlink.runs
    [<docx.text.run.Run at 0x7f...>]

Add multiple runs to a hyperlink:

    >>> hyperlink = paragraph.add_hyperlink(address='https://github.com')
    >>> hyperlink.add_run('A')
    >>> hyperlink.add_run('formatted').italic = True
    >>> hyperlink.add_run('link').bold = True
    >>> hyperlink.runs
    [<docx.text.run.Run at 0x7f...>,
    <docx.text.run.Run at 0x7fb...>,
    <docx.text.run.Run at 0x7fb...>]

Retrieve a paragraph's content:

    >>> paragraph = document.add_paragraph('A plain paragraph having some ')
    >>> paragraph.add_run('link such as ')
    >>> paragraph.add_hyperlink(address='http://github.com', text='github')
    >>> paragraph.iter_p_content():
    [<docx.text.paragraph.Run at 0x7f...>,
    <docx.text.paragraph.Hyperlink at 0x7f...>]



Specimen XML
------------

.. highlight:: xml


External links
~~~~~~~~~~~~~~

An external link is specified by the attribute r:id. The location of the link
is defined in the relationships part of the document.

A simple hyperlink to an external url::

    <w:p>
      <w:r>
        <w:t xml:space="preserve">This is an external link to </w:t>
      </w:r>
      <w:hyperlink r:id="rId4">
        <w:r>
          <w:rPr>
            <w:rStyle w:val="Hyperlink"/>
          </w:rPr>
          <w:t>Google</w:t>
        </w:r>
      </w:hyperlink>
    </w:p>


The r:id="rId4" references the following relationship within the relationships
part for the document document.xml.rels.::

    <Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
      <Relationship Id="rId4" Mode="External"
      Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink"
      Target="http://google.com/"/>
    </Relationships>

A hyperlink with multiple runs of text::

    <w:p>
      <w:hyperlink r:id="rId2">
        <w:r>
          <w:rPr>
            <w:rStyle w:val="Hyperlink"/>
          </w:rPr>
          <w:t>A</w:t>
        </w:r>
        <w:r>
          <w:rPr>
            <w:rStyle w:val="Hyperlink"/>
            <w:i/>
          </w:rPr>
          <w:t xml:space="preserve"> formatted</w:t>
        </w:r>
        <w:r>
          <w:rPr>
            <w:rStyle w:val="Hyperlink"/>
            <w:b/>
          </w:rPr>
          <w:t xml:space="preserve"> link</w:t>
        </w:r>
      </w:hyperlink>
    </w:p>


Internal links
~~~~~~~~~~~~~~

An internal link, that link to a location in the document, do not have the r:id attribute
and is specified by the anchor attribute.
The value of the anchor attribute is the name of a bookmark in the document.

Example::

    <w:p>
      <w:r>
        <w:t xml:space="preserve">This is an </w:t>
      </w:r>
      <w:hyperlink w:anchor="myAnchor">
        <w:r>
          <w:rPr>
            <w:rStyle w:val="Hyperlink"/>
          </w:rPr>
          <w:t>internal link</w:t>
        </w:r>
      </w:hyperlink>
    </w:p>

    ...

    <w:p>
      <w:r>
        <w:t xml:space="preserve">This is text with a </w:t>
      </w:r>
      <w:bookmarkStart w:id="0" w:name="myAnchor"/>
        <w:r>
          <w:t>bookmark</w:t>
        </w:r>
      <w:bookmarkEnd w:id="0"/>
    </w:p>


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

    <xsd:complexType name="CT_Hyperlink">
      <xsd:group ref="EG_PContent" minOccurs="0" maxOccurs="unbounded"/>
      <xsd:attribute name="tgtFrame" type="s:ST_String" use="optional"/>
      <xsd:attribute name="tooltip" type="s:ST_String" use="optional"/>
      <xsd:attribute name="docLocation" type="s:ST_String" use="optional"/>
      <xsd:attribute name="history" type="s:ST_OnOff" use="optional"/>
      <xsd:attribute name="anchor" type="s:ST_String" use="optional"/>
      <xsd:attribute ref="r:id"/>
    </xsd:complexType>

    <xsd:group name="EG_PContent">  <!-- denormalized -->
      <xsd:choice>
        <xsd:element name="r"               type="CT_R"/>
        <xsd:element name="hyperlink"       type="CT_Hyperlink"/>
        <xsd:element name="fldSimple"       type="CT_SimpleField"/>
        <xsd:element name="sdt"             type="CT_SdtRun"/>
        <xsd:element name="customXml"       type="CT_CustomXmlRun"/>
        <xsd:element name="smartTag"        type="CT_SmartTagRun"/>
        <xsd:element name="dir"             type="CT_DirContentRun"/>
        <xsd:element name="bdo"             type="CT_BdoContentRun"/>
        <xsd:element name="subDoc"          type="CT_Rel"/>
        <xsd:group    ref="EG_RunLevelElts"/>
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

    <xsd:simpleType name="ST_RelationshipId">
      <xsd:restriction base="xsd:string"/>
    </xsd:simpleType>

