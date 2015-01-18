
Working with Text
=================

To work effectively with text, it's important to first understand a little
about block-level elements like paragraphs and inline-level objects like
runs.


Block-level vs. inline text objects
-----------------------------------

The paragraph is the primary block-level object in Word.

A block-level item flows the text it contains between its left and right
edges, adding an additional line each time the text extends beyond its right
boundary. For a paragraph, the boundaries are generally the page margins, but
they can also be column boundaries if the page is laid out in columns, or
cell boundaries if the paragraph occurs inside a table cell.

A table is also a block-level object.

An inline object is a portion of the content that occurs inside a block-level
item. An example would be a word that appears in bold or a sentence in
all-caps. The most common inline object is a *run*. All content within
a block container is inside of an inline object. Typically, a paragraph
contains one or more runs, each of which contain some part of the paragraph's
text.

The attributes of a block-level item specify its placement on the page, such
items as indentation and space before and after a paragraph. The attributes
of an inline item generally specify the font in which the content appears,
things like typeface, font size, bold, and italic.


Paragraph properties
--------------------

A paragraph has a variety of properties that specify its placement within its
container (typically a page) and the way it divides its content into separate
lines.

In general, it's best to define a *paragraph style* collecting these
attributes into a meaningful group and apply the appropriate style to each
paragraph, rather than repeatedly apply those properties directly to each
paragraph. This is analogous to how Cascading Style Sheets (CSS) work with
HTML. All the paragraph properties described here can be set using a style as
well as applied directly to a paragraph.

The formatting properties of a paragraph are accessed using the
|ParagraphFormat| object available using the paragraph's
:attr:`~.Paragraph.paragraph_format` property.


Horizontal alignment (justification)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Also known as *justification*, the horizontal alignment of a paragraph can be
set to left, centered, right, or fully justified (aligned on both the left
and right sides) using values from the enumeration
:ref:`WdParagraphAlignment`::

    >>> from docx.enum.text import WD_ALIGN_PARAGRAPH
    >>> document = Document()
    >>> paragraph = document.add_paragraph()
    >>> paragraph_format = paragraph.paragraph_format

    >>> paragraph_format.alignment
    None  # indicating alignment is inherited from the style hierarchy
    >>> paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    >>> paragraph_format.alignment
    CENTER (1)


Indentation
~~~~~~~~~~~

Indentation is the horizontal space between a paragraph and edge of its
container, typically the page margin. A paragraph can be indented separately
on the left and right side. The first line can also have a different
indentation than the rest of the paragraph. A first line indented further
than the rest of the paragraph has *first line indent*. A first line indented
less has a *hanging indent*.

Indentation is specified using a |Length| value, such as |Inches|, |Pt|, or
|Cm|. Negative values are valid and cause the paragraph to overlap the margin
by the specified amount. A value of |None| indicates the indentation value is
inherited from the style hierarchy. Assigning |None| to an indentation
property removes any directly-applied indentation setting and restores
inheritance from the style hierarchy::

    >>> from docx.shared import Inches
    >>> paragraph = document.add_paragraph()
    >>> paragraph_format = paragraph.paragraph_format

    >>> paragraph.left_indent
    None  # indicating indentation is inherited from the style hierarchy
    >>> paragraph.left_indent = Inches(0.5)
    >>> paragraph.left_indent
    457200
    >>> paragraph.left_indent.inches
    0.5


Right-side indent works in a similar way::

    >>> from docx.shared import Pt
    >>> paragraph.right_indent
    None
    >>> paragraph.right_indent = Pt(24)
    >>> paragraph.right_indent
    304800
    >>> paragraph.right_indent.pt
    24.0


First-line indent is specified using the
:attr:`~.ParagraphFormat.first_line_indent` property and is interpreted
relative to the left indent. A negative value indicates a hanging indent::

    >>> paragraph.first_line_indent
    None
    >>> paragraph.first_line_indent = Inches(-0.25)
    >>> paragraph.first_line_indent
    -228600
    >>> paragraph.first_line_indent.inches
    -0.25


