# encoding: utf-8

"""
Directly exposed API functions and classes, :func:`Document` for now.
Provides a syntactically more convenient API for interacting with the
OpcPackage graph.
"""

from __future__ import absolute_import, division, print_function

import os

from docx.opc.constants import CONTENT_TYPE as CT
from docx.package import Package


def Document(docx=None):
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
    return os.path.join(_thisdir, "templates", "default.docx")
