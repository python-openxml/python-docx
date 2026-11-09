
Comments
========

Word allows *comments* to be added to a document. This is an aspect of the *reviewing*
feature-set and is typically used by a second party to provide feedback to the author
without changing the document itself.

The procedure is simple:

- You select some range of text with the mouse or Shift+Arrow keys
- You press the *New Comment* button (Review toolbar)
- You type or paste in your comment

.. image:: /_static/img/comment-parts.png

**Comment Anatomy.** Each comment has two parts, the *comment-reference* and the
*comment-content*:

The *comment-refererence*, sometimes *comment-anchor*, is the text you selected before
pressing the *New Comment* button. It is a *range* in the document content delimited by
a start marker and an end marker, and containing the *id* of the comment that refers to
it.

The *comment-content* is whatever content you typed or pasted in. The content for each
comment is stored in the separate *comments-part* (part-name ``word/comments.xml``) as a
distinct comment object. Each comment has a unique id, allowing a comment reference to
be associated with its content and vice versa.

**Comment Reference.** The comment-reference is a *range*. A range must both start and
end at an even *run* boundary. Intuitively, a range corresponds to a *selection* of text
in the Word UI, one formed by dragging with the mouse or using the *Shift-Arrow* keys.

In general a range can span "run containers", such as paragraphs, such that the range
begins in one paragraph and ends in a later paragraph. However, a range must enclose
*contiguous* runs, such that a range that contains only two vertically adjacent cells in
a multi-column table is not possible (even though such a selection with the mouse is
possible).

**Comment Content.** Interestingly, although commonly used to contain a single line of
plain text, the comment-content can contain essentially any content that can appear in
the document body. This includes rich text with emphasis, runs with a different typeface
and size, both paragraph and character styles, hyperlinks, images, and tables. Note that
tables do not appear in the comment as displayed in the *comment-sidebar* although they
do apper in the *reviewing-pane*.

**Comment Metadata.** Each comment can be assigned *author*, *initals*, and *date*
metadata. In Word, these fields are assigned automatically based on values in ``Settings
> User`` of the installed Word application. These may be configured automatically in an
enterprise installation, based on the user account, but by default they are empty.

*author* metadata is required, although silently assigned the empty string by Word if
the user name is not configured. *initials* is optional, but always set by Word, to the
empty string if not configured. *date* is also optional, but always set by Word to the
date and time the comment was added (seconds resolution, UTC).

**Additional Features.** Later versions of Word allow a comment to be *resolved*. A
comment in this state will appear grayed-out in the Word UI. Later versions of Word also
allow a comment to be *replied to*, forming a *comment thread*. Neither of these
features is supported by the initial implementation of comments in *python-docx*.

The resolved-status and replies features are implemented as *extensions* and involve two
additional comment-related parts:

- `commentsExtended.xml` - contains completion (resolved) status and parent-id for
  threading comment responses; keys to `w15:paraId` of comment paragraph in
  `comments.xml`
- `commentsIds.xml` - maps `w16cid:paraId` to `w16cid:durableId`, not sure what that is
  exactly.

**Applicability.** Note that comments cannot be added to a header or footer and cannot
be nested inside a comment itself. In general the *python-docx* API will not allow these
operations but if you outsmart it then the resulting comment will either be silently
removed or trigger a repair error when the document is loaded by Word.


Word Behavior
-------------

- A DOCX package does not contain a ``comments.xml`` part by default. It is added to the
  package when the first comment is added to the document.

- A newly-created comment contains a single paragraph

- Word starts `w:id` at 0 and increments from there. It appears to use a
  `max(comment_ids) + 1` algorithm rather than aggressively filling in id numbering
  gaps.

- Word-behavior: looks like Word doesn't allow a "zero-length" comment reference; if you
  insert a comment when no text is selected, the word prior to the insertion-point is
  selected.

- Word allows a comment to be applied to a range that starts before any character and
  ends after any later character. However, the XML range-markers can only be placed
  between runs. Word accommodates this be breaking runs as necessary to start and stop
  at the desired character positions.


MS API
------

.. highlight:: python

**Document**::

    Document.Comments

**Comments**

