# -*- coding: utf-8 -*-
#
# test_text.py
#
# Copyright (C) 2013 Steve Canny scanny@cisco.com
#
# This module is part of python-docx and is released under the MIT License:
# http://www.opensource.org/licenses/mit-license.php

"""Test suite for the docx.text module."""

from docx.oxml.text import CT_P
from docx.text import Paragraph, Run

import pytest

from mock import call, create_autospec, Mock

from .unitutil import class_mock


class DescribeParagraph(object):

    @pytest.fixture
    def Run_(self, request):
        return class_mock('docx.text.Run', request)

    def it_has_a_sequence_of_the_runs_it_contains(self, Run_):
        p_elm = Mock(name='p_elm')
        r1, r2 = (Mock(name='r1'), Mock(name='r2'))
        R1, R2 = (Mock(name='Run1'), Mock(name='Run2'))
        p_elm.r_elms = [r1, r2]
        p = Paragraph(p_elm)
        Run_.side_effect = [R1, R2]
        # exercise ---------------------
        runs = p.runs
        # verify -----------------------
        assert Run_.mock_calls == [call(r1), call(r2)]
        assert runs == (R1, R2)

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


class DescribeRun(object):

    @pytest.fixture
    def Text_(self, request):
        return class_mock('docx.text.Text', request)

    def it_can_add_text_to_itself(self, Text_):
        # mockery ----------------------
        r_elm = Mock(name='r_elm')
        r_elm.add_t.return_value = t_elm = Mock(name='t_elm')
        text = Mock(name='text')
        r = Run(r_elm)
        # exercise ---------------------
        t = r.add_text(text)
        # verify -----------------------
        r_elm.add_t.assert_called_once_with(text)
        Text_.assert_called_once_with(t_elm)
        assert t is Text_.return_value

    def it_has_a_composite_of_the_text_it_contains(self):
        # mockery ----------------------
        t1, t2 = (Mock(name='t1', text='foo'), Mock(name='t2', text='bar'))
        r_elm = Mock(name='r_elm', t_elms=[t1, t2])
        r = Run(r_elm)
        # verify -----------------------
        assert r.text == 'foobar'
