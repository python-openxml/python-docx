Lists and numbering
===================

A paragraph style controls appearance. A list instance controls which
paragraphs share a numbering sequence. Create an instance from a paragraph
style that references numbering in your document or template::

    from docx import Document

    document = Document()
    sequence = document.add_list("List Number", start=3)
    paragraph = document.add_paragraph("Third item", "List Number")
    sequence.apply(paragraph)

    continuation = document.add_paragraph("More about the third item", "List Number")
    sequence.apply_continuation(continuation)

    document.add_paragraph("Intervening text")
    sequence.apply(document.add_paragraph("Fourth item", "List Number"))

    restarted = sequence.restart(start=1)
    restarted.apply(document.add_paragraph("First item of a new list", "List Number"))

Use ``List Bullet`` for bullets. The library never inserts visible number or
bullet text into a run. ``start=0`` is supported. Later paragraph text does
not control the sequence's numbering.

Template numbering
------------------

``Document("brand.docx").add_list("Brand Numbered")`` uses numbering inherited
by that style. The style must already reference a numbering definition.
The library creates a new concrete numbering instance and preserves the
original abstract definition. Each sequence gets a private copy with the same
bullet fonts, indentation, and tabs. This prevents Word from sharing counters
when independent sequences are interleaved.
Existing instance overrides are copied. Numbering-style links are currently
unsupported and raise ``ValueError``. This API does not author numbering
formats or recover a list handle from an existing paragraph.

``apply()`` does not set the paragraph's style. Set it separately, as shown
above. A style is not a list identity. Two calls to ``add_list()`` create
independent sequences even when both use the same style.

Nesting
-------

Use ``sequence.levels`` to inspect available zero-based levels, and
``sequence.apply(paragraph, level=1)`` to select one. Multilevel definitions
use the template's level text and nested restart rules. Returning to an
outer level continues that level's sequence. ``restart()`` creates a new
instance and can select a starting level without changing earlier items.

The built-in ``List Number 2`` and ``List Bullet 2`` styles are independent
single-level definitions with deeper indentation. Their numbering level is
still zero. For nested lists using those styles, create an independent
instance for each nested list. This also supports mixed bullets and numbers.
Do not confuse a visual nesting depth with a template's numbering level.

Continuation paragraphs
-----------------------

``apply_continuation()`` suppresses numbering and removes the first-line
indent while retaining the effective text indentation and tabs. It does not
advance the sequence. Apply the item's style and desired direct formatting
before calling it. This takes a formatting snapshot. Subsequent changes to
the numbering definition do not update the continuation paragraph.

Word has no list-item container. The caller places continuation paragraphs
next to their item. Main-document paragraphs and table-cell paragraphs are
supported. Other stories and cross-document paragraphs are rejected before
mutation. Undefined levels and invalid starting numbers are also rejected.

For a table or another block that cannot receive numbering, call
``sequence.continuation_left_indent(item_paragraph)`` to obtain the same
left indent without changing the item paragraph. For example, assign that
value to ``table.left_indent`` on a left-aligned table. The result is
``None`` when the style and numbering define no explicit left indent.
