# encoding: utf-8

"""
Run-related proxy objects for python-docx, Run in particular.
"""

from __future__ import absolute_import, print_function, unicode_literals

from ..enum.style import WD_STYLE_TYPE
from ..enum.text import WD_BREAK
from .font import Font
from ..shape import InlineShape
from ..shared import Parented
from .run import Run


class Del(Parented):
    """
    A delRun object
    """
    def __init__(self, d, parent):
        super(Del,self).__init__(parent)
        self._d = self._element = self.element = d
    def add_run(self,text,style):
        """
        Append a run to this paragraph containing *text* and having character
        style identified by style ID *style*. *text* can contain tab
        (``\\t``) characters, which are converted to the appropriate XML form
        for a tab. *text* can also include newline (``\\n``) or carriage
        return (``\\r``) characters, each of which is converted to a line
        break.
        """
        r = self._p.add_r()
        run = Run(r, self)
        if text:
            run.deltext = text
        if style:
            run.style = style
        return run
    def add_text(self,text):

        t = self._d.add_dt(text)
        return _Text(t)

    def text(self,text):
        self._d.text = text


class _Text(object):
    """
    Proxy object wrapping ``<w:delText>`` element.
    """
    def __init__(self, t_elm):
        super(_Text, self).__init__()
        self._dt = t_elm
