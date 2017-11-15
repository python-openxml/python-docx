
Bookmarks
=========

WordprocessingML allows zero or more *bookmark* items to be specified at an
arbitrary location in a document.

A bookmark consists of a `w:bookmarkStart` element identified with both
a `w:id` and `w:name` attribute, and a matching `w:bookmarkEnd` element
having the same `w:id` value.

Taken as a whole (matching element pair) the bookmark has both an id and
a name. The bookmark appears in the Word UI by its name; the presence and
uniqueness of the name are both required. While used to match starts and
ends, the id value is not stable across saves in the Word UI. The bookmark
name should be used as the key value for lookups.

A bookmark delimits an arbitrary contiguous sequence of text in a document.
It's start and end can be at either the block level (between paragraphs
and/or tables) or in-between runs (between individual characters). A bookmark
can also appear in a table.

Among the applications of bookmarks in Word is their use in captions and
cross-references.


Protocol
--------

.. highlight:: python

Adding a bookmark::

    >>> bookmarks = document.bookmarks
    >>> bookmarks
    <docx.text.bookmark.Bookmarks object at 0x...>
    >>> len(bookmarks)
    0
    >>> bookmark = document.start_bookmark('Target')
    >>> bookmark.name
    'Target'
    >>> bookmark.id
    1
    >>> len(bookmarks)  # doesn't count until it's closed
    0

    >>> document.add_paragraph()  # etc. ...

    >>> document.end_bookmark(bookmark)
    >>> len(bookmarks)
    1
    >>> bookmarks.get('Target')
    docx.text.bookmark.Bookmark object at 0x00fa1afe1>
    >>> bookmarks.get(id=1)
    docx.text.bookmark.Bookmark object at 0x00fa1afe1>
    >>> bookmarks[0]
    docx.text.bookmark.Bookmark object at 0x00fa1afe1>


Word Behavior
-------------

* The Word UI enforces the uniqueness of bookmark names.

* A bookmark having the same name as a prior bookmark (in document order) is
  ignored by Word.

* An unclosed bookmark (`w:bookmarkStart` without matching `w:bookmarkEnd`)
  is ignored by Word.

* A "reversed" bookmark (`w:bookmarkEnd` appears before matching
  `w:bookmarkStart`) is ignored by Word and removed on the next save (by
  Word).

* Word will change bookmark ids (while keeping start and end consistent) at
  its convenience. A bookmark id is not a stable key across document saves
  (in Word).

* In general, referents to a bookmark use the bookmark *name* as the key.
  This makes sense as the id is not a durable key.

* A bookmark can be *hidden*, which occurs for example when cross-references
  are inserted into the document.

* ? Do bookmarks need to be unique across all stories? (like headers, footers,
  etc.)? This could be trouble for us because we don't yet have access to
  those "stories".

* ? How do overlapping bookmarks behave? Are those permitted? Like new one
  starts before prior one finishes?

  ? What about "nested" bookmarks? Are those permitted? Line second bookmark
  starts and ends after first one starts and before it ends?

* A bookmark can be added in five different document parts: Body, Header,
  Footer, Footnote and Endnote.


XML Semantics
-------------

* The `w:bookmarkStart` element can use optional `w:colFirst` and `w:colLast`
  elements to bookmark specific parts of a table. If used, both should appear.


Specimen XML
------------

.. highlight:: xml

::

  <w:p>
    <w:r>
      <w:t>Foo</w:t>
    </w:r>
    <w:bookmarkStart w:id="0" w:name="sampleBookmark" />
    <w:r>
      <w:t>bar</w:t>
    </w:r>
  </w:p>
  <w:p>
    <w:r>
      <w:t>Bar</w:t>
    </w:r>
    <w:bookmarkEnd w:id="0" />
    <w:r>
      <w:t>foo</w:t>
    </w:r>
  </w:p>


MS API Protocol
---------------

The MS API defines a `Bookmarks` object which is a collection of
`Bookmark objects`

.. _Bookmarks object:
   https://msdn.microsoft.com/en-us/vba/word-vba/articles/bookmarks-object-word

