
Working with Styles
===================

This page uses concepts developed in the prior page without introduction. If
a term is unfamiliar, consult the prior page :ref:`understanding_styles` for
a definition.


Access a style
--------------

Styles are accessed using the :attr:`.Document.styles` attribute::

    >>> document = Document()
    >>> styles = document.styles
    >>> styles
    <docx.styles.styles.Styles object at 0x10a7c4f50>

The |Styles| object provides dictionary-style access to defined styles by
name::

    >>> styles['Normal']
    <docx.styles.style._ParagraphStyle object at <0x10a7c4f6b>

.. note:: Built-in styles are stored in a WordprocessingML file using their
   English name, e.g. 'Heading 1', even though users working on a localized
   version of Word will see native language names in the UI, e.g. 'Kop 1'.
   Because |docx| operates on the WordprocessingML file, style lookups must
   use the English name. A document available on this external site allows
   you to create a mapping between local language names and English style
   names:
   http://www.thedoctools.com/index.php?show=mt_create_style_name_list

   User-defined styles, also known as *custom styles*, are not localized and
   are accessed with the name exactly as it appears in the Word UI.

The |Styles| object is also iterable. By using the identification properties
on |BaseStyle|, various subsets of the defined styles can be generated. For
example, this code will produce a list of the defined paragraph styles::

   >>> from docx.enum.style import WD_STYLE_TYPE
   >>> styles = document.styles
   >>> paragraph_styles = [
   ...     s for s in styles if s.type == WD_STYLE_TYPE.PARAGRAPH
   ... ]
   >>> for style in paragraph_styles:
   ...     print(style.name)
   ...
   Normal
   Body Text
   List Bullet


Apply a style
-------------

The |Paragraph|, |Run|, and |Table| objects each have a :attr:`style`
attribute. Assigning a style object to this attribute applies that style::

    >>> document = Document()
    >>> paragraph = document.add_paragraph()
    >>> paragraph.style
    <docx.styles.style._ParagraphStyle object at <0x11a7c4c50>
    >>> paragraph.style.name
    'Normal'
    >>> paragraph.style = document.styles['Heading 1']
    >>> paragraph.style.name
    'Heading 1'

A style name can also be assigned directly, in which case |docx| will do the
lookup for you::

    >>> paragraph.style = 'List Bullet'
    >>> paragraph.style
    <docx.styles.style._ParagraphStyle object at <0x10a7c4f84>
    >>> paragraph.style.name
    'List Bullet'

A style can also be applied at creation time using either the style object or
its name::

    >>> paragraph = document.add_paragraph(style='Body Text')
    >>> paragraph.style.name
    'Body Text'
    >>> body_text_style = document.styles['Body Text']
    >>> paragraph = document.add_paragraph(style=body_text_style)
    >>> paragraph.style.name
    'Body Text'


Add or delete a style
---------------------

A new style can be added to the document by specifying a unique name and
a style type::

    >>> from docx.enum.style import WD_STYLE_TYPE
    >>> styles = document.styles
    >>> style = styles.add_style('Citation', WD_STYLE_TYPE.PARAGRAPH)
    >>> style.name
    'Citation'
    >>> style.type
    PARAGRAPH (1)

Use the :attr:`~.BaseStyle.base_style` property to specify a style the new
style should inherit formatting settings from::

    >>> style.base_style
    None
    >>> style.base_style = styles['Normal']
    >>> style.base_style
    <docx.styles.style._ParagraphStyle object at 0x10a7a9550>
    >>> style.base_style.name
    'Normal'

A style can be removed from the document simply by calling its
:meth:`~.BaseStyle.delete` method::

    >>> styles = document.styles
    >>> len(styles)
    10
    >>> styles['Citation'].delete()
    >>> len(styles)
    9

.. note:: The :meth:`.Style.delete` method removes the style's definition
   from the document. It does not affect content in the document to which
   that style is applied. Content having a style not defined in the document
   is rendered using the default style for that content object, e.g.
   'Normal' in the case of a paragraph.


Define character formatting
---------------------------

