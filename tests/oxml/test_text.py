# -*- coding: utf-8 -*-
#
# test_text.py
#
# Copyright (C) 2013 Steve Canny scanny@cisco.com
#
# This module is part of python-docx and is released under the MIT License:
# http://www.opensource.org/licenses/mit-license.php

"""Test suite for the docx.oxml.text module."""

from docx.oxml.text import CT_P

from ..unitdata import a_p


class DescribeCT_P(object):

    def it_can_construct_a_new_p_element(self):
        p = CT_P.new()
        expected_xml = a_p().with_nsdecls().xml
        assert p.xml == expected_xml