Paragraph spacing
~~~~~~~~~~~~~~~~~

The :attr:`~.ParagraphFormat.space_before` and
:attr:`~.ParagraphFormat.space_after` properties control the spacing between
subsequent paragraphs, controlling the spacing before and after a paragraph,
respectively. Inter-paragraph spacing is *collapsed* during page layout,
meaning the spacing between two paragraphs is the maximum of the
`space_after` for the first paragraph and the `space_before` of the second
paragraph. Paragraph spacing is specified as a |Length| value, often using
|Pt|::

    >>> paragraph_format.space_before, paragraph_format.space_after
    (None, None)  # inherited by default

    >>> paragraph_format.space_before = Pt(18)
    >>> paragraph_format.space_before.pt
    18.0

    >>> paragraph_format.space_after = Pt(12)
    >>> paragraph_format.space_after.pt
    12.0


Line spacing
~~~~~~~~~~~~

Line spacing is the distance between subsequent baselines in the lines of
a paragraph. Line spacing can be specified either as an absolute distance or
relative to the line height (essentially the point size of the font used).
A typical absolute measure would be 18 points. A typical relative measure
would be double-spaced (2.0 line heights). The default line spacing is
single-spaced (1.0 line heights).

Line spacing is controlled by the interaction of the
:attr:`~.ParagraphFormat.line_spacing` and
:attr:`~.ParagraphFormat.line_spacing_rule` properties.
:attr:`~.ParagraphFormat.line_spacing` is either a |Length| value,
a (small-ish) |float|, or None. A |Length| value indicates an absolute
distance. A |float| indicates a number of line heights. |None| indicates line
spacing is inherited. :attr:`~.ParagraphFormat.line_spacing_rule` is a member
of the :ref:`WdLineSpacing` enumeration or |None|::

    >>> from docx.shared import Length
    >>> paragraph_format.line_spacing
    None
    >>> paragraph_format.line_spacing_rule
    None

    >>> paragraph_format.line_spacing = Pt(18)
    >>> isinstance(Length, paragraph_format.line_spacing)
    True
    >>> paragraph_format.line_spacing.pt
    18.0
    >>> paragraph_format.line_spacing_rule
    EXACTLY (4)

    >>> paragraph_format.line_spacing = 1.75
    >>> paragraph_format.line_spacing
    1.75
    >>> paragraph_format.line_spacing_rule
    MULTIPLE (5)


Pagination properties
~~~~~~~~~~~~~~~~~~~~~

Four paragraph properties, :attr:`~.ParagraphFormat.keep_together`,
:attr:`~.ParagraphFormat.keep_with_next`,
:attr:`~.ParagraphFormat.page_break_before`, and
:attr:`~.ParagraphFormat.widow_control` control aspects of how the paragraph
behaves near page boundaries.

:attr:`~.ParagraphFormat.keep_together` causes the entire paragraph to appear
on the same page, issuing a page break before the paragraph if it would
otherwise be broken across two pages.

:attr:`~.ParagraphFormat.keep_with_next` keeps a paragraph on the same page
as the subsequent paragraph. This can be used, for example, to keep a section
heading on the same page as the first paragraph of the section.

:attr:`~.ParagraphFormat.page_break_before` causes a paragraph to be placed
at the top of a new page. This could be used on a chapter heading to ensure
chapters start on a new page.

:attr:`~.ParagraphFormat.widow_control` breaks a page to avoid placing the
first or last line of the paragraph on a separate page from the rest of the
paragraph.

All four of these properties are *tri-state*, meaning they can take the value
|True|, |False|, or |None|. |None| indicates the property value is inherited
from the style hierarchy. |True| means "on" and |False| means "off"::

    >>> paragraph_format.keep_together
    None  # all four inherit by default
    >>> paragraph_format.keep_with_next = True
    >>> paragraph_format.keep_with_next
    True
    >>> paragraph_format.page_break_before = False
    >>> paragraph_format.page_break_before
    False
