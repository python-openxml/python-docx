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
