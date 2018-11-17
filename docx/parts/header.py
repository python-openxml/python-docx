# encoding: utf-8

"""
|HeaderPart| and closely related objects
"""

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

from ..opc.part import XmlPart
from ..header import Header


class HeaderPart(XmlPart):
    """
    Main header part of a WordprocessingML (WML) package, aka a .docx file.
    Acts as broker to other parts such as image, core properties, and style
    parts. It also acts as a convenient delegate when a mid-document object
    needs a service involving a remote ancestor. The `Parented.part` property
    inherited by many content objects provides access to this part object for
    that purpose.
    """

    @property
    def core_properties(self):
        """
        A |CoreProperties| object providing read/write access to the core
        properties of this header.
        """
        return self.package.core_properties

    @property
    def header(self):
        return Header(self._element, self)
