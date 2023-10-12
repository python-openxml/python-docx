
Hyperlink
=========

Word allows a hyperlink to be placed in a document wherever a paragraph can appear. The
actual hyperlink element is a peer of |Run|.

The link may be to an external resource such as a web site, or internal, to another
location in the document. The link may also be a `mailto:` URI or a reference to a file
on an accessible local or network filesystem.

The visible text of a hyperlink is held in one or more runs. Technically a hyperlink can
have zero runs, but this occurs only in contrived cases (otherwise there would be
nothing to click on). As usual, each run can have its own distinct text formatting
(font), so for example one word in the hyperlink can be bold, etc. By default, Word
applies the built-in `Hyperlink` character style to a newly inserted hyperlink. Like
other text, the hyperlink text may often be broken into multiple runs as a result of
edits in different "revision-save" editing sessions (between "Save" commands).

Note that rendered page-breaks can occur in the middle of a hyperlink.

A |Hyperlink| is a child of |Paragraph|, a peer of |Run|.


TODO: What about URL-encoding/decoding (like %20) behaviors, if any?


Candidate protocol
------------------

An external hyperlink has an address and an optional anchor. An internal hyperlink has
only an anchor. An anchor is more precisely known as a *URI fragment* in a web URL and
follows a hash mark ("#"). The fragment-separator hash character is not stored in the
XML.

Note that the anchor and address are stored in two distinct attributes, so you need to
concatenate `.address` and `.anchor` like `f"{address}#{anchor}"` if you want the whole
thing.

Also note that Word does not rigorously separate a fragment in a web URI so it may
appear as part of the address or separately in the anchor attribute, depending on how
the hyperlink was authored. Hyperlinks inserted using the dialog-box seem to separate it
and addresses typed into the document directly don't, based on my limited experience.

.. highlight:: python

**Access hyperlinks in a paragraph**::

    >>> hyperlinks = paragraph.hyperlinks
    [<docx.text.hyperlink.Hyperlink at 0x7f...>]

**Access hyperlinks in a paragraph in document order with runs**::

    >>> list(paragraph.iter_inner_content())
    [
      <docx.text.run.Run at 0x7f...>
      <docx.text.hyperlink.Hyperlink at 0x7f...>
      <docx.text.run.Run at 0x7f...>
    ]

**Access hyperlink address**::

    >>> hyperlink.address
    'https://google.com/'

**Access hyperlink fragment**::

    >>> hyperlink.fragment
    'introduction'

**Access hyperlink history (visited or not, True means not visited yet)**::

    >>> hyperlink.history
    True

**Access hyperlinks runs**::

    >>> hyperlink.runs
    [
      <docx.text.run.Run at 0x7f...>
      <docx.text.run.Run at 0x7f...>
      <docx.text.run.Run at 0x7f...>
    ]

**Access hyperlink URL**::

    >>> hyperlink.url
    'https://us.com#introduction'

**Determine whether a hyperlink contains a rendered page-break**::

    >>> hyperlink.contains_page_break
    False

**Access visible text of a hyperlink**::

    >>> hyperlink.text
    'an excellent Wikipedia article on ferrets'

**Add an external hyperlink** (not yet implemented)::

    >>> hyperlink = paragraph.add_hyperlink(
    ...   'About', address='http://us.com', fragment='about'
    ... )
    >>> hyperlink
    <docx.text.hyperlink.Hyperlink at 0x7f...>
    >>> hyperlink.text
    'About'
    >>> hyperlink.address
    'http://us.com'
    >>> hyperlink.fragment
    'about'
    >>> hyperlink.url
    'http://us.com#about'

**Add an internal hyperlink (to a bookmark)**::

    >>> hyperlink = paragraph.add_hyperlink('Section 1', fragment='Section_1')
    >>> hyperlink.text
    'Section 1'
    >>> hyperlink.fragment
    'Section_1'
    >>> hyperlink.address
    ''

**Modify hyperlink properties**::

    >>> hyperlink.text = 'Froogle'
    >>> hyperlink.text
    'Froogle'
    >>> hyperlink.address = 'mailto:info@froogle.com?subject=sup dawg?'
    >>> hyperlink.address
    'mailto:info@froogle.com?subject=sup%20dawg%3F'
    >>> hyperlink.anchor = None
    >>> hyperlink.anchor
    None

