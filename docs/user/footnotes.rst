Native footnotes
================

Create a note immediately after a run in a body paragraph or table cell::

    document = Document()
    paragraph = document.add_paragraph()
    before = paragraph.add_run("A statement")
    paragraph.add_run(" with following text.")
    note = document.add_footnote(before, "An explanation.")
    note.add_paragraph("A second paragraph.")
    note.paragraphs[0].add_run(" Important.").bold = True
    document.save("notes.docx")

The new reference occupies its own run. Inserting it does not change the text or
formatting of adjacent runs. References must be direct children of attached body
or table-cell paragraphs in the same document. Headers, footers, other notes,
comments, hyperlink runs, detached content, and text boxes are unsupported.

Each call creates a new native note. Reusing an existing note through an additional
reference is outside this API. Word supplies the visible number, placement, and
pagination according to document and section settings. This API does not calculate
page positions or change numbering settings.

``Document.footnotes`` supports iteration, ``len()``, and ``get(footnote_id)``.
Separator entries are excluded. Iteration follows part order, which can differ
from reference order. ``Run.footnote_ids`` exposes reference IDs in content order,
including dangling references. Reading the collection does not create a part.

Notes are block containers with normal paragraph, run, table, and image APIs.
Their own part owns relationships for note content. Newlines passed to
``add_footnote`` create separate paragraphs. An empty note starts with one paragraph
containing its native number marker and a space. ``Footnote.text`` includes that
space and joins paragraphs with newlines. Do not replace the first paragraph's
text or clear its marker run when editing content, since doing so removes the
native note marker. Append runs or edit the existing text runs instead.

New notes use Footnote Text and Footnote Reference styles. Existing styles are
preserved. Missing styles are created, with note paragraphs inheriting the default
paragraph style and reference numbers superscripted. Existing note content and
unrelated package content are preserved when adding notes.

Endnotes, field-based cross-references, and note deletion are outside this feature.