Character, paragraph, and table styles can all specify character formatting
to be applied to content with that style. All the character formatting that
can be applied directly to text can be specified in a style. Examples include
font typeface and size, bold, italic, and underline.

Each of these three style types have a :attr:`~._CharacterStyle.font`
attribute providing access to a |Font| object. A style's |Font| object
provides properties for getting and setting the character formatting for that
style.

Several examples are provided here. For a complete set of the available
properties, see the |Font| API documentation.

The font for a style can be accessed like this::

    >>> from docx import Document
    >>> document = Document()
    >>> style = document.styles['Normal']
    >>> font = style.font

Typeface and size are set like this::

    >>> from docx.shared import Pt
    >>> font.name = 'Calibri'
    >>> font.size = Pt(12)

Many font properties are *tri-state*, meaning they can take the values
|True|, |False|, and |None|. |True| means the property is "on", |False| means
it is "off". Conceptually, the |None| value means "inherit". Because a style
exists in an inheritance hierarchy, it is important to have the ability to
specify a property at the right place in the hierarchy, generally as far up
the hierarchy as possible. For example, if all headings should be in the
Arial typeface, it makes more sense to set that property on the `Heading 1`
style and have `Heading 2` inherit from `Heading 1`.

Bold and italic are tri-state properties, as are all-caps, strikethrough,
superscript, and many others. See the |Font| API documentation for a full
list::

    >>> font.bold, font.italic
    (None, None)
    >>> font.italic = True
    >>> font.italic
    True
    >>> font.italic = False
    >>> font.italic
    False
    >>> font.italic = None
    >>> font.italic
    None

Underline is a bit of a special case. It is a hybrid of a tri-state property
and an enumerated value property. |True| means single underline, by far the
most common. |False| means no underline, but more often |None| is the right
choice if no underlining is wanted since it is rare to inherit it from a base
style. The other forms of underlining, such as double or dashed, are
specified with a member of the :ref:`WdUnderline` enumeration::

    >>> font.underline
    None
    >>> font.underline = True
    >>> # or perhaps
    >>> font.underline = WD_UNDERLINE.DOT_DASH


Define paragraph formatting
---------------------------

Both a paragraph style and a table style allow paragraph formatting to be
specified. These styles provide access to a |ParagraphFormat| object via
their :attr:`~._ParagraphStyle.paragraph_format` property.

Paragraph formatting includes layout behaviors such as justification,
indentation, space before and after, page break before, and widow/orphan
control. For a complete list of the available properties, consult the API
documentation page for the |ParagraphFormat| object.

Here's an example of how you would create a paragraph style having hanging
indentation of 1/4 inch, 12 points spacing above, and widow/orphan control::

    >>> from docx.enum.style import WD_STYLE_TYPE
    >>> from docx.shared import Inches, Pt
    >>> document = Document()
    >>> style = document.styles.add_style('Indent', WD_STYLE_TYPE.PARAGRAPH)
    >>> paragraph_format = style.paragraph_format
    >>> paragraph_format.left_indent = Inches(0.25)
    >>> paragraph_format.first_line_indent = Inches(-0.25)
    >>> paragraph_format.space_before = Pt(12)
    >>> paragraph_format.widow_control = True


Use paragraph-specific style properties
---------------------------------------

A paragraph style has a :attr:`~._ParagraphStyle.next_paragraph_style`
property that specifies the style to be applied to new paragraphs inserted
after a paragraph of that style. This is most useful when the style would
normally appear only once in a sequence, such as a heading. In that case, the
paragraph style can automatically be set back to a body style after
completing the heading.

In the most common case (body paragraphs), subsequent paragraphs should
receive the same style as the current paragraph. The default handles this
case well by applying the same style if a next paragraph style is not
specified.

Here's an example of how you would change the next paragraph style of the
*Heading 1* style to *Body Text*::

    >>> from docx import Document
    >>> document = Document()
    >>> styles = document.styles

    >>> styles['Heading 1'].next_paragraph_style = styles['Body Text']

