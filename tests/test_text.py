# -*- coding: utf-8 -*-
#
# test_text.py
#
# Copyright (C) 2013 Steve Canny scanny@cisco.com
#
# This module is part of python-docx and is released under the MIT License:
# http://www.opensource.org/licenses/mit-license.php

"""Test suite for the docx.text module."""

from docx.text import Paragraph
from docx.oxml.text import CT_P

import pytest

from mock import create_autospec, Mock

from .unitutil import class_mock


class DescribeParagraph(object):

    @pytest.fixture
    def Run_(self, request):
        return class_mock('docx.text.Run', request)

    def it_can_add_a_run_to_itself(self, Run_):
        # mockery ----------------------
        p_elm = create_autospec(CT_P)
        p_elm.add_r.return_value = r_elm = Mock(name='r_elm')
        p = Paragraph(p_elm)
        # exercise ---------------------
        r = p.add_run()
        # verify -----------------------
        p_elm.add_r.assert_called_once_with()
        Run_.assert_called_once_with(r_elm)
        assert r is Run_.return_value
