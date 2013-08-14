# -*- coding: utf-8 -*-
#
# oxml/parts.py
#
# Copyright (C) 2013 Steve Canny scanny@cisco.com
#
# This module is part of python-docx and is released under the MIT License:
# http://www.opensource.org/licenses/mit-license.php

"""
Custom element classes that correspond to OPC parts like <w:document>.
"""

from docx.oxml.base import OxmlBaseElement
from docx.oxml.text import CT_P


class CT_Document(OxmlBaseElement):
    """
    ``<w:document>`` element, the root element of a document.xml file.
    """


class CT_Body(OxmlBaseElement):
    """
    ``<w:body>``, the container element for the main document story in
    ``document.xml``.
    """
    def add_p(self):
        """
        Return a new <w:p> element that has been added at the end of any
        existing body content.
        """
        p = CT_P.new()
        if hasattr(self, 'sectPr'):
            self.sectPr.addprevious(p)
        else:
            self.append(p)
        return p

    def clear_content(self):
        """
        Remove all content child elements from this <w:body> element. Leave
        the <w:sectPr> element if it is present.
        """
        children = self.getchildren()
        content_elms = children[:-1] if self._has_sectPr else children
        for content_elm in content_elms:
            self.remove(content_elm)

    @property
    def _has_sectPr(self):
        """
        Return True if this <w:body> element has a <w:sectPr> child element,
        False otherwise.
        """
        return hasattr(self, 'sectPr')
