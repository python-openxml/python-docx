# encoding: utf-8

"""
Directly exposed API functions and classes, :func:`Document` for now.
Provides a syntactically more convenient API for interacting with the
OpcPackage graph.
"""

import os

from docx.opc.constants import CONTENT_TYPE as CT
from docx.package import Package


thisdir = os.path.split(__file__)[0]
_default_docx_path = os.path.join(thisdir, 'templates', 'default.docx')


def Document(docx=None):
    """
    Return a |_Document| instance loaded from *docx*, where *docx* can be
    either a path to a ``.docx`` file (a string) or a file-like object. If
    *docx* is missing or ``None``, the built-in default document "template"
    is loaded.
    """
    if docx is None:
        docx = _default_docx_path
    pkg = Package.open(docx)
    document_part = pkg.main_document
    if document_part.content_type != CT.WML_DOCUMENT_MAIN:
        tmpl = "file '%s' is not a Word file, content type is '%s'"
        raise ValueError(tmpl % (docx, document_part.content_type))
    return _Document(pkg, document_part)


class _Document(object):
    """
    API class representing a Word document.
    """
    def __init__(self, package, document_part):
        super(_Document, self).__init__()
        self._document_part = document_part
        self._package = package

    def add_inline_picture(self, image_path_or_stream):
        """
        Add the image at *image_path_or_stream* to the document at its native
        size. The picture is placed inline in a new paragraph at the end of
        the document.
        """
        return self.inline_shapes.add_picture(image_path_or_stream)

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

    def save(self, file_):
        """
        Save this document to *file_*, where *file_* can be either a path to
        a file (a string) or a file-like object.
        """
        self._package.save(file_)
