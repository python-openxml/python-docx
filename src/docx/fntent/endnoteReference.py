# encoding: utf-8

from __future__ import absolute_import, division, print_function, unicode_literals

from ..shared import Parented

class EndnoteReference(Parented):
    """
    Proxy object wrapping ``<w:endnoteReference>`` element.
    """
    def __init__(self, endnoteReference, parent):
        super(EndnoteReference, self).__init__(parent)
        self._element = endnoteReference

    @property
    def endnote(self):
        return self.part.get_endnote(self._element.id)
