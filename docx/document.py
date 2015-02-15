# encoding: utf-8

"""
|Document| and closely related objects
"""

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

from .blkcntnr import BlockItemContainer
from .enum.section import WD_SECTION
from .enum.text import WD_BREAK
from .section import Section
from .shared import ElementProxy


class Document(ElementProxy):
    """
    WordprocessingML (WML) document.
    """

    __slots__ = ('_part', '__body')

    def __init__(self, element, part):
        super(Document, self).__init__(element)
        self._part = part
        self.__body = None

    def add_heading(self, text='', level=1):
        """
        Return a heading paragraph newly added to the end of the document,
        containing *text* and having its paragraph style determined by
        *level*. If *level* is 0, the style is set to `Title`. If *level* is
        1 (or omitted), `Heading 1` is used. Otherwise the style is set to
        `Heading {level}`. Raises |ValueError| if *level* is outside the
        range 0-9.
        """
        if not 0 <= level <= 9:
            raise ValueError("level must be in range 0-9, got %d" % level)
        style = 'Title' if level == 0 else 'Heading %d' % level
        return self.add_paragraph(text, style)

    def add_page_break(self):
        """
        Return a paragraph newly added to the end of the document and
        containing only a page break.
        """
        paragraph = self.add_paragraph()
        paragraph.add_run().add_break(WD_BREAK.PAGE)
        return paragraph

    def add_paragraph(self, text='', style=None):
        """
        Return a paragraph newly added to the end of the document, populated
        with *text* and having paragraph style *style*. *text* can contain
        tab (``\\t``) characters, which are converted to the appropriate XML
        form for a tab. *text* can also include newline (``\\n``) or carriage
        return (``\\r``) characters, each of which is converted to a line
        break.
        """
        return self._body.add_paragraph(text, style)

    def add_picture(self, image_path_or_stream, width=None, height=None):
        """
        Return a new picture shape added in its own paragraph at the end of
        the document. The picture contains the image at
        *image_path_or_stream*, scaled based on *width* and *height*. If
        neither width nor height is specified, the picture appears at its
        native size. If only one is specified, it is used to compute
        a scaling factor that is then applied to the unspecified dimension,
        preserving the aspect ratio of the image. The native size of the
        picture is calculated using the dots-per-inch (dpi) value specified
        in the image file, defaulting to 72 dpi if no value is specified, as
        is often the case.
        """
        run = self.add_paragraph().add_run()
        return run.add_picture(image_path_or_stream, width, height)

    def add_section(self, start_type=WD_SECTION.NEW_PAGE):
        """
        Return a |Section| object representing a new section added at the end
        of the document. The optional *start_type* argument must be a member
        of the :ref:`WdSectionStart` enumeration, and defaults to
        ``WD_SECTION.NEW_PAGE`` if not provided.
        """
        new_sectPr = self._element.body.add_section_break()
        new_sectPr.start_type = start_type
        return Section(new_sectPr)

    def add_table(self, rows, cols, style='Light Shading Accent 1'):
        """
        Add a table having row and column counts of *rows* and *cols*
        respectively and table style of *style*. If *style* is |None|, a
        table with no style is produced.
        """
        table = self._body.add_table(rows, cols)
        table.style = style
        return table

    @property
    def part(self):
        """
        The |DocumentPart| object of this document.
        """
        return self._part

    @property
    def _body(self):
        """
        The |_Body| instance containing the content for this document.
        """
        if self.__body is None:
            self.__body = _Body(self._element.body, self)
        return self.__body


class _Body(BlockItemContainer):
    """
    Proxy for ``<w:body>`` element in this document, having primarily a
    container role.
    """
    def __init__(self, body_elm, parent):
        super(_Body, self).__init__(body_elm, parent)
        self._body = body_elm