https://learn.microsoft.com/en-us/office/vba/api/word.comments::

    Comments.Add(Range, Text) -> Comment

    # -- retrieve comment by array idx, not comment_id key --
    Comments.Item(idx: Long) -> Comment

    Comments.Count() -> Long

    # -- restrict visible comments to those by a particular reviewer
    Comments.ShowBy = "Travis McGuillicuddy"

**Comment**

https://learn.microsoft.com/en-us/office/vba/api/word.comment::

    # -- delete comment and all replies to it --
    Comment.DeleteRecursively() -> void

    # -- open OLE object embedded in comment for editing --
    Comment.Edit() -> void

    # -- get the "parent" comment when this comment is a reply --
    Comment.Ancestor() -> Comment | Nothing

    # -- author of this comment, with email and name fields --
    Comment.Contact -> CoAuthor

    Comment.Date -> Date
    Comment.Done -> bool
    Comment.IsInk -> bool

    # -- content of the comment, contrast with `Reference` below --
    Comment.Range -> Range

    # -- content within document this comment refers to --
    Comment.Reference -> Range

    Comment.Replies -> Comments

    # -- described in API docs like the same thing as `Reference` --
    Comment.Scope -> Range


Candidate Protocol
------------------

.. highlight:: python

The critical required reference for adding a comment is the *range* referred to by the
comment; i.e. the "selection" of text that is being commented on. Because this range
must start and end at an even run boundary, it is enough to specify the first and last
run in the range, where a single run can be both the start and end run::

    >>> paragraph = document.add_paragraph("Hello, world!")
    >>> document.add_comment(
    ...    runs=paragraph.runs,
    ...    text="I have this to say about that"
    ...    author="Steve Canny",
    ...    initials="SC",
    ... )
    <docx.comments.Comment object at 0x02468ACE>

