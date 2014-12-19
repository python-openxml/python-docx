.. _WdBuiltinStyle:

``WD_BUILTIN_STYLE``
====================

alias: **WD_STYLE**

Specifies a built-in Microsoft Word style.

Example::

    from docx import Document
    from docx.enum.style import WD_STYLE

    document = Document()
    styles = document.styles
    style = styles[WD_STYLE.BODY_TEXT]

----

BLOCK_QUOTATION
    Block Text.

BODY_TEXT
    Body Text.

BODY_TEXT_2
    Body Text 2.

BODY_TEXT_3
    Body Text 3.

BODY_TEXT_FIRST_INDENT
    Body Text First Indent.

BODY_TEXT_FIRST_INDENT_2
    Body Text First Indent 2.

BODY_TEXT_INDENT
    Body Text Indent.

BODY_TEXT_INDENT_2
    Body Text Indent 2.

BODY_TEXT_INDENT_3
    Body Text Indent 3.

BOOK_TITLE
    Book Title.

CAPTION
    Caption.

CLOSING
    Closing.

COMMENT_REFERENCE
    Comment Reference.

COMMENT_TEXT
    Comment Text.

DATE
    Date.

DEFAULT_PARAGRAPH_FONT
    Default Paragraph Font.

EMPHASIS
    Emphasis.

ENDNOTE_REFERENCE
    Endnote Reference.

ENDNOTE_TEXT
    Endnote Text.

ENVELOPE_ADDRESS
    Envelope Address.

ENVELOPE_RETURN
    Envelope Return.

FOOTER
    Footer.

FOOTNOTE_REFERENCE
    Footnote Reference.

FOOTNOTE_TEXT
    Footnote Text.

HEADER
    Header.

HEADING_1
    Heading 1.

HEADING_2
    Heading 2.

HEADING_3
    Heading 3.

HEADING_4
    Heading 4.

HEADING_5
    Heading 5.

HEADING_6
    Heading 6.

HEADING_7
    Heading 7.

HEADING_8
    Heading 8.

HEADING_9
    Heading 9.

HTML_ACRONYM
    HTML Acronym.

HTML_ADDRESS
    HTML Address.

HTML_CITE
    HTML Cite.

HTML_CODE
    HTML Code.

HTML_DFN
    HTML Definition.

HTML_KBD
    HTML Keyboard.

HTML_NORMAL
    Normal (Web).

HTML_PRE
    HTML Preformatted.

HTML_SAMP
    HTML Sample.

HTML_TT
    HTML Typewriter.

HTML_VAR
    HTML Variable.

HYPERLINK
    Hyperlink.

HYPERLINK_FOLLOWED
    Followed Hyperlink.

INDEX_1
    Index 1.

INDEX_2
    Index 2.

INDEX_3
    Index 3.

INDEX_4
    Index 4.

INDEX_5
    Index 5.

INDEX_6
    Index 6.

INDEX_7
    Index 7.

INDEX_8
    Index 8.

INDEX_9
    Index 9.

INDEX_HEADING
    Index Heading

INTENSE_EMPHASIS
    Intense Emphasis.

INTENSE_QUOTE
    Intense Quote.

INTENSE_REFERENCE
    Intense Reference.

LINE_NUMBER
    Line Number.

LIST
    List.

LIST_2
    List 2.

LIST_3
    List 3.

LIST_4
    List 4.

LIST_5
    List 5.

LIST_BULLET
    List Bullet.

LIST_BULLET_2
    List Bullet 2.

LIST_BULLET_3
    List Bullet 3.

LIST_BULLET_4
    List Bullet 4.

LIST_BULLET_5
    List Bullet 5.

LIST_CONTINUE
    List Continue.

LIST_CONTINUE_2
    List Continue 2.

LIST_CONTINUE_3
    List Continue 3.

LIST_CONTINUE_4
    List Continue 4.

LIST_CONTINUE_5
    List Continue 5.

LIST_NUMBER
    List Number.

LIST_NUMBER_2
    List Number 2.

LIST_NUMBER_3
    List Number 3.

LIST_NUMBER_4
    List Number 4.

LIST_NUMBER_5
    List Number 5.

LIST_PARAGRAPH
    List Paragraph.

MACRO_TEXT
    Macro Text.

MESSAGE_HEADER
    Message Header.

NAV_PANE
    Document Map.

NORMAL
    Normal.

NORMAL_INDENT
    Normal Indent.

NORMAL_OBJECT
    Normal (applied to an object).

NORMAL_TABLE
    Normal (applied within a table).

NOTE_HEADING
    Note Heading.

PAGE_NUMBER
    Page Number.

PLAIN_TEXT
    Plain Text.

QUOTE
    Quote.

SALUTATION
    Salutation.

SIGNATURE
    Signature.

STRONG
    Strong.

SUBTITLE
    Subtitle.

SUBTLE_EMPHASIS
    Subtle Emphasis.

SUBTLE_REFERENCE
    Subtle Reference.

TABLE_COLORFUL_GRID
    Colorful Grid.

TABLE_COLORFUL_LIST
    Colorful List.

TABLE_COLORFUL_SHADING
    Colorful Shading.

TABLE_DARK_LIST
    Dark List.

TABLE_LIGHT_GRID
    Light Grid.

TABLE_LIGHT_GRID_ACCENT_1
    Light Grid Accent 1.

TABLE_LIGHT_LIST
    Light List.

TABLE_LIGHT_LIST_ACCENT_1
    Light List Accent 1.

TABLE_LIGHT_SHADING
    Light Shading.

TABLE_LIGHT_SHADING_ACCENT_1
    Light Shading Accent 1.

TABLE_MEDIUM_GRID_1
    Medium Grid 1.

TABLE_MEDIUM_GRID_2
    Medium Grid 2.

TABLE_MEDIUM_GRID_3
    Medium Grid 3.

TABLE_MEDIUM_LIST_1
    Medium List 1.

TABLE_MEDIUM_LIST_1_ACCENT_1
    Medium List 1 Accent 1.

TABLE_MEDIUM_LIST_2
    Medium List 2.

TABLE_MEDIUM_SHADING_1
    Medium Shading 1.

TABLE_MEDIUM_SHADING_1_ACCENT_1
    Medium Shading 1 Accent 1.

TABLE_MEDIUM_SHADING_2
    Medium Shading 2.

TABLE_MEDIUM_SHADING_2_ACCENT_1
    Medium Shading 2 Accent 1.

TABLE_OF_AUTHORITIES
    Table of Authorities.

TABLE_OF_FIGURES
    Table of Figures.

TITLE
    Title.

TOAHEADING
    TOA Heading.

TOC_1
    TOC 1.

TOC_2
    TOC 2.

TOC_3
    TOC 3.

TOC_4
    TOC 4.

TOC_5
    TOC 5.

TOC_6
    TOC 6.

TOC_7
    TOC 7.

TOC_8
    TOC 8.

TOC_9
    TOC 9.
