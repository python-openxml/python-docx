# encoding: utf-8

"""Custom element classes related to end-notes"""

from __future__ import absolute_import, division, print_function, unicode_literals

from docx.oxml.xmlchemy import BaseOxmlElement


class CT_Endnotes(BaseOxmlElement):
    """`w:endnotes` element"""
