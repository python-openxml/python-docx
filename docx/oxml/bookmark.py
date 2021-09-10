# encoding: utf-8

"""Custom element classes related to bookmarks."""

from __future__ import absolute_import, division, print_function, unicode_literals

from docx.oxml.simpletypes import ST_DecimalNumber, ST_String
from docx.oxml.xmlchemy import BaseOxmlElement, RequiredAttribute


class CT_Bookmark(BaseOxmlElement):
    """`w:bookmarkStart` element"""

    id = RequiredAttribute("w:id", ST_DecimalNumber)
    name = RequiredAttribute("w:name", ST_String)


class CT_MarkupRange(BaseOxmlElement):
    """`w:bookmarkEnd` element"""

    id = RequiredAttribute("w:id", ST_DecimalNumber)
