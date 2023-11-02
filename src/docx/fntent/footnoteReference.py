# encoding: utf-8

from __future__ import absolute_import, division, print_function, unicode_literals

from ..shared import Parented

class FootnoteReference(Parented):
    """
    Proxy object wrapping ``<w:footnoteReference>`` element.
    """
    def __init__(self, footnoteReference, parent):
        super(FootnoteReference, self).__init__(parent)
        self._element = footnoteReference

    @property
    def footnote(self):
        return self.part.get_footnote(self._element.id)
