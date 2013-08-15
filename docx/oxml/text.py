# -*- coding: utf-8 -*-
#
# oxml/text.py
#
# Copyright (C) 2013 Steve Canny scanny@cisco.com
#
# This module is part of python-docx and is released under the MIT License:
# http://www.opensource.org/licenses/mit-license.php

"""
Custom element classes related to text, such as paragraph (CT_P) and runs
(CT_R).
"""

from docx.oxml.base import nsdecls, OxmlBaseElement, oxml_fromstring


class CT_P(OxmlBaseElement):
    """
    ``<w:p>`` element, containing the properties and text for a paragraph.
    """
    def add_r(self):
        """
        Return a newly added CT_R (<w:r>) element.
        """

    @staticmethod
    def new():
        """
        Return a new ``<w:p>`` element.
        """
        xml = '<w:p %s/>' % nsdecls('w')
        p = oxml_fromstring(xml)
        return p
