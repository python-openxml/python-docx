# encoding: utf-8

"""
Provides StylesPart and related objects
"""

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

from ..opc.package import Part


class StylesPart(Part):
    """
    Proxy for the styles.xml part containing style definitions for a document
    or glossary.
    """
    @classmethod
    def new(cls):
        """
        Return newly created empty styles part, containing only the root
        ``<w:styles>`` element.
        """
        raise NotImplementedError
