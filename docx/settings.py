# encoding: utf-8

"""
Settings object, providing access to document-level settings.
"""

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

from .shared import ElementProxy


class Settings(ElementProxy):
    """
    Provides access to document-level settings for a document. Accessed using
    the :attr:`.Document.settings` property.
    """

    __slots__ = ()

    def __init__(self, element):
        super(Settings, self).__init__(element)
        self._element = element

    @property
    def odd_and_even_pages_header_footer(self):
        """
        |Length| object representing the bottom margin for all pages in this
        section in English Metric Units.
        """
        return self._element.evenOrOddHeaders

    @odd_and_even_pages_header_footer.setter
    def odd_and_even_pages_header_footer(self, value):
        self._element.evenOrOddHeaders_val = value