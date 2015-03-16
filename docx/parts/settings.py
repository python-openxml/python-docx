# encoding: utf-8

"""
|SettingsPart| and closely related objects
"""

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

from ..opc.part import XmlPart


class SettingsPart(XmlPart):
    """
    Document-level settings part of a WordprocessingML (WML) package.
    """
    @property
    def settings(self):
        """
        A |Settings| proxy object for the `w:settings` element in this part,
        containing the document-level settings for this document.
        """
        raise NotImplementedError