The default behavior can be restored by assigning |None| or the style itself::

    >>> heading_1_style = styles['Heading 1']
    >>> heading_1_style.next_paragraph_style.name
    'Body Text'

    >>> heading_1_style.next_paragraph_style = heading_1_style
    >>> heading_1_style.next_paragraph_style.name
    'Heading 1'

    >>> heading_1_style.next_paragraph_style = None
    >>> heading_1_style.next_paragraph_style.name
    'Heading 1'


Control how a style appears in the Word UI
------------------------------------------

The properties of a style fall into two categories, *behavioral properties*
and *formatting properties*. Its behavioral properties control when and where
the style appears in the Word UI. Its formatting properties determine the
formatting of content to which the style is applied, such as the size of the
font and its paragraph indentation.

There are five behavioral properties of a style:

* :attr:`~.BaseStyle.hidden`
* :attr:`~.BaseStyle.unhide_when_used`
* :attr:`~.BaseStyle.priority`
* :attr:`~.BaseStyle.quick_style`
* :attr:`~.BaseStyle.locked`

See the :ref:`style_behavior` section in :ref:`understanding_styles` for
a description of how these behavioral properties interact to determine when
and where a style appears in the Word UI.

The :attr:`priority` property takes an integer value. The other four style
behavior properties are *tri-state*, meaning they can take the value |True|
(on), |False| (off), or |None| (inherit).

Display a style in the style gallery
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The following code will cause the 'Body Text' paragraph style to appear first
in the style gallery::

    >>> from docx import Document
    >>> document = Document()
    >>> style = document.styles['Body Text']

    >>> style.hidden = False
    >>> style.quick_style = True
    >>> style.priorty = 1

Remove a style from the style gallery
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This code will remove the 'Normal' paragraph style from the style gallery,
but allow it to remain in the recommended list::

    >>> style = document.styles['Normal']

    >>> style.hidden = False
    >>> style.quick_style = False


Working with Latent Styles
--------------------------

See the :ref:`builtin_styles` and :ref:`latent_styles` sections in
:ref:`understanding_styles` for a description of how latent styles define the
behavioral properties of built-in styles that are not yet defined in the
`styles.xml` part of a .docx file.

Access the latent styles in a document
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The latent styles in a document are accessed from the styles object::

    >>> document = Document()
    >>> latent_styles = document.styles.latent_styles

A |LatentStyles| object supports :meth:`len`, iteration, and dictionary-style
access by style name::

    >>> len(latent_styles)
    161

    >>> latent_style_names = [ls.name for ls in latent_styles]
    >>> latent_style_names
    ['Normal', 'Heading 1', 'Heading 2', ... 'TOC Heading']

    >>> latent_quote = latent_styles['Quote']
    >>> latent_quote
    <docx.styles.latent.LatentStyle object at 0x10a7c4f50>
    >>> latent_quote.priority
    29

Change latent style defaults
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The |LatentStyles| object also provides access to the default behavioral
properties for built-in styles in the current document. These defaults
provide the value for any undefined attributes of the |_LatentStyle|
definitions and to all behavioral properties of built-in styles having no
explicit latent style definition. See the API documentation for the
|LatentStyles| object for the complete set of available properties::

    >>> latent_styles.default_to_locked
    False
    >>> latent_styles.default_to_locked = True
    >>> latent_styles.default_to_locked
    True

Add a latent style definition
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A new latent style can be added using the
:meth:`~.LatentStyles.add_latent_style` method on |LatentStyles|. This code
adds a new latent style for the builtin style 'List Bullet', setting it to
appear in the style gallery::

    >>> latent_style = latent_styles['List Bullet']
    KeyError: no latent style with name 'List Bullet'
    >>> latent_style = latent_styles.add_latent_style('List Bullet')
    >>> latent_style.hidden = False
    >>> latent_style.priority = 2
    >>> latent_style.quick_style = True

Delete a latent style definition
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A latent style definition can be deleted by calling its
:meth:`~.LatentStyle.delete` method::

    >>> latent_styles['Light Grid']
    <docx.styles.latent.LatentStyle object at 0x10a7c4f50>
    >>> latent_styles['Light Grid'].delete()
    >>> latent_styles['Light Grid']
    KeyError: no latent style with name 'Light Grid'
