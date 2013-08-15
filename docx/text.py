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


class Run(object):
    """
    Proxy object wrapping ``<w:r>`` element.
    """
    def __init__(self, r_elm):
        super(Run, self).__init__()
        self._r = r_elm
