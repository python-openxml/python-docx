# encoding: utf-8

"""
Test suite for the docx.text module
"""

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

from docx.enum.text import WD_BREAK
from docx.oxml.text import CT_P, CT_R
from docx.text import Paragraph, Run

import pytest

from mock import call, Mock

from .oxml.unitdata.text import a_b, a_br, a_t, a_p, an_i, an_r, an_rPr
from .unitutil import class_mock, instance_mock


class DescribeParagraph(object):

    def it_has_a_sequence_of_the_runs_it_contains(self, runs_fixture):
        paragraph, Run_, r_, r_2_, run_, run_2_ = runs_fixture
        runs = paragraph.runs
        assert Run_.mock_calls == [call(r_), call(r_2_)]
        assert runs == [run_, run_2_]

    def it_can_add_a_run_to_itself(self, add_run_fixture):
        paragraph, text, expected_xml = add_run_fixture
        run = paragraph.add_run(text)
        assert paragraph._p.xml == expected_xml
        assert isinstance(run, Run)
        assert run._r is paragraph._p.r_lst[0]

    def it_knows_its_paragraph_style(self):
        cases = (
            (Mock(name='p_elm', style='foobar'), 'foobar'),
            (Mock(name='p_elm', style=None),     'Normal'),
        )
        for p_elm, expected_style in cases:
            p = Paragraph(p_elm)
            assert p.style == expected_style

    def it_can_set_its_paragraph_style(self):
        cases = (
            ('foobar', 'foobar'),
            ('Normal', None),
        )
        for style, expected_setting in cases:
            p_elm = Mock(name='p_elm')
            p = Paragraph(p_elm)
            p.style = style
            assert p_elm.style == expected_setting

    def it_knows_the_text_it_contains(self, text_prop_fixture):
        p, expected_text = text_prop_fixture
        assert p.text == expected_text

    # fixtures -------------------------------------------------------

    @pytest.fixture(params=[None, '', 'foobar'])
    def add_run_fixture(self, request, paragraph):
        text = request.param
        r_bldr = an_r()
        if text:
            r_bldr.with_child(a_t().with_text(text))
        expected_xml = a_p().with_nsdecls().with_child(r_bldr).xml()
        return paragraph, text, expected_xml

    @pytest.fixture
    def p_(self, request, r_, r_2_):
        return instance_mock(request, CT_P, r_lst=(r_, r_2_))

    @pytest.fixture
    def paragraph(self, request):
        p = a_p().with_nsdecls().element
        return Paragraph(p)

    @pytest.fixture
    def Run_(self, request, runs_):
        run_, run_2_ = runs_
        return class_mock(
            request, 'docx.text.Run', side_effect=[run_, run_2_]
        )

    @pytest.fixture
    def r_(self, request):
        return instance_mock(request, CT_R)

    @pytest.fixture
    def r_2_(self, request):
        return instance_mock(request, CT_R)

    @pytest.fixture
    def runs_(self, request):
        run_ = instance_mock(request, Run, name='run_')
        run_2_ = instance_mock(request, Run, name='run_2_')
        return run_, run_2_

    @pytest.fixture
    def runs_fixture(self, p_, Run_, r_, r_2_, runs_):
        paragraph = Paragraph(p_)
        run_, run_2_ = runs_
        return paragraph, Run_, r_, r_2_, run_, run_2_

    @pytest.fixture
    def text_prop_fixture(self):
        p = (
            a_p().with_nsdecls().with_child(
                an_r().with_child(
                    a_t().with_text('foo'))).with_child(
                an_r().with_child(
                    a_t().with_text(' de bar')))
        ).element
        paragraph = Paragraph(p)
        return paragraph, 'foo de bar'


