# encoding: utf-8

"""
|SettingsPart| and closely related objects
"""

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

from ..opc.part import XmlPart
from ..settings import Settings


class SettingsPart(XmlPart):
    """
    Document-level settings part of a WordprocessingML (WML) package.
    """
    @classmethod
    def default(cls, package):
        """
        Return a newly created settings part, containing a default
        `w:settings` element tree.
        """
        raise NotImplementedError

    @property
    def settings(self):
        """
        A |Settings| proxy object for the `w:settings` element in this part,
        containing the document-level settings for this document.
        """
        return Settings(self.element)