**Add additional runs to a hyperlink**::

    >>> hyperlink.text = 'A '
    >>> # .insert_run inserts a new run at idx, defaults to idx=-1
    >>> hyperlink.insert_run(' link').bold = True
    >>> hyperlink.insert_run('formatted', idx=1).bold = True
    >>> hyperlink.text
    'A formatted link'
    >>> [r for r in hyperlink.iter_runs()]
    [<docx.text.run.Run at 0x7fa...>,
     <docx.text.run.Run at 0x7fb...>,
     <docx.text.run.Run at 0x7fc...>]

**Iterate over the run-level items a paragraph contains**::

    >>> paragraph = document.add_paragraph('A paragraph having a link to: ')
    >>> paragraph.add_hyperlink(text='github', address='http://github.com')
    >>> [item for item in paragraph.iter_run_level_items()]:
    [<docx.text.paragraph.Run at 0x7fd...>, <docx.text.paragraph.Hyperlink at 0x7fe...>]

**Paragraph.text now includes text contained in a hyperlink**::

    >>> paragraph.text
    'A paragraph having a link to: github'


Word Behaviors
--------------

* What are the semantics of the w:history attribute on w:hyperlink? I'm
  suspecting this indicates whether the link should show up blue (unvisited)
  or purple (visited). I'm inclined to think we need that as a read/write
  property on hyperlink. We should see what the MS API does on this count.

* We probably need to enforce some character-set restrictions on w:anchor.
  Word doesn't seem to like spaces or hyphens, for example. The simple type
  ST_String doesn't look like it takes care of this.

* We'll need to test URL escaping of special characters like spaces and
  question marks in Hyperlink.address.

* What does Word do when loading a document containing an internal hyperlink
  having an anchor value that doesn't match an existing bookmark? We'll want
  to know because we're sure to get support inquiries from folks who don't
  match those up and wonder why they get a repair error or whatever.


Specimen XML
------------

.. highlight:: xml


External links
~~~~~~~~~~~~~~

The address (URL) of an external hyperlink is stored in the document.xml.rels
file, keyed by the w:hyperlink@r:id attribute::

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

... mapping to relationship in document.xml.rels::

    <Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
      <Relationship Id="rId4" Mode="External" Type="http://..." Target="http://google.com/"/>
    </Relationships>

A hyperlink can contain multiple runs of text (and a whole lot of other stuff, at least
as far as the schema indicates)::

    <w:p>
      <w:hyperlink r:id="rId2">
        <w:r>
          <w:rPr>
            <w:rStyle w:val="Hyperlink"/>
          </w:rPr>
          <w:t xml:space="preserve">A hyperlink containing an </w:t>
        </w:r>
        <w:r>
          <w:rPr>
            <w:rStyle w:val="Hyperlink"/>
            <w:i/>
          </w:rPr>
          <w:t>italicized</w:t>
        </w:r>
        <w:r>
          <w:rPr>
            <w:rStyle w:val="Hyperlink"/>
          </w:rPr>
          <w:t xml:space="preserve"> word</w:t>
        </w:r>
      </w:hyperlink>
    </w:p>


Internal links
~~~~~~~~~~~~~~

An internal link provides "jump to another document location" behavior in the
Word UI. An internal link is distinguished by the absence of an r:id
attribute. In this case, the w:anchor attribute is required. The value of the
anchor attribute is the name of a bookmark in the document.

Example::

    <w:p>
      <w:r>
        <w:t xml:space="preserve">See </w:t>
      </w:r>
      <w:hyperlink w:anchor="Section_4">
        <w:r>
          <w:rPr>
            <w:rStyle w:val="Hyperlink"/>
          </w:rPr>
          <w:t>Section 4</w:t>
        </w:r>
      </w:hyperlink>
      <w:r>
        <w:t xml:space="preserve"> for more details.</w:t>
      </w:r>
    </w:p>

