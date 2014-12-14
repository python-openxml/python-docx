# encoding: utf-8

"""
Core properties part, corresponds to ``/docProps/core.xml`` part in package.
"""

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

from ..part import XmlPart


class CorePropertiesPart(XmlPart):
    """
    Corresponds to part named ``/docProps/core.xml``, containing the core
    document properties for this document package.
    """
    @classmethod
    def default(cls, package):
        """
        Return a new |CorePropertiesPart| object initialized with default
        values for its base properties.
        """
        raise NotImplementedError

    @property
    def core_properties(self):
        """
        A |CoreProperties| object providing read/write access to the core
        properties contained in this core properties part.
        """
        raise NotImplementedError