A single run can be provided when that is more convenient::

    >>> paragraph = document.add_paragraph("Summary: ")
    >>> run = paragraph.add_run("{{place-summary-here}}
    >>> document.add_comment(
    ...     run, text="The AI model will replace this placeholder with a summary"
    ... )
    <docx.comments.Comment object at 0x02468ACE>

Note that `author` and `initials` are optional parameters; both default to the empty
string.

`text` is also an optional parameter and also defaults to the empty string. Omitting a
`text` argument (or passing `text=""`) produces a comment containing a single paragraph
you can immediately add runs to and add additional paragraphs after:

    >>> paragraph = document.add_paragraph("Summary: ")
    >>> run = paragraph.add_run("{{place-summary-here}}")
    >>> comment = document.add_comment(run)
    >>> paragraph = comment.paragraphs[0]
    >>> paragraph.add_run("The ")
    >>> paragraph.add_run("AI model").bold = True
    >>> paragraph.add_run(" will replace this placeholder with a ")
    >>> paragraph.add_run("summary").bold = True
    <docx.comments.Comment object at 0x02468ACE>

A method directly on |Run| may also be convenient, since you will always have the first
run of the range in hand when adding a comment but may not have ready access to the
``document`` object::

    >>> runs = find_sequence_of_one_or_more_runs_to_comment_on()
    >>> runs[0].add_comment(
    ...     last_run=runs[-1],
    ...     text="The AI model will replace this placeholder with a summary",
    ... )
    <docx.comments.Comment object at 0x02468ACE>

However, in this situation we would need to qualify the runs as being inside the
document part and not in a header or footer or comment, and perhaps other invalid
comment locations. I believe comments can be applied to footnotes and endnotes though.


Specimen XML
------------

.. highlight:: xml

``comments.xml`` (namespace declarations may vary)::

    <?xml version="1.0" encoding="UTF-8" standalone="yes"?>
    <w:comments
        xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"
        xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"
        xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"
        xmlns:p="... others omitted for brevity ...">
    >
      <w:comment w:id="0" w:author="Steve Canny" w:initials="SJC" w:date="2025-06-10T22:27:56Z">
        <w:p>
          <w:r>
            <w:rPr>
              <w:rStyle w:val="CommentReference"/>
            </w:rPr>
            <w:annotationRef/>
          </w:r>
          <w:r>
            <w:t>I have this to say about that</w:t>
          </w:r>
        </w:p>
      </w:comment>
    </w:comments>


Comment reference in document body::

    <w:p>
      <w:commentRangeStart w:id="0"/>
      <w:r>
        <w:t>Hello, world!</w:t>
      </w:r>
      <w:commentRangeEnd w:id="0"/>
      <w:r>
        <w:rPr>
          <w:rStyle w:val="CommentReference"/>
        </w:rPr>
        <w:commentReference w:id="0"/>
      </w:r>
    </w:p>


**Notes**

- `w:comment` is a *block-item* container, and can contain any content that can appear
  in a document body or table cell, including both paragraphs and tables (and whatever
  can go inside those, like images, hyperlinks, etc.

- Word places the `w:annotationRef`-containing run as the first run in the first
  paragraph of the comment. I haven't been able to detect any behavior change caused by
  leaving this out or placing it elsewhere in the comment content.

- Relationships referenced from within `w:comment` content are relationships *from the
  comments part* to the image part, hyperlink, etc.

- `w:commentRangeStart` and `w:commentRangeEnd` elements are *optional*. The
  authoritative position of the comment is the required `w:commentReference` element.
  This means the *ending* location of a comment anchor can be efficiently found using
  XPath.


Schema Excerpt
--------------

**Notes:**

- `commentRangeStart` and `commentRangeEnd` are both type `CT_MarkupRange` and both
  belong to `EG_RunLevelElts` (peers of `w:r`) which gives them their positioning in the
  document structure.

- These two markers can occur at the *block* level, at the *run* level, or at the *table
  row* or *cell* level. However Word only seems to use them as peers of `w:r`. These can
  occur as a sibling to:

  - a *paragraph* (`w:p`)
  - a *table* (`w:tbl`)
  - a *run* (`w:r`)
  - a *table row* (`w:tr`)
  - a *table cell* (`w:tc`)

.. code-block:: xml

    <!-- marker types that appear in `document.xml` to mark the referenced range -->

    <xsd:element name="commentRangeStart" type="CT_MarkupRange"/>
    <xsd:element name="commentRangeEnd" type="CT_MarkupRange"/>
    <xsd:element name="commentReference" type="CT_Markup"/>

    <xsd:complexType name="CT_MarkupRange">
      <xsd:attribute name="id" type="ST_DecimalNumber" use="required"/>
      <xsd:attribute name="displacedByCustomXml" type="ST_DisplacedByCustomXml" use="optional"/>
    </xsd:complexType>

    <xsd:simpleType name="ST_DisplacedByCustomXml">
      <xsd:restriction base="xsd:string">
        <xsd:enumeration value="next"/>
        <xsd:enumeration value="prev"/>
      </xsd:restriction>
    </xsd:simpleType>

    <xsd:complexType name="CT_Markup">
      <xsd:attribute name="id" type="ST_DecimalNumber" use="required"/>
    </xsd:complexType>

    <!-- CT_Comment (individual comment in comments.xml) consolidated -->

    <xsd:complexType name="CT_Comment">  <!-- denormalized -->
      <xsd:attribute name="id" type="ST_DecimalNumber" use="required"/>
      <xsd:attribute name="author" type="s:ST_String" use="required"/>
      <xsd:attribute name="date" type="ST_DateTime" use="optional"/>
      <xsd:attribute name="initials" type="s:ST_String" use="optional"/>

      <xsd:sequence>
        <xsd:choice minOccurs="0" maxOccurs="unbounded">
          <xsd:element name="customXml" type="CT_CustomXmlBlock"/>
          <xsd:element name="sdt" type="CT_SdtBlock"/>
          <xsd:element name="p" type="CT_P" minOccurs="0" maxOccurs="unbounded"/>
          <xsd:element name="tbl" type="CT_Tbl" minOccurs="0" maxOccurs="unbounded"/>
          <xsd:group ref="EG_RunLevelElts" minOccurs="0" maxOccurs="unbounded"/>
          <xsd:element name="altChunk" type="CT_AltChunk" minOccurs="0" maxOccurs="unbounded"/>
        </xsd:choice>
      </xsd:sequence>
    </xsd:complexType>

    <xsd:group name="EG_RunLevelElts">
      <xsd:choice>
        <xsd:element name="proofErr" minOccurs="0" type="CT_ProofErr"/>
        <xsd:element name="permStart" minOccurs="0" type="CT_PermStart"/>
        <xsd:element name="permEnd" minOccurs="0" type="CT_Perm"/>
        <xsd:group ref="EG_RangeMarkupElements" minOccurs="0" maxOccurs="unbounded"/>
        <xsd:element name="ins" type="CT_RunTrackChange" minOccurs="0"/>
        <xsd:element name="del" type="CT_RunTrackChange" minOccurs="0"/>
        <xsd:element name="moveFrom" type="CT_RunTrackChange"/>
        <xsd:element name="moveTo" type="CT_RunTrackChange"/>
        <xsd:group ref="EG_MathContent" minOccurs="0" maxOccurs="unbounded"/>
      </xsd:choice>
    </xsd:group>

    <!-- referenced types -->

    <xsd:complexType name="CT_Comment">
      <xsd:complexContent>
        <xsd:extension base="CT_TrackChange">
          <xsd:sequence>
            <xsd:group ref="EG_BlockLevelElts" minOccurs="0" maxOccurs="unbounded"/>
          </xsd:sequence>
          <xsd:attribute name="initials" type="s:ST_String" use="optional"/>
        </xsd:extension>
      </xsd:complexContent>
    </xsd:complexType>

    <xsd:complexType name="CT_TrackChange">
      <xsd:complexContent>
        <xsd:extension base="CT_Markup">
          <xsd:attribute name="author" type="s:ST_String" use="required"/>
          <xsd:attribute name="date" type="ST_DateTime" use="optional"/>
        </xsd:extension>
      </xsd:complexContent>
    </xsd:complexType>

    <xsd:complexType name="CT_Markup">
      <xsd:attribute name="id" type="ST_DecimalNumber" use="required"/>
    </xsd:complexType>

    <xsd:group name="EG_BlockLevelElts">
      <xsd:choice>
        <xsd:group ref="EG_BlockLevelChunkElts" minOccurs="0" maxOccurs="unbounded"/>
        <xsd:element name="altChunk" type="CT_AltChunk" minOccurs="0" maxOccurs="unbounded"/>
      </xsd:choice>
    </xsd:group>

    <xsd:group name="EG_BlockLevelChunkElts">
      <xsd:choice>
        <xsd:group ref="EG_ContentBlockContent" minOccurs="0" maxOccurs="unbounded"/>
      </xsd:choice>
    </xsd:group>

    <xsd:group name="EG_ContentBlockContent">
      <xsd:choice>
        <xsd:element name="customXml" type="CT_CustomXmlBlock"/>
        <xsd:element name="sdt" type="CT_SdtBlock"/>
        <xsd:element name="p" type="CT_P" minOccurs="0" maxOccurs="unbounded"/>
        <xsd:element name="tbl" type="CT_Tbl" minOccurs="0" maxOccurs="unbounded"/>
        <xsd:group ref="EG_RunLevelElts" minOccurs="0" maxOccurs="unbounded"/>
      </xsd:choice>
    </xsd:group>

    <xsd:group name="EG_RunLevelElts">
      <xsd:choice>
        <xsd:element name="proofErr" minOccurs="0" type="CT_ProofErr"/>
        <xsd:element name="permStart" minOccurs="0" type="CT_PermStart"/>
        <xsd:element name="permEnd" minOccurs="0" type="CT_Perm"/>
        <xsd:group ref="EG_RangeMarkupElements" minOccurs="0" maxOccurs="unbounded"/>
        <xsd:element name="ins" type="CT_RunTrackChange" minOccurs="0"/>
        <xsd:element name="del" type="CT_RunTrackChange" minOccurs="0"/>
        <xsd:element name="moveFrom" type="CT_RunTrackChange"/>
        <xsd:element name="moveTo" type="CT_RunTrackChange"/>
        <xsd:group ref="EG_MathContent" minOccurs="0" maxOccurs="unbounded"/>
      </xsd:choice>
    </xsd:group>