... referring to this bookmark elsewhere in the document::

    <w:p>
      <w:bookmarkStart w:id="0" w:name="Section_4"/>
        <w:r>
          <w:t>Section 4</w:t>
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

  <xsd:group name="EG_PContent">  <!-- denormalized -->
    <xsd:choice>
      <xsd:element name="r"         type="CT_R"/>
      <xsd:element name="hyperlink" type="CT_Hyperlink"/>
      <xsd:element name="fldSimple" type="CT_SimpleField"/>
      <xsd:element name="sdt"       type="CT_SdtRun"/>
      <xsd:element name="customXml" type="CT_CustomXmlRun"/>
      <xsd:element name="smartTag"  type="CT_SmartTagRun"/>
      <xsd:element name="dir"       type="CT_DirContentRun"/>
      <xsd:element name="bdo"       type="CT_BdoContentRun"/>
      <xsd:element name="subDoc"    type="CT_Rel"/>
      <xsd:group ref="EG_RunLevelElts"/>
    </xsd:choice>
  </xsd:group>

  <xsd:complexType name="CT_Hyperlink">
    <xsd:group ref="EG_PContent" minOccurs="0" maxOccurs="unbounded"/>
    <xsd:attribute name="tgtFrame"    type="s:ST_String"/>
    <xsd:attribute name="tooltip"     type="s:ST_String"/>
    <xsd:attribute name="docLocation" type="s:ST_String"/>
    <xsd:attribute name="history"     type="s:ST_OnOff"/>
    <xsd:attribute name="anchor"      type="s:ST_String"/>
    <xsd:attribute ref="r:id"/>
  </xsd:complexType>

  <xsd:group name="EG_RunLevelElts">
    <xsd:choice>
      <xsd:element name="proofErr"                    type="CT_ProofErr"/>
      <xsd:element name="permStart"                   type="CT_PermStart"/>
      <xsd:element name="permEnd"                     type="CT_Perm"/>
      <xsd:element name="bookmarkStart"               type="CT_Bookmark"/>
      <xsd:element name="bookmarkEnd"                 type="CT_MarkupRange"/>
      <xsd:element name="moveFromRangeStart"          type="CT_MoveBookmark"/>
      <xsd:element name="moveFromRangeEnd"            type="CT_MarkupRange"/>
      <xsd:element name="moveToRangeStart"            type="CT_MoveBookmark"/>
      <xsd:element name="moveToRangeEnd"              type="CT_MarkupRange"/>
      <xsd:element name="commentRangeStart"           type="CT_MarkupRange"/>
      <xsd:element name="commentRangeEnd"             type="CT_MarkupRange"/>
      <xsd:element name="customXmlInsRangeStart"      type="CT_TrackChange"/>
      <xsd:element name="customXmlInsRangeEnd"        type="CT_Markup"/>
      <xsd:element name="customXmlDelRangeStart"      type="CT_TrackChange"/>
      <xsd:element name="customXmlDelRangeEnd"        type="CT_Markup"/>
      <xsd:element name="customXmlMoveFromRangeStart" type="CT_TrackChange"/>
      <xsd:element name="customXmlMoveFromRangeEnd"   type="CT_Markup"/>
      <xsd:element name="customXmlMoveToRangeStart"   type="CT_TrackChange"/>
      <xsd:element name="customXmlMoveToRangeEnd"     type="CT_Markup"/>
      <xsd:element name="ins"                         type="CT_RunTrackChange"/>
      <xsd:element name="del"                         type="CT_RunTrackChange"/>
      <xsd:element name="moveFrom"                    type="CT_RunTrackChange"/>
      <xsd:element name="moveTo"                      type="CT_RunTrackChange"/>
      <xsd:group ref="EG_MathContent" minOccurs="0" maxOccurs="unbounded"/>
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

  <xsd:simpleType name="ST_OnOff">
    <xsd:union memberTypes="xsd:boolean ST_OnOff1"/>
  </xsd:simpleType>

  <xsd:simpleType name="ST_OnOff1">
    <xsd:restriction base="xsd:string">
      <xsd:enumeration value="on"/>
      <xsd:enumeration value="off"/>
    </xsd:restriction>
  </xsd:simpleType>

  <xsd:simpleType name="ST_RelationshipId">
    <xsd:restriction base="xsd:string"/>
  </xsd:simpleType>

  <xsd:simpleType name="ST_String">
    <xsd:restriction base="xsd:string"/>
  </xsd:simpleType>
