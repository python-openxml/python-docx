# encoding: utf-8

"""
Hyperlink proxy objects.
"""

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

from ..opc.constants import RELATIONSHIP_TYPE as RT
from ..shared import Parented
from .run import Run


class Hyperlink(Parented):
    """
    Proxy object wrapping ``<w:hyperlink>`` element.
    """
    def __init__(self, hyperlink, parent):
        super(Hyperlink, self).__init__(parent)
        self._hyperlink = self.element = hyperlink

    @property
    def address(self):
        rId = self._hyperlink.relationship
        return self.part.target_ref(rId) if rId else None

    @address.setter
    def address(self, url):
        rId = self.part.relate_to(url, RT.HYPERLINK, is_external=True)
        self._hyperlink.relationship = rId

    @property
    def anchor(self):
        return self._hyperlink.anchor

    @anchor.setter
    def anchor(self, anchor):
        self._hyperlink.anchor = anchor

    def iter_runs(self):
        return [Run(r, self) for r in self._hyperlink.r_lst]

    def insert_run(self, text, style=None):
        _r = self._hyperlink.add_r()
        run = Run(_r, self)
        run.text = text
        if style:
            run.style = style
        return run

    @property
    def text(self):
        return ''.join([run.text for run in self.iter_runs()])

    @text.setter
    def text(self, text):
        self._hyperlink.clear_content()
        self.insert_run(text)
