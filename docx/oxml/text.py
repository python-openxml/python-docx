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
        r = CT_R.new()
        self.append(r)
        return r

    @staticmethod
    def new():
        """
        Return a new ``<w:p>`` element.
        """
        xml = '<w:p %s/>' % nsdecls('w')
        p = oxml_fromstring(xml)
        return p


class CT_R(OxmlBaseElement):
    """
    ``<w:r>`` element, containing the properties and text for a run.
    """
    @staticmethod
    def new():
        """
        Return a new ``<w:r>`` element.
        """
        xml = '<w:r %s/>' % nsdecls('w')
        return oxml_fromstring(xml)

    def add_t(self, text):
        """
        Return a newly added CT_T (<w:t>) element containing *text*.
        """
        t = CT_Text.new(text)
        self.append(t)
        return t


class CT_Text(OxmlBaseElement):
    """
    ``<w:t>`` element, containing a sequence of characters within a run.
    """
    @staticmethod
    def new(text):
        """
        Return a new ``<w:t>`` element.
        """
        xml = '<w:t %s>%s</w:t>' % (nsdecls('w'), text)
        return oxml_fromstring(xml)
