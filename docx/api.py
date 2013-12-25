# encoding: utf-8

"""
Directly exposed API functions and classes, :func:`Document` for now.
Provides a syntactically more convenient API for interacting with the
OpcPackage graph.
"""

import os

from docx.opc.package import OpcPackage
from docx.opc.constants import CONTENT_TYPE as CT


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
    pkg = OpcPackage.open(docx)
    document_part = pkg.main_document
    if document_part.content_type != CT.WML_DOCUMENT_MAIN:
        tmpl = "file '%s' is not a Word file, content type is '%s'"
        raise ValueError(tmpl % (docx, document_part.content_type))
    return _Document(pkg, document_part)


class _Document(object):
    """
    API class representing a Word document.
    """
    def __init__(self, pkg, document_part):
        super(_Document, self).__init__()
        self._document = document_part
        self._pkg = pkg

    @property
    def body(self):
        """
        Return a reference to the |_Body| instance for this document.
        """
        return self._document.body

    @property
    def inline_shapes(self):
        """
        Return a reference to the |InlineShapes| instance for this document.
        """
        return self._document.inline_shapes

    def save(self, file_):
        """
        Save this document to *file_*, where *file_* can be either a path to
        a file (a string) or a file-like object.
        """
        return self._pkg.save(file_)
