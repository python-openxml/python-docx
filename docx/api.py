# encoding: utf-8

"""
Directly exposed API functions and classes, :func:`Document` for now.
Provides a syntactically more convenient API for interacting with the
OpcPackage graph.
"""

from __future__ import absolute_import, division, print_function

import os

from docx.enum.section import WD_SECTION
from docx.opc.constants import CONTENT_TYPE as CT, RELATIONSHIP_TYPE as RT
from docx.package import Package
from docx.parts.numbering import NumberingPart
from docx.shared import lazyproperty


def DocumentNew(docx=None):
    """
    Return a |Document| object loaded from *docx*, where *docx* can be
    either a path to a ``.docx`` file (a string) or a file-like object. If
    *docx* is missing or ``None``, the built-in default document "template"
    is loaded.
    """
    docx = _default_docx_path() if docx is None else docx
    document_part = Package.open(docx).main_document_part
    if document_part.content_type != CT.WML_DOCUMENT_MAIN:
        tmpl = "file '%s' is not a Word file, content type is '%s'"
        raise ValueError(tmpl % (docx, document_part.content_type))
    return document_part.document


def _default_docx_path():
    """
    Return the path to the built-in default .docx package.
    """
    _thisdir = os.path.split(__file__)[0]
    return os.path.join(_thisdir, 'templates', 'default.docx')


class Document(object):
    """
    Return a |Document| instance loaded from *docx*, where *docx* can be
    either a path to a ``.docx`` file (a string) or a file-like object. If
    *docx* is missing or ``None``, the built-in default document "template"
    is loaded.
    """
    def __init__(self, docx=None):
        self._document = document = DocumentNew(docx)
        self._document_part = document._part
        self._package = document._part.package

    def add_heading(self, text='', level=1):
        return self._document.add_heading(text, level)

    def add_page_break(self):
        return self._document.add_page_break()

    def add_paragraph(self, text='', style=None):
        return self._document.add_paragraph(text, style)

    def add_picture(self, image_descriptor, width=None, height=None):
        return self._document.add_picture(image_descriptor, width, height)

    def add_section(self, start_type=WD_SECTION.NEW_PAGE):
        return self._document.add_section(start_type)

    def add_table(self, rows, cols, style='Light Shading Accent 1'):
        return self._document.add_table(rows, cols, style)

    @property
    def core_properties(self):
        return self._document.core_properties

    @property
    def inline_shapes(self):
        return self._document.inline_shapes

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

    @property
    def part(self):
        return self._document.part

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

    @property
    def styles(self):
        """
        A |Styles| object providing access to the styles for this document.
        """
        return self._document_part.styles

    @property
    def tables(self):
        """
        A list of |Table| instances corresponding to the tables in the
        document, in document order. Note that tables within revision marks
        such as ``<w:ins>`` or ``<w:del>`` do not appear in this list.
        """
        return self._document_part.tables
