# -*- coding: utf-8 -*-
#
# text.py
#
# Copyright (C) 2013 Steve Canny scanny@cisco.com
#
# This module is part of python-docx and is released under the MIT License:
# http://www.opensource.org/licenses/mit-license.php

"""
Text-related proxy types for python-docx, such as Paragraph and Run.
"""


class Paragraph(object):
    """
    Proxy object wrapping ``<w:p>`` element.
    """
    def __init__(self, p_elm):
        super(Paragraph, self).__init__()
        self._p = p_elm

    def add_run(self):
        """
        Append a run to this paragraph.
        """
        r = self._p.add_r()
        return Run(r)

    @property
    def runs(self):
        """
        Sequence of |Run| instances corresponding to the <w:r> elements in
        this paragraph.
        """
        return tuple([Run(r) for r in self._p.r_elms])

    @property
    def style(self):
        """
        Paragraph style for this paragraph. Read/Write.
        """
        style = self._p.style
        return style if style is not None else 'Normal'


class Run(object):
    """
    Proxy object wrapping ``<w:r>`` element.
    """
    def __init__(self, r_elm):
        super(Run, self).__init__()
        self._r = r_elm

    def add_text(self, text):
        """
        Add a text element to this run.
        """
        t = self._r.add_t(text)
        return Text(t)

    @property
    def text(self):
        """
        A string formed by concatenating all the <w:t> elements present in
        this run.
        """
        text = ''
        for t in self._r.t_elms:
            text += t.text
        return text


class Text(object):
    """
    Proxy object wrapping ``<w:t>`` element.
    """
    def __init__(self, t_elm):
        super(Text, self).__init__()
        self._t = t_elm
