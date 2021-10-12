# encoding: utf-8

"""|FootnotesPart| and related objects"""

from __future__ import absolute_import, division, print_function, unicode_literals

from docx.opc.part import XmlPart


class FootnotesPart(XmlPart):
    """Package part containing footnotes"""
