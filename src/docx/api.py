"""Directly exposed API functions and classes, :func:`Document` for now.

Provides a syntactically more convenient API for interacting with the OpcPackage graph.
"""

from __future__ import annotations

import os
from typing import IO, TYPE_CHECKING, cast

from docx.opc.constants import CONTENT_TYPE as CT
from docx.package import Package

if TYPE_CHECKING:
    from docx.document import Document as DocumentObject
    from docx.parts.document import DocumentPart


# -- content-types of the main document part of each Word package kind python-docx can open --
_WORD_MAIN_CONTENT_TYPES = (
    CT.WML_DOCUMENT_MAIN,  # -- .docx --
    CT.WML_DOCUMENT_MACRO_MAIN,  # -- .docm --
    CT.WML_TEMPLATE_MAIN,  # -- .dotx --
    CT.WML_TEMPLATE_MACRO_MAIN,  # -- .dotm --
)


def Document(docx: str | IO[bytes] | None = None) -> DocumentObject:
    """Return a |Document| object loaded from `docx`, where `docx` can be either a path
    to a Word file (a string) or a file-like object.

    In addition to a regular ``.docx`` document, `docx` can be a macro-enabled document
    (``.docm``), a template (``.dotx``) or a macro-enabled template (``.dotm``). The
    package kind is preserved on save, as are any macros, which are carried along
    unchanged.

    If `docx` is missing or ``None``, the built-in default document "template" is
    loaded.
    """
    docx = _default_docx_path() if docx is None else docx
    document_part = cast("DocumentPart", Package.open(docx).main_document_part)
    if document_part.content_type not in _WORD_MAIN_CONTENT_TYPES:
        tmpl = "file '%s' is not a Word file, content type is '%s'"
        raise ValueError(tmpl % (docx, document_part.content_type))
    return document_part.document


def _default_docx_path():
    """Return the path to the built-in default .docx package."""
    _thisdir = os.path.split(__file__)[0]
    return os.path.join(_thisdir, "templates", "default.docx")
