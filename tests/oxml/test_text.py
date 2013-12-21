# encoding: utf-8

"""
Test suite for the docx.oxml.text module.
"""

from docx.oxml.text import CT_P, CT_PPr, CT_R, CT_Text

from .unitdata.text import a_p, a_pPr, a_pStyle, a_t, an_r


class DescribeCT_P(object):

    def it_can_construct_a_new_p_element(self):
        p = CT_P.new()
        expected_xml = a_p().with_nsdecls().xml()
        assert p.xml == expected_xml

    def it_has_a_sequence_of_the_runs_it_contains(self):
        p = a_p().with_nsdecls().with_child(an_r()).with_child(an_r()).element
        assert len(p.r_lst) == 2
        for r in p.r_lst:
            assert isinstance(r, CT_R)

    def it_can_add_an_r_to_itself(self):
        p = a_p().with_nsdecls().element
        # exercise -----------------
        r = p.add_r()
        # verify -------------------
        assert p.xml == a_p().with_nsdecls().with_child(an_r()).xml()
        assert isinstance(r, CT_R)

    def it_knows_its_paragraph_style(self):
        pPr_bldr = a_pPr().with_child(a_pStyle().with_val('foobar'))
        cases = (
            (a_p(), None),
            (a_p().with_child(pPr_bldr), 'foobar'),
        )
        for builder, expected_value in cases:
            p = builder.with_nsdecls().element
            assert p.style == expected_value

    def it_can_set_its_paragraph_style(self):
        pPr = a_pPr().with_child(a_pStyle().with_val('foobar'))
        pPr2 = a_pPr().with_child(a_pStyle().with_val('barfoo'))
        cases = (
            (1, a_p(), None, a_p().with_child(a_pPr())),
            (2, a_p(), 'foobar', a_p().with_child(pPr)),
            (3, a_p().with_child(pPr), None, a_p().with_child(a_pPr())),
            (4, a_p().with_child(pPr), 'barfoo', a_p().with_child(pPr2)),
        )
        for case_nmbr, before_bldr, new_style, after_bldr in cases:
            p = before_bldr.with_nsdecls().element
            p.style = new_style
            expected_xml = after_bldr.with_nsdecls().xml()
            assert p.xml == expected_xml


class DescribeCT_PPr(object):

    def it_can_construct_a_new_pPr_element(self):
        pPr = CT_PPr.new()
        expected_xml = a_pPr().with_nsdecls().xml()
        assert pPr.xml == expected_xml

    def it_knows_the_paragraph_style(self):
        cases = (
            (a_pPr(), None),
            (a_pPr().with_child(a_pStyle().with_val('foobar')), 'foobar'),
        )
        for builder, expected_value in cases:
            pPr = builder.with_nsdecls().element
            assert pPr.style == expected_value

    def it_can_set_the_paragraph_style(self):
        cases = (
            (1, a_pPr(), None, a_pPr()),
            (2, a_pPr(), 'foobar',
             a_pPr().with_child(a_pStyle().with_val('foobar'))),
            (3, a_pPr().with_child(a_pStyle().with_val('foobar')), None,
             a_pPr()),
            (4, a_pPr().with_child(a_pStyle().with_val('foobar')), 'barfoo',
             a_pPr().with_child(a_pStyle().with_val('barfoo'))),
        )
        for case_nmbr, before_bldr, new_style, after_bldr in cases:
            pPr = before_bldr.with_nsdecls().element
            pPr.style = new_style
            expected_xml = after_bldr.with_nsdecls().xml()
            assert pPr.xml == expected_xml


class DescribeCT_R(object):

    def it_can_construct_a_new_r_element(self):
        r = CT_R.new()
        assert r.xml == an_r().with_nsdecls().xml()

    def it_can_add_a_t_to_itself(self):
        text = 'foobar'
        r = an_r().with_nsdecls().element
        # exercise -----------------
        t = r.add_t(text)
        # verify -------------------
        assert (
            r.xml ==
            an_r().with_nsdecls().with_child(a_t().with_text(text)).xml()
        )
        assert isinstance(t, CT_Text)

    def it_has_a_sequence_of_the_t_elms_it_contains(self):
        cases = (
            (an_r().with_nsdecls(), 0),
            (an_r().with_nsdecls().with_child(
                a_t().with_text('foo')), 1),
            (an_r().with_nsdecls().with_child(
                a_t().with_text('foo')).with_child(
                a_t().with_text('bar')), 2),
        )
        for r_bldr, expected_len in cases:
            r = r_bldr.element
            assert len(r.t_lst) == expected_len
            for t in r.t_lst:
                assert isinstance(t, CT_Text)


class DescribeCT_Text(object):

    def it_can_construct_a_new_t_element(self):
        text = 'foobar'
        t = CT_Text.new(text)
        assert t.xml == a_t().with_nsdecls().with_text(text).xml()
