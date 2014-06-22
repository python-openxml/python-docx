# encoding: utf-8

"""
Directly exposed API functions and classes, :func:`Document` for now.
Provides a syntactically more convenient API for interacting with the
OpcPackage graph.
"""

from __future__ import absolute_import, division, print_function

import os

from docx.enum.section import WD_SECTION
from docx.enum.text import WD_BREAK
from docx.opc.constants import CONTENT_TYPE as CT, RELATIONSHIP_TYPE as RT
from docx.package import Package
from docx.parts.numbering import NumberingPart
from docx.parts.styles import StylesPart
from docx.shared import lazyproperty


_thisdir = os.path.split(__file__)[0]
_default_docx_path = os.path.join(_thisdir, 'templates', 'default.docx')


class Document(object):
    """
    Return a |Document| instance loaded from *docx*, where *docx* can be
    either a path to a ``.docx`` file (a string) or a file-like object. If
    *docx* is missing or ``None``, the built-in default document "template"
    is loaded.
    """
    def __init__(self, docx=None):
        super(Document, self).__init__()
        document_part, package = self._open(docx)
        self._document_part = document_part
        self._package = package

    def add_heading(self, text='', level=1):
        """
        Return a heading paragraph newly added to the end of the document,
        populated with *text* and having the heading paragraph style
        determined by *level*. If *level* is 0, the style is set to
        ``'Title'``. If *level* is 1 (or not present), ``'Heading1'`` is used.
        Otherwise the style is set to ``'Heading{level}'``. If *level* is
        outside the range 0-9, |ValueError| is raised.
        """
        if not 0 <= level <= 9:
            raise ValueError("level must be in range 0-9, got %d" % level)
        style = 'Title' if level == 0 else 'Heading%d' % level
        return self.add_paragraph(text, style)

    def add_page_break(self):
        """
        Return a paragraph newly added to the end of the document and
        containing only a page break.
        """
        p = self._document_part.add_paragraph()
        r = p.add_run()
        r.add_break(WD_BREAK.PAGE)
        return p

    def add_paragraph(self, text='', style=None):
        """
        Return a paragraph newly added to the end of the document, populated
        with *text* and having paragraph style *style*.
        """
        p = self._document_part.add_paragraph()
        if text:
            r = p.add_run()
            r.add_text(text)
        if style is not None:
            p.style = style
        return p

    def add_picture(self, image_path_or_stream, width=None, height=None):
        """
        Add the image at *image_path_or_stream* in a new paragraph at the end
        of the document. If neither width nor height is specified, the
        picture appears at its native size. If only one is specified, it is
        used to compute a scaling factor that is then applied to the
        unspecified dimension, preserving the aspect ratio of the image. The
        native size of the picture is calculated using the dots-per-inch
        (dpi) value specified in the image file, defaulting to 72 dpi if no
        value is specified, as is often the case.
        """
        picture = self.inline_shapes.add_picture(image_path_or_stream)

        # scale picture dimensions if width and/or height provided
        if width is not None or height is not None:
            native_width, native_height = picture.width, picture.height
            if width is None:
                scaling_factor = float(height) / float(native_height)
                width = int(round(native_width * scaling_factor))
            elif height is None:
                scaling_factor = float(width) / float(native_width)
                height = int(round(native_height * scaling_factor))
            # set picture to scaled dimensions
            picture.width = width
            picture.height = height

        return picture

    def add_section(self, start_type=WD_SECTION.NEW_PAGE):
        """
        Return a |Section| object representing a new section added at the end
        of the document. The optional *start_type* argument must be a member
        of the :ref:`WdSectionStart` enumeration defaulting to
        ``WD_SECTION.NEW_PAGE`` if not provided.
        """
        return self._document_part.add_section(start_type)

    def add_table(self, rows, cols, style='LightShading-Accent1'):
        """
        Add a table having row and column counts of *rows* and *cols*
        respectively and table style of *style*. If *style* is |None|, a
        table with no style is produced.
        """
        table = self._document_part.add_table(rows, cols)
        if style:
            table.style = style
        return table

    @property
    def inline_shapes(self):
        """
        Return a reference to the |InlineShapes| instance for this document.
        """
        return self._document_part.inline_shapes

    @lazyproperty
    def numbering_part(self):
        """
        Instance of |NumberingPart| for this document. Creates an empty
        numbering part if one is not present.
        """
        try:
            return self._document_part.part_related_by(RT.NUMBERING)
        except KeyError:
            numbering_part = NumberingPart.new()
            self._document_part.relate_to(numbering_part, RT.NUMBERING)
            return numbering_part

    @property
    def paragraphs(self):
        """
        A list of |Paragraph| instances corresponding to the paragraphs in
        the document, in document order. Note that paragraphs within revision
        marks such as ``<w:ins>`` or ``<w:del>`` do not appear in this list.
        """
        return self._document_part.paragraphs

    def save(self, path_or_stream):
        """
        Save this document to *path_or_stream*, which can be either a path to
        a filesystem location (a string) or a file-like object.
        """
        self._package.save(path_or_stream)

    @property
    def sections(self):
        """
        Return a reference to the |Sections| instance for this document.
        """
        return self._document_part.sections

    @lazyproperty
    def styles_part(self):
        """
        Instance of |StylesPart| for this document. Creates an empty styles
        part if one is not present.
        """
        try:
            return self._document_part.part_related_by(RT.STYLES)
        except KeyError:
            styles_part = StylesPart.new()
            self._document_part.relate_to(styles_part, RT.STYLES)
            return styles_part

    @property
    def tables(self):
        """
        A list of |Table| instances corresponding to the tables in the
        document, in document order. Note that tables within revision marks
        such as ``<w:ins>`` or ``<w:del>`` do not appear in this list.
        """
        return self._document_part.tables

    @staticmethod
    def _open(docx):
        """
        Return a (document_part, package) 2-tuple loaded from *docx*, where
        *docx* can be either a path to a ``.docx`` file (a string) or a
        file-like object. If *docx* is ``None``, the built-in default
        document "template" is loaded.
        """
        docx = _default_docx_path if docx is None else docx
        package = Package.open(docx)
        document_part = package.main_document
        if document_part.content_type != CT.WML_DOCUMENT_MAIN:
            tmpl = "file '%s' is not a Word file, content type is '%s'"
            raise ValueError(tmpl % (docx, document_part.content_type))
        return document_part, package