* Bookmarks.Add(name, range)
* Bookmarks.Exists(name)
* Bookmarks.Item(index)
* Bookmarks.DefaultSorting
* Bookmarks.ShowHidden

.. _Bookmark objects:
   https://msdn.microsoft.com/en-us/vba/word-vba/articles/bookmark-object-word

* Bookmark.Delete()
* Bookmark.Column (boolean)
* Bookmark.Empty (boolean, True if contains no text.)
* Bookmark.End
* Bookmark.Name
* Bookmark.Start
* Bookmark.StoryType


Schema excerpt
--------------

::

  <xsd:element name="document" type="CT_Document"/>

  <xsd:element name="endnotes" type="CT_Endnotes"/>

  <xsd:element name="footnotes" type="CT_Footnotes"/>

  <xsd:element name="ftr" type="CT_HdrFtr"/>

  <xsd:element name="hdr" type="CT_HdrFtr"/>

  <xsd:complexType name="CT_Body">
    <xsd:sequence>
      <xsd:choice minOccurs="0" maxOccurs="unbounded">
        <xsd:element name="p"                           type="CT_P"/>
        <xsd:element name="tbl"                         type="CT_Tbl"/>
        <xsd:element name="customXml"                   type="CT_CustomXmlBlock"/>
        <xsd:element name="sdt"                         type="CT_SdtBlock"/>
        <xsd:element name="proofErr"                    type="CT_ProofErr"/>
        <xsd:element name="permStart"                   type="CT_PermStart"/>
        <xsd:element name="permEnd"                     type="CT_Perm"/>
        <xsd:element name="ins"                         type="CT_RunTrackChange"/>
        <xsd:element name="del"                         type="CT_RunTrackChange"/>
        <xsd:element name="moveFrom"                    type="CT_RunTrackChange"/>
        <xsd:element name="moveTo"                      type="CT_RunTrackChange"/>
        <xsd:element  ref="m:oMathPara"                 type="CT_OMathPara"/>
        <xsd:element  ref="m:oMath"                     type="CT_OMath"/>
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
        <xsd:element name="altChunk"                    type="CT_AltChunk"/>
      </xsd:choice>
      <xsd:element name="sectPr" type="CT_SectPr" minOccurs="0" maxOccurs="1"/>
    </xsd:sequence>
  </xsd:complexType>

  <xsd:complexType name="CT_Bookmark">
    <xsd:attribute name="id"                   type="ST_DecimalNumber" use="required"/>
    <xsd:attribute name="name"                 type="s:ST_String"      use="required"/>
    <xsd:attribute name="displacedByCustomXml" type="ST_DisplacedByCustomXml"/>
    <xsd:attribute name="colFirst"             type="ST_DecimalNumber"/>
    <xsd:attribute name="colLast"              type="ST_DecimalNumber"/>
  </xsd:complexType>

  <xsd:complexType name="CT_MarkupRange">  <!-- denormalized -->
    <xsd:attribute name="id"                   type="ST_DecimalNumber" use="required"/>
    <xsd:attribute name="displacedByCustomXml" type="ST_DisplacedByCustomXml"/>
  </xsd:complexType>

  <xsd:complexType name="CT_Endnotes">
    <xsd:sequence maxOccurs="unbounded">
      <xsd:element name="endnote" type="CT_FtnEdn" minOccurs="0"/>
    </xsd:sequence>
  </xsd:complexType>

  <xsd:complexType name="CT_Footnotes">
    <xsd:sequence maxOccurs="unbounded">
      <xsd:element name="footnote" type="CT_FtnEdn" minOccurs="0"/>
    </xsd:sequence>
  </xsd:complexType>

  <xsd:complexType name="CT_HdrFtr">
    <xsd:group ref="EG_BlockLevelElts" minOccurs="1" maxOccurs="unbounded"/>
  </xsd:complexType>

  <xsd:simpleType name="ST_DecimalNumber">
    <xsd:restriction base="xsd:integer"/>
  </xsd:simpleType>

  <xsd:simpleType name="ST_DisplacedByCustomXml">
    <xsd:restriction base="xsd:string">
      <xsd:enumeration value="next"/>
      <xsd:enumeration value="prev"/>
    </xsd:restriction>
  </xsd:simpleType>
