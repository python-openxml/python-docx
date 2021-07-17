
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
    <docx.bookmark._Bookmark at 0x00fa1afe1>
    >>> bookmarks.get_by_id(1)
    <docx.bookmark._Bookmark at 0x00fa1afe1>
    >>> bookmarks[0]
    <docx.bookmark._Bookmark at 0x00fa1afe1>

    # A bookmark can be deleted:
    >>> len(bookmarks)
    >>> 2
    >>> bookmark =  bookmarks[0]
    >>> bookmark.delete()
    >>> len(bookmarks)
    >>> 1


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

* As bookmarks need to be unique over all document stories, a check should
  be done for uniqueness. (The word API replaces the bookmark by a new one
  when a duplicate bookmarkname is used to insert a new bookmark.
  The word editor removes duplicate bookmarks.)

* Bookmarks may overlap i.e. A new bookmark is started as the previous
  one is not yet ended.

* Bookmarks may be nested i.e. a bookmark may exists within the limits
  of another bookmark.

* A bookmark can be added in five different document parts: Body, Header,
  Footer, Footnote and Endnote.

* As bookmarks can be added in at different locations as well as different
  document parts, the bookmarkStart and bookmarkEnd elements should be added
  to different complex types: CT_Body, CT_P and CT_Tbl, as well as CT_HdrFtr
  and CT_FtnEdn.


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

Bookmarks object:

https://msdn.microsoft.com/en-us/vba/word-vba/articles/bookmarks-object-word

Methods:
* Bookmarks.Exists(name) - Checks if bookmark name exists in document.
* Bookmarks.Item(index) - Returns bookmark based on id or name.

Properties:
* Bookmarks.Count - Number of bookmarks

Bookmark objects:
https://msdn.microsoft.com/en-us/vba/word-vba/articles/bookmark-object-word

Methods:
* Bookmark.Delete() - Removing the two elements from the document

Properties:
* Bookmark.Column (boolean) - True if bookmark is inside a table Column
* Bookmark.Empty (boolean) - True if the specified bookmark is Empty
* Bookmark.Name - Return name of bookmark.

Schema excerpt
--------------