class DescribeRun(object):

    def it_knows_if_its_bold(self, bold_get_fixture):
        run, is_bold = bold_get_fixture
        assert run.bold == is_bold

    def it_knows_if_its_italic(self, italic_get_fixture):
        run, is_italic = italic_get_fixture
        assert run.italic == is_italic

    def it_can_change_its_bold_setting(self, bold_set_fixture):
        run, bold_value, expected_xml = bold_set_fixture
        run.bold = bold_value
        assert run._r.xml == expected_xml

    def it_can_change_its_italic_setting(self, italic_set_fixture):
        run, italic_value, expected_xml = italic_set_fixture
        run.italic = italic_value
        assert run._r.xml == expected_xml

    def it_can_add_text(self, add_text_fixture):
        run, text_str, expected_xml, Text_ = add_text_fixture
        _text = run.add_text(text_str)
        assert run._r.xml == expected_xml
        assert _text is Text_.return_value

    def it_can_add_a_break(self, add_break_fixture):
        run, break_type, expected_xml = add_break_fixture
        run.add_break(break_type)
        assert run._r.xml == expected_xml

    def it_knows_the_text_it_contains(self, text_prop_fixture):
        run, expected_text = text_prop_fixture
        assert run.text == expected_text

    # fixtures -------------------------------------------------------

    @pytest.fixture(params=[
        'line', 'page', 'column', 'clr_lt', 'clr_rt', 'clr_all'
    ])
    def add_break_fixture(self, request, run):
        type_, clear, break_type = {
            'line':    (None,           None,    WD_BREAK.LINE),
            'page':    ('page',         None,    WD_BREAK.PAGE),
            'column':  ('column',       None,    WD_BREAK.COLUMN),
            'clr_lt':  ('textWrapping', 'left',  WD_BREAK.LINE_CLEAR_LEFT),
            'clr_rt':  ('textWrapping', 'right', WD_BREAK.LINE_CLEAR_RIGHT),
            'clr_all': ('textWrapping', 'all',   WD_BREAK.LINE_CLEAR_ALL),
        }[request.param]
        # expected_xml -----------------
        br_bldr = a_br()
        if type_ is not None:
            br_bldr.with_type(type_)
        if clear is not None:
            br_bldr.with_clear(clear)
        expected_xml = an_r().with_nsdecls().with_child(br_bldr).xml()
        return run, break_type, expected_xml

    @pytest.fixture(params=['foobar', ' foo bar', 'bar foo '])
    def add_text_fixture(self, request, run, Text_):
        text_str = request.param
        t_bldr = a_t().with_text(text_str)
        if text_str.startswith(' ') or text_str.endswith(' '):
            t_bldr.with_space('preserve')
        expected_xml = an_r().with_nsdecls().with_child(t_bldr).xml()
        return run, text_str, expected_xml, Text_

    @pytest.fixture(params=[True, False, None])
    def bold_get_fixture(self, request):
        is_bold = request.param
        r_bldr = an_r().with_nsdecls()
        if is_bold is not None:
            b_bldr = a_b()
            if is_bold is False:
                b_bldr.with_val('off')
            rPr_bldr = an_rPr().with_child(b_bldr)
            r_bldr.with_child(rPr_bldr)
        r = r_bldr.element
        run = Run(r)
        return run, is_bold

    @pytest.fixture(params=[True, False, None])
    def italic_get_fixture(self, request):
        is_italic = request.param
        r_bldr = an_r().with_nsdecls()
        if is_italic is not None:
            i_bldr = an_i()
            if is_italic is False:
                i_bldr.with_val('off')
            rPr_bldr = an_rPr().with_child(i_bldr)
            r_bldr.with_child(rPr_bldr)
        r = r_bldr.element
        run = Run(r)
        return run, is_italic

    @pytest.fixture(params=[True, False, None])
    def bold_set_fixture(self, request):
        # run --------------------------
        r = an_r().with_nsdecls().element
        run = Run(r)
        # bold_value -------------------
        bold_value = request.param
        # expected_xml -----------------
        rPr_bldr = an_rPr()
        if bold_value is not None:
            b_bldr = a_b()
            if bold_value is False:
                b_bldr.with_val(0)
            rPr_bldr.with_child(b_bldr)
        expected_xml = an_r().with_nsdecls().with_child(rPr_bldr).xml()
        return run, bold_value, expected_xml

    @pytest.fixture(params=[True, False, None])
    def italic_set_fixture(self, request):
        # run --------------------------
        r = an_r().with_nsdecls().element
        run = Run(r)
        # italic_value -------------------
        italic_value = request.param
        # expected_xml -----------------
        rPr_bldr = an_rPr()
        if italic_value is not None:
            i_bldr = an_i()
            if italic_value is False:
                i_bldr.with_val(0)
            rPr_bldr.with_child(i_bldr)
        expected_xml = an_r().with_nsdecls().with_child(rPr_bldr).xml()
        return run, italic_value, expected_xml

    @pytest.fixture
    def run(self):
        r = an_r().with_nsdecls().element
        return Run(r)

    @pytest.fixture
    def Text_(self, request):
        return class_mock(request, 'docx.text.Text')

    @pytest.fixture
    def text_prop_fixture(self, Text_):
        r = (
            an_r().with_nsdecls().with_child(
                a_t().with_text('foo')).with_child(
                a_t().with_text('bar'))
        ).element
        run = Run(r)
        return run, 'foobar'
