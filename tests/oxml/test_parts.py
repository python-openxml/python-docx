# -*- coding: utf-8 -*-
#
# test_parts.py
#
# Copyright (C) 2013 Steve Canny scanny@cisco.com
#
# This module is part of python-docx and is released under the MIT License:
# http://www.opensource.org/licenses/mit-license.php

"""Test suite for the docx.oxml.parts module."""

from docx.oxml.text import CT_P

from ..unitdata import a_body


class DescribeCT_Body(object):

    def it_can_add_a_p_to_itself(self):
        """
        Return a newly created |CT_P| element that has been added after any
        existing content.
        """
        cases = (
            (a_body(),               a_body().with_p()),
            (a_body().with_sectPr(), a_body().with_p().with_sectPr()),
        )
        for before_body_bldr, after_body_bldr in cases:
            body = before_body_bldr.element
            # exercise -----------------
            p = body.add_p()
            # verify -------------------
            assert body.xml == after_body_bldr.xml
            assert isinstance(p, CT_P)
