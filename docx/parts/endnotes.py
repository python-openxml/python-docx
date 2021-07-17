# encoding: utf-8

"""|EndnotesPart| and closely related objects"""

from __future__ import absolute_import, division, print_function, unicode_literals

from docx.opc.part import XmlPart


class EndnotesPart(XmlPart):
    """Package part containing end-notes"""
