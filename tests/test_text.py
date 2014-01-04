# encoding: utf-8

"""
Test suite for the docx.text module
"""

from __future__ import absolute_import, print_function, unicode_literals

from docx.enum.text import WD_BREAK
from docx.oxml.text import CT_P
from docx.text import Paragraph, Run

import pytest

from mock import call, create_autospec, Mock

from .oxml.unitdata.text import a_b, a_br, a_t, a_p, an_r, an_rPr
from .unitutil import class_mock


class DescribeParagraph(object):

    @pytest.fixture
    def Run_(self, request):
        return class_mock(request, 'docx.text.Run')

    def it_has_a_sequence_of_the_runs_it_contains(self, Run_):
        p_elm = Mock(name='p_elm')
        r1, r2 = (Mock(name='r1'), Mock(name='r2'))
        R1, R2 = (Mock(name='Run1'), Mock(name='Run2'))
        p_elm.r_lst = [r1, r2]
        p = Paragraph(p_elm)
        Run_.side_effect = [R1, R2]
        # exercise ---------------------
        runs = p.runs
        # verify -----------------------
        assert Run_.mock_calls == [call(r1), call(r2)]
        assert runs == [R1, R2]

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

    def it_knows_if_its_bold(self, bold_fixture):
        run, is_bold = bold_fixture
        print('\n%s' % run._r.xml)
        assert run.bold == is_bold

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

    @pytest.fixture
    def add_text_fixture(self, run, Text_):
        text_str = 'foobar'
        expected_xml = (
            an_r().with_nsdecls().with_child(
                a_t().with_text(text_str))
        ).xml()
        return run, text_str, expected_xml, Text_

    @pytest.fixture(params=[True, False, None])
    def bold_fixture(self, request):
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
