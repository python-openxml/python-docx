# encoding: utf-8

"""Settings object, providing access to document-level settings"""

from __future__ import absolute_import, division, print_function, unicode_literals

from docx.shared import ElementProxy


class Settings(ElementProxy):
    """Provides access to document-level settings for a document.

    Accessed using the :attr:`.Document.settings` property.
    """

    __slots__ = ()

    @property
    def odd_and_even_pages_header_footer(self):
        """True if this document has distinct odd and even page headers and footers.

        Read/write.
        """
        return self._element.evenAndOddHeaders_val

    @odd_and_even_pages_header_footer.setter
    def odd_and_even_pages_header_footer(self, value):
        self._element.evenAndOddHeaders_val = value
