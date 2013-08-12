# -*- coding: utf-8 -*-
#
# test_text.py
#
# Copyright (C) 2013 Steve Canny scanny@cisco.com
#
# This module is part of python-docx and is released under the MIT License:
# http://www.opensource.org/licenses/mit-license.php

"""Test suite for the docx.oxml.text module."""

from docx.oxml.text import CT_P, CT_R, CT_Text

from ..unitdata import a_p, a_t, an_r


class DescribeCT_P(object):

    def it_can_construct_a_new_p_element(self):
        p = CT_P.new()
        expected_xml = a_p().with_nsdecls().xml
        assert p.xml == expected_xml

    def it_has_a_sequence_of_the_runs_it_contains(self):
        p = a_p().with_nsdecls().with_r(3).element
        assert len(p.r_elms) == 3
        for r in p.r_elms:
            assert isinstance(r, CT_R)

    def it_can_add_an_r_to_itself(self):
        p = a_p().with_nsdecls().element
        # exercise -----------------
        r = p.add_r()
        # verify -------------------
        assert p.xml == a_p().with_nsdecls().with_r().xml
        assert isinstance(r, CT_R)


class DescribeCT_R(object):

    def it_can_construct_a_new_r_element(self):
        r = CT_R.new()
        assert r.xml == an_r().with_nsdecls().xml

    def it_can_add_a_t_to_itself(self):
        text = 'foobar'
        r = an_r().with_nsdecls().element
        # exercise -----------------
        t = r.add_t(text)
        # verify -------------------
        assert r.xml == an_r().with_nsdecls().with_t(text).xml
        assert isinstance(t, CT_Text)

    def it_has_a_sequence_of_the_t_elms_it_contains(self):
        cases = (
            (an_r().with_nsdecls(), 0),
            (an_r().with_nsdecls().with_t('foo'), 1),
            (an_r().with_nsdecls().with_t('foo').with_t('bar'), 2),
        )
        for builder, expected_len in cases:
            r = builder.element
            assert len(r.t_elms) == expected_len
            for t in r.t_elms:
                assert isinstance(t, CT_Text)


class DescribeCT_Text(object):

    def it_can_construct_a_new_t_element(self):
        text = 'foobar'
        t = CT_Text.new(text)
        assert t.xml == a_t(text).with_nsdecls().xml
