# encoding: utf-8

"""|BaseStoryPart| and related objects"""

from __future__ import absolute_import, division, print_function, unicode_literals

from docx.opc.part import XmlPart
from docx.shared import lazyproperty


class BaseStoryPart(XmlPart):
    """Base class for story parts.

    A story part is one that can contain textual content, such as the document-part and
    header or footer parts. These all share content behaviors like `.paragraphs`,
    `.add_paragraph()`, `.add_table()` etc.
    """

    def get_style(self, style_id, style_type):
        """Return the style in this document matching *style_id*.

        Returns the default style for *style_type* if *style_id* is |None| or does not
        match a defined style of *style_type*.
        """
        return self._document_part.get_style(style_id, style_type)

    def get_style_id(self, style_or_name, style_type):
        """Return str style_id for *style_or_name* of *style_type*.

        Returns |None| if the style resolves to the default style for *style_type* or if
        *style_or_name* is itself |None|. Raises if *style_or_name* is a style of the
        wrong type or names a style not present in the document.
        """
        return self._document_part.get_style_id(style_or_name, style_type)

    @lazyproperty
    def _document_part(self):
        """|DocumentPart| object for this package."""
        return self.package.main_document_part
