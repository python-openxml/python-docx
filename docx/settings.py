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
