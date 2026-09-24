Bookmarks
=========

Bookmarks provide named destinations without changing visible text.
Use a paragraph target for navigation to a heading::

    document = Document()
    heading = document.add_heading("Details")
    bookmark = document.bookmarks.add("Details", paragraph=heading)
    assert document.bookmarks.get("details").paragraph.text == "Details"

A paragraph target is a collapsed range at the start of the paragraph,
after its paragraph properties. It does not enclose the heading text.
Appending runs to the paragraph does not move the target.

To enclose text, supply a run or consecutive runs from one paragraph::

    paragraph = document.add_paragraph()
    first = paragraph.add_run("Important ")
    last = paragraph.add_run("details")
    last.bold = True
    document.bookmarks.add("ImportantDetails", runs=[first, last])

Creation supports body paragraphs and table cells. Cross-paragraph ranges,
runs inside hyperlinks, other stories, and detached paragraphs are rejected.
Ranges must be in document order and cannot skip runs or intervening content.
Invalid inputs do not leave partially inserted markers.

Names and lookup
----------------

The collection includes bookmarks in related Word stories and supports ``len()`` and case-insensitive ``get(name)``. ``Bookmark.name``
preserves the stored spelling. ``Bookmark.paragraph`` returns the starting
main-story paragraph or ``None`` for a marker in another story or outside a
paragraph. Order follows package parts, then document order within each part. Reading preserves
existing names, including names outside the authoring subset.

New names must contain 1-40 ASCII letters, digits, or underscores and cannot
start with a digit. This is a deliberately portable subset of Word names.
An underscore at the start creates a bookmark that Word normally hides in
its bookmark UI. Duplicate names are rejected case-insensitively. IDs and
names in related Word XML parts are reserved as well, including existing
headers, footers, and notes. The API never replaces an existing bookmark.

Word limits bookmark names to 40 characters even though the XML type allows
longer strings. See `Microsoft's implementation notes
<https://learn.microsoft.com/en-us/openspecs/office_standards/ms-oe376/88454e96-31cb-4112-b7c2-e6b0f84a2637>`_
and the `Word bookmark API
<https://learn.microsoft.com/en-us/office/vba/api/word.bookmarks.add>`_.

Rename, deletion, and arbitrary document-range editing are outside this API.
