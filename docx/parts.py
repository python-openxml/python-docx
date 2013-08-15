# -*- coding: utf-8 -*-
#
# parts.py
#
# Copyright (C) 2013 Steve Canny scanny@cisco.com
#
# This module is part of python-docx and is released under the MIT License:
# http://www.opensource.org/licenses/mit-license.php

"""
Document parts such as _Document, and closely related classes.
"""

from opc import Part


class _Document(Part):
    """
    Main document part of a WordprocessingML (WML) package, aka a .docx file.
    """
    @property
    def body(self):
        """
        The |_Body| instance containing the content for this document.
        """
