# -*- coding: utf-8 -*-
#
# parts.py
#
# Copyright (C) 2013 Steve Canny scanny@cisco.com
#
# This module is part of python-docx and is released under the MIT License:
# http://www.opensource.org/licenses/mit-license.php

"""
Document parts such as _Document, and closely related classes.
"""

from opc import Part

from docx.oxml.base import oxml_fromstring
from docx.text import Paragraph


class _Document(Part):
    """
    Main document part of a WordprocessingML (WML) package, aka a .docx file.
    """
    def __init__(self, partname, content_type, document_elm):
        super(_Document, self).__init__(partname, content_type)
        self._element = document_elm

    @property
    def body(self):
        """
        The |_Body| instance containing the content for this document.
        """
        return _Body(self._element.body)

    @staticmethod
    def load(partname, content_type, blob):
        document_elm = oxml_fromstring(blob)
        document = _Document(partname, content_type, document_elm)
        return document


class _Body(object):
    """
    Proxy for ``<w:body>`` element in this document, having primarily a
    container role.
    """
    def __init__(self, body_elm):
        super(_Body, self).__init__()
        self._body = body_elm

    def add_paragraph(self):
        p = self._body.add_p()
        return Paragraph(p)

    @property
    def paragraphs(self):
        if not hasattr(self._body, 'p'):
            return ()
        return tuple([Paragraph(p) for p in self._body.p])
