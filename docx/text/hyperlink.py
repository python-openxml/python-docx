# encoding: utf-8

"""
Hyperlink proxy objects.
"""

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)
from .run import Run
from ..shared import Parented
from docx.opc.constants import RELATIONSHIP_TYPE as RT


class Hyperlink(Parented):
    """
    Proxy object wrapping ``<w:hyperlink>`` element, which in turn contains a
    ``<w:r>`` element. It has two main properties: The *url* it points to and
    the *text* that is shown on the page.
    """
    def __init__(self, hyperlink, parent):
        super(Hyperlink, self).__init__(parent)
        self._hyperlink = self.element = hyperlink

    @property
    def url(self):
        """
        Read/write. The relationship ID the Hyperlink points to, or |None| if
        it has no directly-applied relationship. Setting this property sets
        the The ``r:id`` attribute of the ``<w:rPr>`` element inside the
        hyperlink.
        """
        part = self.part
        rId = self._hyperlink.relationship
        url = part.target_ref(rId) if rId else ''
        return url

    @url.setter
    def url(self, url):
        part = self.part
        rId = part.relate_to(url, RT.HYPERLINK, is_external=True)
        self._hyperlink.relationship = rId

    @property
    def runs(self):
        """
        Sequence of |Run| instances corresponding to the <w:r> elements in
        this hyperlink.
        """
        return [Run(r, self) for r in self._hyperlink.r_lst]

    def add_run(self, text=None, style=None):
        """
        Append a run to this hyperlink containing *text* and having character
        style identified by style ID *style*. *text* can contain tab
        (``\\t``) characters, which are converted to the appropriate XML form
        for a tab. *text* can also include newline (``\\n``) or carriage
        return (``\\r``) characters, each of which is converted to a line
        break.
        """
        r = self._hyperlink.add_r()
        run = Run(r, self)
        if text:
            run.text = text
        if style:
            run.style = style
        return run

    @property
    def text(self):
        text = ''
        for run in self.runs:
            text += run.text
        return text

    @text.setter
    def text(self, text):
        self._hyperlink.clear_content()
        self.add_run(text)


class Text(object):
    """
    Proxy object wrapping ``<w:t>`` element.
    """
    def __init__(self, t_elm):
        super(Text, self).__init__()
        self._t = t_elm
