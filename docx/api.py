# encoding: utf-8

"""
Directly exposed API functions and classes, :func:`Document` for now.
Provides a syntactically more convenient API for interacting with the
OpcPackage graph.
"""

import os

from docx.opc.constants import CONTENT_TYPE as CT
from docx.package import Package


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

    def add_inline_picture(self, image_path_or_stream):
        """
        Add the image at *image_path_or_stream* to the document at its native
        size. The picture is placed inline in a new paragraph at the end of
        the document.
        """
        return self.inline_shapes.add_picture(image_path_or_stream)

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

    @property
    def body(self):
        """
        Return a reference to the |_Body| instance for this document.
        """
        return self._document_part.body

    @property
    def inline_shapes(self):
        """
        Return a reference to the |InlineShapes| instance for this document.
        """
        return self._document_part.inline_shapes

    @property
    def paragraphs(self):
        """
        A list of |Paragraph| instances corresponding to the paragraphs in
        the document, in document order. Note that paragraphs within revision
        marks such as inserted or deleted do not appear in this list.
        """
        return self._document_part.paragraphs

    def save(self, path_or_stream):
        """
        Save this document to *path_or_stream*, which can be either a path to
        a filesystem location (a string) or a file-like object.
        """
        self._package.save(path_or_stream)

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
