# encoding: utf-8

"""
Enumerations related to styles
"""

from __future__ import absolute_import, print_function, unicode_literals

from .base import alias, EnumMember, XmlEnumeration, XmlMappedEnumMember


@alias('WD_STYLE')
class WD_BUILTIN_STYLE(XmlEnumeration):
    """
    alias: **WD_STYLE**

    Specifies a built-in Microsoft Word style.

    Example::

        from docx import Document
        from docx.enum.style import WD_STYLE

        document = Document()
        styles = document.styles
        style = styles[WD_STYLE.BODY_TEXT]
    """

    __ms_name__ = 'WdBuiltinStyle'

    __url__ = 'http://msdn.microsoft.com/en-us/library/office/ff835210.aspx'

    __members__ = (
        EnumMember(
            'BLOCK_QUOTATION', -85, 'Block Text.'
        ),
        EnumMember(
            'BODY_TEXT', -67, 'Body Text.'
        ),
        EnumMember(
            'BODY_TEXT_2', -81, 'Body Text 2.'
        ),
        EnumMember(
            'BODY_TEXT_3', -82, 'Body Text 3.'
        ),
        EnumMember(
            'BODY_TEXT_FIRST_INDENT', -78, 'Body Text First Indent.'
        ),
        EnumMember(
            'BODY_TEXT_FIRST_INDENT_2', -79, 'Body Text First Indent 2.'
        ),
        EnumMember(
            'BODY_TEXT_INDENT', -68, 'Body Text Indent.'
        ),
        EnumMember(
            'BODY_TEXT_INDENT_2', -83, 'Body Text Indent 2.'
        ),
        EnumMember(
            'BODY_TEXT_INDENT_3', -84, 'Body Text Indent 3.'
        ),
        EnumMember(
            'BOOK_TITLE', -265, 'Book Title.'
        ),
        EnumMember(
            'CAPTION', -35, 'Caption.'
        ),
        EnumMember(
            'CLOSING', -64, 'Closing.'
        ),
        EnumMember(
            'COMMENT_REFERENCE', -40, 'Comment Reference.'
        ),
        EnumMember(
            'COMMENT_TEXT', -31, 'Comment Text.'
        ),
        EnumMember(
            'DATE', -77, 'Date.'
        ),
        EnumMember(
            'DEFAULT_PARAGRAPH_FONT', -66, 'Default Paragraph Font.'
        ),
        EnumMember(
            'EMPHASIS', -89, 'Emphasis.'
        ),
        EnumMember(
            'ENDNOTE_REFERENCE', -43, 'Endnote Reference.'
        ),
        EnumMember(
            'ENDNOTE_TEXT', -44, 'Endnote Text.'
        ),
        EnumMember(
            'ENVELOPE_ADDRESS', -37, 'Envelope Address.'
        ),
        EnumMember(
            'ENVELOPE_RETURN', -38, 'Envelope Return.'
        ),
        EnumMember(
            'FOOTER', -33, 'Footer.'
        ),
        EnumMember(
            'FOOTNOTE_REFERENCE', -39, 'Footnote Reference.'
        ),
        EnumMember(
            'FOOTNOTE_TEXT', -30, 'Footnote Text.'
        ),
        EnumMember(
            'HEADER', -32, 'Header.'
        ),
        EnumMember(
            'HEADING_1', -2, 'Heading 1.'
        ),
        EnumMember(
            'HEADING_2', -3, 'Heading 2.'
        ),
        EnumMember(
            'HEADING_3', -4, 'Heading 3.'
        ),
        EnumMember(
            'HEADING_4', -5, 'Heading 4.'
        ),
        EnumMember(
            'HEADING_5', -6, 'Heading 5.'
        ),
        EnumMember(
            'HEADING_6', -7, 'Heading 6.'
        ),
        EnumMember(
            'HEADING_7', -8, 'Heading 7.'
        ),
        EnumMember(
            'HEADING_8', -9, 'Heading 8.'
        ),
        EnumMember(
            'HEADING_9', -10, 'Heading 9.'
        ),
        EnumMember(
            'HTML_ACRONYM', -96, 'HTML Acronym.'
        ),
        EnumMember(
            'HTML_ADDRESS', -97, 'HTML Address.'
        ),
        EnumMember(
            'HTML_CITE', -98, 'HTML Cite.'
        ),
        EnumMember(
            'HTML_CODE', -99, 'HTML Code.'
        ),
        EnumMember(
            'HTML_DFN', -100, 'HTML Definition.'
        ),
        EnumMember(
            'HTML_KBD', -101, 'HTML Keyboard.'
        ),
        EnumMember(
            'HTML_NORMAL', -95, 'Normal (Web).'
        ),
        EnumMember(
            'HTML_PRE', -102, 'HTML Preformatted.'
        ),
        EnumMember(
            'HTML_SAMP', -103, 'HTML Sample.'
        ),
        EnumMember(
            'HTML_TT', -104, 'HTML Typewriter.'
        ),
        EnumMember(
            'HTML_VAR', -105, 'HTML Variable.'
        ),
        EnumMember(
            'HYPERLINK', -86, 'Hyperlink.'
        ),
        EnumMember(
            'HYPERLINK_FOLLOWED', -87, 'Followed Hyperlink.'
        ),
        EnumMember(
            'INDEX_1', -11, 'Index 1.'
        ),
        EnumMember(
            'INDEX_2', -12, 'Index 2.'
        ),
        EnumMember(
            'INDEX_3', -13, 'Index 3.'
        ),
        EnumMember(
            'INDEX_4', -14, 'Index 4.'
        ),
        EnumMember(
            'INDEX_5', -15, 'Index 5.'
        ),
        EnumMember(
            'INDEX_6', -16, 'Index 6.'
        ),
        EnumMember(
            'INDEX_7', -17, 'Index 7.'
        ),
        EnumMember(
            'INDEX_8', -18, 'Index 8.'
        ),
        EnumMember(
            'INDEX_9', -19, 'Index 9.'
        ),
        EnumMember(
            'INDEX_HEADING', -34, 'Index Heading'
        ),
        EnumMember(
            'INTENSE_EMPHASIS', -262, 'Intense Emphasis.'
        ),
        EnumMember(
            'INTENSE_QUOTE', -182, 'Intense Quote.'
        ),
        EnumMember(
            'INTENSE_REFERENCE', -264, 'Intense Reference.'
        ),
        EnumMember(
            'LINE_NUMBER', -41, 'Line Number.'
        ),
        EnumMember(
            'LIST', -48, 'List.'
        ),
        EnumMember(
            'LIST_2', -51, 'List 2.'
        ),
        EnumMember(
            'LIST_3', -52, 'List 3.'
        ),
        EnumMember(
            'LIST_4', -53, 'List 4.'
        ),
        EnumMember(
            'LIST_5', -54, 'List 5.'
        ),
        EnumMember(
            'LIST_BULLET', -49, 'List Bullet.'
        ),
        EnumMember(
            'LIST_BULLET_2', -55, 'List Bullet 2.'
        ),
        EnumMember(
            'LIST_BULLET_3', -56, 'List Bullet 3.'
        ),
        EnumMember(
            'LIST_BULLET_4', -57, 'List Bullet 4.'
        ),
        EnumMember(
            'LIST_BULLET_5', -58, 'List Bullet 5.'
        ),
        EnumMember(
            'LIST_CONTINUE', -69, 'List Continue.'
        ),
        EnumMember(
            'LIST_CONTINUE_2', -70, 'List Continue 2.'
        ),
        EnumMember(
            'LIST_CONTINUE_3', -71, 'List Continue 3.'
        ),
        EnumMember(
            'LIST_CONTINUE_4', -72, 'List Continue 4.'
        ),
        EnumMember(
            'LIST_CONTINUE_5', -73, 'List Continue 5.'
        ),
        EnumMember(
            'LIST_NUMBER', -50, 'List Number.'
        ),
        EnumMember(
            'LIST_NUMBER_2', -59, 'List Number 2.'
        ),
        EnumMember(
            'LIST_NUMBER_3', -60, 'List Number 3.'
        ),
        EnumMember(
            'LIST_NUMBER_4', -61, 'List Number 4.'
        ),
        EnumMember(
            'LIST_NUMBER_5', -62, 'List Number 5.'
        ),
        EnumMember(
            'LIST_PARAGRAPH', -180, 'List Paragraph.'
        ),
        EnumMember(
            'MACRO_TEXT', -46, 'Macro Text.'
        ),
        EnumMember(
            'MESSAGE_HEADER', -74, 'Message Header.'
        ),
        EnumMember(
            'NAV_PANE', -90, 'Document Map.'
        ),
        EnumMember(
            'NORMAL', -1, 'Normal.'
        ),
        EnumMember(
            'NORMAL_INDENT', -29, 'Normal Indent.'
        ),
        EnumMember(
            'NORMAL_OBJECT', -158, 'Normal (applied to an object).'
        ),
        EnumMember(
            'NORMAL_TABLE', -106, 'Normal (applied within a table).'
        ),
        EnumMember(
            'NOTE_HEADING', -80, 'Note Heading.'
        ),
        EnumMember(
            'PAGE_NUMBER', -42, 'Page Number.'
        ),
        EnumMember(
            'PLAIN_TEXT', -91, 'Plain Text.'
        ),
        EnumMember(
            'QUOTE', -181, 'Quote.'
        ),
        EnumMember(
            'SALUTATION', -76, 'Salutation.'
        ),
        EnumMember(
            'SIGNATURE', -65, 'Signature.'
        ),
        EnumMember(
            'STRONG', -88, 'Strong.'
        ),
        EnumMember(
            'SUBTITLE', -75, 'Subtitle.'
        ),
        EnumMember(
            'SUBTLE_EMPHASIS', -261, 'Subtle Emphasis.'
        ),
        EnumMember(
            'SUBTLE_REFERENCE', -263, 'Subtle Reference.'
        ),
        EnumMember(
            'TABLE_COLORFUL_GRID', -172, 'Colorful Grid.'
        ),
        EnumMember(
            'TABLE_COLORFUL_LIST', -171, 'Colorful List.'
        ),
        EnumMember(
            'TABLE_COLORFUL_SHADING', -170, 'Colorful Shading.'
        ),
        EnumMember(
            'TABLE_DARK_LIST', -169, 'Dark List.'
        ),
        EnumMember(
            'TABLE_LIGHT_GRID', -161, 'Light Grid.'
        ),
        EnumMember(
            'TABLE_LIGHT_GRID_ACCENT_1', -175, 'Light Grid Accent 1.'
        ),
        EnumMember(
            'TABLE_LIGHT_LIST', -160, 'Light List.'
        ),
        EnumMember(
            'TABLE_LIGHT_LIST_ACCENT_1', -174, 'Light List Accent 1.'
        ),
        EnumMember(
            'TABLE_LIGHT_SHADING', -159, 'Light Shading.'
        ),
        EnumMember(
            'TABLE_LIGHT_SHADING_ACCENT_1', -173, 'Light Shading Accent 1.'
        ),
        EnumMember(
            'TABLE_MEDIUM_GRID_1', -166, 'Medium Grid 1.'
        ),
        EnumMember(
            'TABLE_MEDIUM_GRID_2', -167, 'Medium Grid 2.'
        ),
        EnumMember(
            'TABLE_MEDIUM_GRID_3', -168, 'Medium Grid 3.'
        ),
        EnumMember(
            'TABLE_MEDIUM_LIST_1', -164, 'Medium List 1.'
        ),
        EnumMember(
            'TABLE_MEDIUM_LIST_1_ACCENT_1', -178, 'Medium List 1 Accent 1.'
        ),
        EnumMember(
            'TABLE_MEDIUM_LIST_2', -165, 'Medium List 2.'
        ),
        EnumMember(
            'TABLE_MEDIUM_SHADING_1', -162, 'Medium Shading 1.'
        ),
        EnumMember(
            'TABLE_MEDIUM_SHADING_1_ACCENT_1', -176,
            'Medium Shading 1 Accent 1.'
        ),
        EnumMember(
            'TABLE_MEDIUM_SHADING_2', -163, 'Medium Shading 2.'
        ),
        EnumMember(
            'TABLE_MEDIUM_SHADING_2_ACCENT_1', -177,
            'Medium Shading 2 Accent 1.'
        ),
        EnumMember(
            'TABLE_OF_AUTHORITIES', -45, 'Table of Authorities.'
        ),
        EnumMember(
            'TABLE_OF_FIGURES', -36, 'Table of Figures.'
        ),
        EnumMember(
            'TITLE', -63, 'Title.'
        ),
        EnumMember(
            'TOAHEADING', -47, 'TOA Heading.'
        ),
        EnumMember(
            'TOC_1', -20, 'TOC 1.'
        ),
        EnumMember(
            'TOC_2', -21, 'TOC 2.'
        ),
        EnumMember(
            'TOC_3', -22, 'TOC 3.'
        ),
        EnumMember(
            'TOC_4', -23, 'TOC 4.'
        ),
        EnumMember(
            'TOC_5', -24, 'TOC 5.'
        ),
        EnumMember(
            'TOC_6', -25, 'TOC 6.'
        ),
        EnumMember(
            'TOC_7', -26, 'TOC 7.'
        ),
        EnumMember(
            'TOC_8', -27, 'TOC 8.'
        ),
        EnumMember(
            'TOC_9', -28, 'TOC 9.'
        ),
    )


class WD_STYLE_TYPE(XmlEnumeration):
    """
    Specifies one of the four style types: paragraph, character, list, or
    table.

    Example::

        from docx import Document
        from docx.enum.style import WD_STYLE_TYPE

        styles = Document().styles
        assert styles[0].type == WD_STYLE_TYPE.PARAGRAPH
    """

    __ms_name__ = 'WdStyleType'

    __url__ = 'http://msdn.microsoft.com/en-us/library/office/ff196870.aspx'

    __members__ = (
        XmlMappedEnumMember(
            'CHARACTER', 2, 'character', 'Character style.'
        ),
        XmlMappedEnumMember(
            'LIST', 4, 'numbering', 'List style.'
        ),
        XmlMappedEnumMember(
            'PARAGRAPH', 1, 'paragraph', 'Paragraph style.'
        ),
        XmlMappedEnumMember(
            'TABLE', 3, 'table', 'Table style.'
        ),
    )