::

  <xsd:complexType name="CT_Body">  <!-- denormalized -->
    <xsd:sequence>
      <xsd:element name="customXml"                           type="CT_CustomXmlBlock"/>
      <xsd:element name="sdt"                                 type="CT_SdtBlock"/>
      <xsd:element name="p"                                   type="CT_P" minOccurs="0" maxOccurs="unbounded"/>
      <xsd:element name="tbl"                                 type="CT_Tbl" minOccurs="0" maxOccurs="unbounded"/>
      <xsd:element name="proofErr" minOccurs="0"              type="CT_ProofErr"/>
      <xsd:element name="permStart" minOccurs="0"             type="CT_PermStart"/>
      <xsd:element name="permEnd" minOccurs="0"               type="CT_Perm"/>
      <xsd:group ref="EG_RangeMarkupElements" minOccurs="0" maxOccurs="unbounded"/>
      <xsd:element name="ins"                                 type="CT_RunTrackChange" minOccurs="0"/>
      <xsd:element name="del"                                 type="CT_RunTrackChange" minOccurs="0"/>
      <xsd:element name="moveFrom"                            type="CT_RunTrackChange"/>
      <xsd:element name="moveTo"                              type="CT_RunTrackChange"/>
      <xsd:choice>
        <xsd:element ref="m:oMathPara"/>
        <xsd:element ref="m:oMath"/>
      </xsd:choice>
      <xsd:element name="altChunk"                            type="CT_AltChunk" minOccurs="0" maxOccurs="unbounded"/>
      <xsd:element name="sectPr" minOccurs="0" maxOccurs="1"  type="CT_SectPr"/>
    </xsd:sequence>
  </xsd:complexType>

  <xsd:complexType name="CT_P">  <!-- denormalized -->
    <xsd:sequence>
      <xsd:element name="pPr"                           type="CT_PPr" minOccurs="0"/>
      <xsd:element name="customXml"                     type="CT_CustomXmlRun"/>
      <xsd:element name="smartTag"                      type="CT_SmartTagRun"/>
      <xsd:element name="sdt"                           type="CT_SdtRun"/>
      <xsd:element name="dir"                           type="CT_DirContentRun"/>
      <xsd:element name="bdo"                           type="CT_BdoContentRun"/>
      <xsd:element name="r"                             type="CT_R"/>
      <xsd:element name="proofErr" minOccurs="0"        type="CT_ProofErr"/>
      <xsd:element name="permStart" minOccurs="0"       type="CT_PermStart"/>
      <xsd:element name="permEnd" minOccurs="0"         type="CT_Perm"/>
      <xsd:group ref="EG_RangeMarkupElements" minOccurs="0" maxOccurs="unbounded"/>
      <xsd:element name="ins"                           type="CT_RunTrackChange" minOccurs="0"/>
      <xsd:element name="del"                           type="CT_RunTrackChange" minOccurs="0"/>
      <xsd:element name="moveFrom"                      type="CT_RunTrackChange"/>
      <xsd:element name="moveTo"                        type="CT_RunTrackChange"/>
      <xsd:choice>
        <xsd:element ref="m:oMathPara"/>
        <xsd:element ref="m:oMath"/>
      </xsd:choice>
      <xsd:element name="fldSimple"                     type="CT_SimpleField" minOccurs="0" maxOccurs="unbounded"/>
      <xsd:element name="hyperlink"                     type="CT_Hyperlink"/>
      <xsd:element name="subDoc"                        type="CT_Rel"/>
    </xsd:sequence>
    <xsd:attribute name="rsidRPr"                       type="ST_LongHexNumber"/>
    <xsd:attribute name="rsidR"                         type="ST_LongHexNumber"/>
    <xsd:attribute name="rsidDel"                       type="ST_LongHexNumber"/>
    <xsd:attribute name="rsidP"                         type="ST_LongHexNumber"/>
    <xsd:attribute name="rsidRDefault"                  type="ST_LongHexNumber"/>
  </xsd:complexType>

   <xsd:complexType name="CT_Tbl"> <!-- denormalized -->
    <xsd:sequence>
      <xsd:group ref="EG_RangeMarkupElements" minOccurs="0" maxOccurs="unbounded"/>
      <xsd:element name="tblPr"                         type="CT_TblPr"/>
      <xsd:element name="tblGrid"                       type="CT_TblGrid"/>
      <xsd:group ref="EG_ContentRowContent" minOccurs="0" maxOccurs="unbounded"/>
    </xsd:sequence>
  </xsd:complexType>

  <xsd:complexType name="CT_HdrFtr"> <!-- denormalized -->
    <xsd:element name="customXml"                       type="CT_CustomXmlBlock"/>
    <xsd:element name="sdt"                             type="CT_SdtBlock"/>
    <xsd:element name="p"                               type="CT_P" minOccurs="0" maxOccurs="unbounded"/>
    <xsd:element name="tbl"                             type="CT_Tbl" minOccurs="0" maxOccurs="unbounded"/>
    <xsd:element name="proofErr" minOccurs="0"          type="CT_ProofErr"/>
    <xsd:element name="permStart" minOccurs="0"         type="CT_PermStart"/>
    <xsd:element name="permEnd" minOccurs="0"           type="CT_Perm"/>
    <xsd:group ref="EG_RangeMarkupElements" minOccurs="0" maxOccurs="unbounded"/>
    <xsd:element name="ins"                             type="CT_RunTrackChange" minOccurs="0"/>
    <xsd:element name="del"                             type="CT_RunTrackChange" minOccurs="0"/>
    <xsd:element name="moveFrom"                        type="CT_RunTrackChange"/>
    <xsd:element name="moveTo"                          type="CT_RunTrackChange"/>
    <xsd:choice>
      <xsd:element ref="m:oMathPara"/>
      <xsd:element ref="m:oMath"/>
    </xsd:choice>
    <xsd:element name="altChunk"                        type="CT_AltChunk" minOccurs="0" maxOccurs="unbounded"/>
  </xsd:complexType>

  <xsd:complexType name="CT_FtnEdn"> <!-- denormalized -->
    <xsd:sequence>
      <xsd:element name="customXml"               type="CT_CustomXmlBlock"/>
      <xsd:element name="sdt"                     type="CT_SdtBlock"/>
      <xsd:element name="p"                       type="CT_P" minOccurs="0" maxOccurs="unbounded"/>
      <xsd:element name="tbl"                     type="CT_Tbl" minOccurs="0" maxOccurs="unbounded"/>
      <xsd:element name="proofErr" minOccurs="0"  type="CT_ProofErr"/>
      <xsd:element name="permStart" minOccurs="0" type="CT_PermStart"/>
      <xsd:element name="permEnd" minOccurs="0"   type="CT_Perm"/>
      <xsd:group ref="EG_RangeMarkupElements" minOccurs="0" maxOccurs="unbounded"/>
      <xsd:element name="ins"                     type="CT_RunTrackChange" minOccurs="0"/>
      <xsd:element name="del"                     type="CT_RunTrackChange" minOccurs="0"/>
      <xsd:element name="moveFrom"                type="CT_RunTrackChange"/>
      <xsd:element name="moveTo"                  type="CT_RunTrackChange"/>
      <xsd:choice>
        <xsd:element ref="m:oMathPara"/>
        <xsd:element ref="m:oMath"/>
      </xsd:choice>
      <xsd:element name="altChunk"                type="CT_AltChunk" minOccurs="0" maxOccurs="unbounded"/>
    </xsd:sequence>
    <xsd:attribute name="type"                    type="ST_FtnEdn" use="optional"/>
    <xsd:attribute name="id"                      type="ST_DecimalNumber" use="required"/>
  </xsd:complexType>

  <xsd:group name="EG_RangeMarkupElements">
    <xsd:choice>
      <xsd:element name="bookmarkStart"                 type="CT_Bookmark"/>
      <xsd:element name="bookmarkEnd"                   type="CT_MarkupRange"/>
      <xsd:element name="moveFromRangeStart"            type="CT_MoveBookmark"/>
      <xsd:element name="moveFromRangeEnd"              type="CT_MarkupRange"/>
      <xsd:element name="moveToRangeStart"              type="CT_MoveBookmark"/>
      <xsd:element name="moveToRangeEnd"                type="CT_MarkupRange"/>
      <xsd:element name="commentRangeStart"             type="CT_MarkupRange"/>
      <xsd:element name="commentRangeEnd"               type="CT_MarkupRange"/>
      <xsd:element name="customXmlInsRangeStart"        type="CT_TrackChange"/>
      <xsd:element name="customXmlInsRangeEnd"          type="CT_Markup"/>
      <xsd:element name="customXmlDelRangeStart"        type="CT_TrackChange"/>
      <xsd:element name="customXmlDelRangeEnd"          type="CT_Markup"/>
      <xsd:element name="customXmlMoveFromRangeStart"   type="CT_TrackChange"/>
      <xsd:element name="customXmlMoveFromRangeEnd"     type="CT_Markup"/>
      <xsd:element name="customXmlMoveToRangeStart"     type="CT_TrackChange"/>
      <xsd:element name="customXmlMoveToRangeEnd"       type="CT_Markup"/>
    </xsd:choice>
  </xsd:group>

  <xsd:complexType name="CT_Bookmark">  <!-- denormalized -->
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
