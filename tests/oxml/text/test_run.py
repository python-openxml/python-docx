# encoding: utf-8

"""
Test suite for the docx.oxml.text.run module.
"""

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)
import pytest
from ...unitutil.cxml import element, xml


class DescribeCT_R(object):
    def it_can_add_a_t_preserving_edge_whitespace(self, add_t_fixture):
        r, text, expected_xml = add_t_fixture
        r.add_t(text)
        assert r.xml == expected_xml

    # fixtures -------------------------------------------------------

    @pytest.fixture(params=[
        ('w:r', 'foobar', 'w:r/w:t"foobar"'),
        ('w:r', 'foobar ', 'w:r/w:t{xml:space=preserve}"foobar "'),
        ('w:r/(w:rPr/w:rStyle{w:val=emphasis}, w:cr)', 'foobar',
         'w:r/(w:rPr/w:rStyle{w:val=emphasis}, w:cr, w:t"foobar")'),
    ])
    def add_t_fixture(self, request):
        initial_cxml, text, expected_cxml = request.param
        r = element(initial_cxml)
        expected_xml = xml(expected_cxml)
        return r, text, expected_xml


class DescribeCT_RPr(object):
    def it_can_add_a_b(self, add_b_fixture):
        rPr, expected_xml = add_b_fixture
        rPr._add_b()
        assert rPr.xml == expected_xml

    def it_can_add_a_bCs(self, add_bCs_fixture):
        rPr, expected_xml = add_bCs_fixture
        rPr._add_bCs()
        assert rPr.xml == expected_xml

    def it_can_add_a_bdr(self, add_bdr_fixture):
        rPr, expected_xml = add_bdr_fixture
        rPr._add_bdr()
        assert rPr.xml == expected_xml

    def it_can_add_a_caps(self, add_caps_fixture):
        rPr, expected_xml = add_caps_fixture
        rPr._add_caps()
        assert rPr.xml == expected_xml

    def it_can_add_a_color(self, add_color_fixture):
        rPr, expected_xml = add_color_fixture
        rPr._add_color()
        assert rPr.xml == expected_xml

    def it_can_add_a_cs(self, add_cs_fixture):
        rPr, expected_xml = add_cs_fixture
        rPr._add_cs()
        assert rPr.xml == expected_xml

    def it_can_add_a_dstrike(self, add_dstrike_fixture):
        rPr, expected_xml = add_dstrike_fixture
        rPr._add_dstrike()
        assert rPr.xml == expected_xml

    def it_can_add_a_eastAsianLayout(self, add_eastAsianLayout_fixture):
        rPr, expected_xml = add_eastAsianLayout_fixture
        rPr._add_eastAsianLayout()
        assert rPr.xml == expected_xml

    def it_can_add_a_effect(self, add_effect_fixture):
        rPr, expected_xml = add_effect_fixture
        rPr._add_effect()
        assert rPr.xml == expected_xml

    def it_can_add_a_em(self, add_em_fixture):
        rPr, expected_xml = add_em_fixture
        rPr._add_em()
        assert rPr.xml == expected_xml

    def it_can_add_a_emboss(self, add_emboss_fixture):
        rPr, expected_xml = add_emboss_fixture
        rPr._add_emboss()
        assert rPr.xml == expected_xml

    def it_can_add_a_fitText(self, add_fitText_fixture):
        rPr, expected_xml = add_fitText_fixture
        rPr._add_fitText()
        assert rPr.xml == expected_xml

    def it_can_add_a_highlight(self, add_highlight_fixture):
        rPr, expected_xml = add_highlight_fixture
        rPr._add_highlight()
        assert rPr.xml == expected_xml

    def it_can_add_a_i(self, add_i_fixture):
        rPr, expected_xml = add_i_fixture
        rPr._add_i()
        assert rPr.xml == expected_xml

    def it_can_add_a_iCs(self, add_iCs_fixture):
        rPr, expected_xml = add_iCs_fixture
        rPr._add_iCs()
        assert rPr.xml == expected_xml

    def it_can_add_a_imprint(self, add_imprint_fixture):
        rPr, expected_xml = add_imprint_fixture
        rPr._add_imprint()
        assert rPr.xml == expected_xml

    def it_can_add_a_kern(self, add_kern_fixture):
        rPr, expected_xml = add_kern_fixture
        rPr._add_kern()
        assert rPr.xml == expected_xml

    def it_can_add_a_lang(self, add_lang_fixture):
        rPr, expected_xml = add_lang_fixture
        rPr._add_lang()
        assert rPr.xml == expected_xml

    def it_can_add_a_noProof(self, add_noProof_fixture):
        rPr, expected_xml = add_noProof_fixture
        rPr._add_noProof()
        assert rPr.xml == expected_xml

    def it_can_add_a_oMath(self, add_oMath_fixture):
        rPr, expected_xml = add_oMath_fixture
        rPr._add_oMath()
        assert rPr.xml == expected_xml

    def it_can_add_a_outline(self, add_outline_fixture):
        rPr, expected_xml = add_outline_fixture
        rPr._add_outline()
        assert rPr.xml == expected_xml

    def it_can_add_a_position(self, add_position_fixture):
        rPr, expected_xml = add_position_fixture
        rPr._add_position()
        assert rPr.xml == expected_xml

    def it_can_add_a_rFonts(self, add_rFonts_fixture):
        rPr, expected_xml = add_rFonts_fixture
        rPr._add_rFonts()
        assert rPr.xml == expected_xml

    def it_can_add_a_rPrChange(self, add_rPrChange_fixture):
        rPr, expected_xml = add_rPrChange_fixture
        rPr._add_rPrChange()
        assert rPr.xml == expected_xml

    def it_can_add_a_rStyle(self, add_rStyle_fixture):
        rPr, expected_xml = add_rStyle_fixture
        rPr._add_rStyle()
        assert rPr.xml == expected_xml

    def it_can_add_a_rtl(self, add_rtl_fixture):
        rPr, expected_xml = add_rtl_fixture
        rPr._add_rtl()
        assert rPr.xml == expected_xml

    def it_can_add_a_shadow(self, add_shadow_fixture):
        rPr, expected_xml = add_shadow_fixture
        rPr._add_shadow()
        assert rPr.xml == expected_xml

    def it_can_add_a_shd(self, add_shd_fixture):
        rPr, expected_xml = add_shd_fixture
        rPr._add_shd()
        assert rPr.xml == expected_xml

    def it_can_add_a_smallCaps(self, add_smallCaps_fixture):
        rPr, expected_xml = add_smallCaps_fixture
        rPr._add_smallCaps()
        assert rPr.xml == expected_xml

    def it_can_add_a_snapToGrid(self, add_snapToGrid_fixture):
        rPr, expected_xml = add_snapToGrid_fixture
        rPr._add_snapToGrid()
        assert rPr.xml == expected_xml

    def it_can_add_a_spacing(self, add_spacing_fixture):
        rPr, expected_xml = add_spacing_fixture
        rPr._add_spacing()
        assert rPr.xml == expected_xml

    def it_can_add_a_specVanish(self, add_specVanish_fixture):
        rPr, expected_xml = add_specVanish_fixture
        rPr._add_specVanish()
        assert rPr.xml == expected_xml

    def it_can_add_a_strike(self, add_strike_fixture):
        rPr, expected_xml = add_strike_fixture
        rPr._add_strike()
        assert rPr.xml == expected_xml

    def it_can_add_a_sz(self, add_sz_fixture):
        rPr, expected_xml = add_sz_fixture
        rPr._add_sz()
        assert rPr.xml == expected_xml

    def it_can_add_a_szCs(self, add_szCs_fixture):
        rPr, expected_xml = add_szCs_fixture
        rPr._add_szCs()
        assert rPr.xml == expected_xml

    def it_can_add_a_u(self, add_u_fixture):
        rPr, expected_xml = add_u_fixture
        rPr._add_u()
        assert rPr.xml == expected_xml

    def it_can_add_a_vanish(self, add_vanish_fixture):
        rPr, expected_xml = add_vanish_fixture
        rPr._add_vanish()
        assert rPr.xml == expected_xml

    def it_can_add_a_vertAlign(self, add_vertAlign_fixture):
        rPr, expected_xml = add_vertAlign_fixture
        rPr._add_vertAlign()
        assert rPr.xml == expected_xml

    def it_can_add_a_w(self, add_w_fixture):
        rPr, expected_xml = add_w_fixture
        rPr._add_w()
        assert rPr.xml == expected_xml

    def it_can_add_a_webHidden(self, add_webHidden_fixture):
        rPr, expected_xml = add_webHidden_fixture
        rPr._add_webHidden()
        assert rPr.xml == expected_xml

    # fixtures -------------------------------------------------------
    def add_x_fixture(self, request):
        rPr_cxml, expected_cxml = request.param
        rPr = element(rPr_cxml)
        expected_xml = xml(expected_cxml)
        return rPr, expected_xml

    @pytest.fixture(params=[
        ('w:rPr/w:rFonts', 'w:rPr/(w:rStyle,w:rFonts)'),
        ('w:rPr/w:b', 'w:rPr/(w:rStyle,w:b)'),
        ('w:rPr/w:bCs', 'w:rPr/(w:rStyle,w:bCs)'),
        ('w:rPr/w:i', 'w:rPr/(w:rStyle,w:i)'),
        ('w:rPr/w:iCs', 'w:rPr/(w:rStyle,w:iCs)'),
        ('w:rPr/w:caps', 'w:rPr/(w:rStyle,w:caps)'),
        ('w:rPr/w:smallCaps', 'w:rPr/(w:rStyle,w:smallCaps)'),
        ('w:rPr/w:strike', 'w:rPr/(w:rStyle,w:strike)'),
        ('w:rPr/w:dstrike', 'w:rPr/(w:rStyle,w:dstrike)'),
        ('w:rPr/w:outline', 'w:rPr/(w:rStyle,w:outline)'),
        ('w:rPr/w:shadow', 'w:rPr/(w:rStyle,w:shadow)'),
        ('w:rPr/w:emboss', 'w:rPr/(w:rStyle,w:emboss)'),
        ('w:rPr/w:imprint', 'w:rPr/(w:rStyle,w:imprint)'),
        ('w:rPr/w:noProof', 'w:rPr/(w:rStyle,w:noProof)'),
        ('w:rPr/w:snapToGrid', 'w:rPr/(w:rStyle,w:snapToGrid)'),
        ('w:rPr/w:vanish', 'w:rPr/(w:rStyle,w:vanish)'),
        ('w:rPr/w:webHidden', 'w:rPr/(w:rStyle,w:webHidden)'),
        ('w:rPr/w:color', 'w:rPr/(w:rStyle,w:color)'),
        ('w:rPr/w:spacing', 'w:rPr/(w:rStyle,w:spacing)'),
        ('w:rPr/w:w', 'w:rPr/(w:rStyle,w:w)'),
        ('w:rPr/w:kern', 'w:rPr/(w:rStyle,w:kern)'),
        ('w:rPr/w:position', 'w:rPr/(w:rStyle,w:position)'),
        ('w:rPr/w:sz', 'w:rPr/(w:rStyle,w:sz)'),
        ('w:rPr/w:szCs', 'w:rPr/(w:rStyle,w:szCs)'),
        ('w:rPr/w:highlight', 'w:rPr/(w:rStyle,w:highlight)'),
        ('w:rPr/w:u', 'w:rPr/(w:rStyle,w:u)'),
        ('w:rPr/w:effect', 'w:rPr/(w:rStyle,w:effect)'),
        ('w:rPr/w:bdr', 'w:rPr/(w:rStyle,w:bdr)'),
        ('w:rPr/w:shd', 'w:rPr/(w:rStyle,w:shd)'),
        ('w:rPr/w:fitText', 'w:rPr/(w:rStyle,w:fitText)'),
        ('w:rPr/w:vertAlign', 'w:rPr/(w:rStyle,w:vertAlign)'),
        ('w:rPr/w:rtl', 'w:rPr/(w:rStyle,w:rtl)'),
        ('w:rPr/w:cs', 'w:rPr/(w:rStyle,w:cs)'),
        ('w:rPr/w:em', 'w:rPr/(w:rStyle,w:em)'),
        ('w:rPr/w:lang', 'w:rPr/(w:rStyle,w:lang)'),
        ('w:rPr/w:eastAsianLayout', 'w:rPr/(w:rStyle,w:eastAsianLayout)'),
        ('w:rPr/w:specVanish', 'w:rPr/(w:rStyle,w:specVanish)'),
        ('w:rPr/w:oMath', 'w:rPr/(w:rStyle,w:oMath)'),
        ('w:rPr/w:rPrChange', 'w:rPr/(w:rStyle,w:rPrChange)')
    ])
    def add_rStyle_fixture(self, request):
        return self.add_x_fixture(request)

    @pytest.fixture(params=[
        ('w:rPr/w:rStyle', 'w:rPr/(w:rStyle,w:rFonts)'),
        ('w:rPr/w:b', 'w:rPr/(w:rFonts,w:b)'),
        ('w:rPr/w:bCs', 'w:rPr/(w:rFonts,w:bCs)'),
        ('w:rPr/w:i', 'w:rPr/(w:rFonts,w:i)'),
        ('w:rPr/w:iCs', 'w:rPr/(w:rFonts,w:iCs)'),
        ('w:rPr/w:caps', 'w:rPr/(w:rFonts,w:caps)'),
        ('w:rPr/w:smallCaps', 'w:rPr/(w:rFonts,w:smallCaps)'),
        ('w:rPr/w:strike', 'w:rPr/(w:rFonts,w:strike)'),
        ('w:rPr/w:dstrike', 'w:rPr/(w:rFonts,w:dstrike)'),
        ('w:rPr/w:outline', 'w:rPr/(w:rFonts,w:outline)'),
        ('w:rPr/w:shadow', 'w:rPr/(w:rFonts,w:shadow)'),
        ('w:rPr/w:emboss', 'w:rPr/(w:rFonts,w:emboss)'),
        ('w:rPr/w:imprint', 'w:rPr/(w:rFonts,w:imprint)'),
        ('w:rPr/w:noProof', 'w:rPr/(w:rFonts,w:noProof)'),
        ('w:rPr/w:snapToGrid', 'w:rPr/(w:rFonts,w:snapToGrid)'),
        ('w:rPr/w:vanish', 'w:rPr/(w:rFonts,w:vanish)'),
        ('w:rPr/w:webHidden', 'w:rPr/(w:rFonts,w:webHidden)'),
        ('w:rPr/w:color', 'w:rPr/(w:rFonts,w:color)'),
        ('w:rPr/w:spacing', 'w:rPr/(w:rFonts,w:spacing)'),
        ('w:rPr/w:w', 'w:rPr/(w:rFonts,w:w)'),
        ('w:rPr/w:kern', 'w:rPr/(w:rFonts,w:kern)'),
        ('w:rPr/w:position', 'w:rPr/(w:rFonts,w:position)'),
        ('w:rPr/w:sz', 'w:rPr/(w:rFonts,w:sz)'),
        ('w:rPr/w:szCs', 'w:rPr/(w:rFonts,w:szCs)'),
        ('w:rPr/w:highlight', 'w:rPr/(w:rFonts,w:highlight)'),
        ('w:rPr/w:u', 'w:rPr/(w:rFonts,w:u)'),
        ('w:rPr/w:effect', 'w:rPr/(w:rFonts,w:effect)'),
        ('w:rPr/w:bdr', 'w:rPr/(w:rFonts,w:bdr)'),
        ('w:rPr/w:shd', 'w:rPr/(w:rFonts,w:shd)'),
        ('w:rPr/w:fitText', 'w:rPr/(w:rFonts,w:fitText)'),
        ('w:rPr/w:vertAlign', 'w:rPr/(w:rFonts,w:vertAlign)'),
        ('w:rPr/w:rtl', 'w:rPr/(w:rFonts,w:rtl)'),
        ('w:rPr/w:cs', 'w:rPr/(w:rFonts,w:cs)'),
        ('w:rPr/w:em', 'w:rPr/(w:rFonts,w:em)'),
        ('w:rPr/w:lang', 'w:rPr/(w:rFonts,w:lang)'),
        ('w:rPr/w:eastAsianLayout', 'w:rPr/(w:rFonts,w:eastAsianLayout)'),
        ('w:rPr/w:specVanish', 'w:rPr/(w:rFonts,w:specVanish)'),
        ('w:rPr/w:oMath', 'w:rPr/(w:rFonts,w:oMath)'),
        ('w:rPr/w:rPrChange', 'w:rPr/(w:rFonts,w:rPrChange)')
    ])
    def add_rFonts_fixture(self, request):
        return self.add_x_fixture(request)

    @pytest.fixture(params=[
        ('w:rPr/w:rStyle', 'w:rPr/(w:rStyle,w:b)'),
        ('w:rPr/w:rFonts', 'w:rPr/(w:rFonts,w:b)'),
        ('w:rPr/w:bCs', 'w:rPr/(w:b,w:bCs)'),
        ('w:rPr/w:i', 'w:rPr/(w:b,w:i)'),
        ('w:rPr/w:iCs', 'w:rPr/(w:b,w:iCs)'),
        ('w:rPr/w:caps', 'w:rPr/(w:b,w:caps)'),
        ('w:rPr/w:smallCaps', 'w:rPr/(w:b,w:smallCaps)'),
        ('w:rPr/w:strike', 'w:rPr/(w:b,w:strike)'),
        ('w:rPr/w:dstrike', 'w:rPr/(w:b,w:dstrike)'),
        ('w:rPr/w:outline', 'w:rPr/(w:b,w:outline)'),
        ('w:rPr/w:shadow', 'w:rPr/(w:b,w:shadow)'),
        ('w:rPr/w:emboss', 'w:rPr/(w:b,w:emboss)'),
        ('w:rPr/w:imprint', 'w:rPr/(w:b,w:imprint)'),
        ('w:rPr/w:noProof', 'w:rPr/(w:b,w:noProof)'),
        ('w:rPr/w:snapToGrid', 'w:rPr/(w:b,w:snapToGrid)'),
        ('w:rPr/w:vanish', 'w:rPr/(w:b,w:vanish)'),
        ('w:rPr/w:webHidden', 'w:rPr/(w:b,w:webHidden)'),
        ('w:rPr/w:color', 'w:rPr/(w:b,w:color)'),
        ('w:rPr/w:spacing', 'w:rPr/(w:b,w:spacing)'),
        ('w:rPr/w:w', 'w:rPr/(w:b,w:w)'),
        ('w:rPr/w:kern', 'w:rPr/(w:b,w:kern)'),
        ('w:rPr/w:position', 'w:rPr/(w:b,w:position)'),
        ('w:rPr/w:sz', 'w:rPr/(w:b,w:sz)'),
        ('w:rPr/w:szCs', 'w:rPr/(w:b,w:szCs)'),
        ('w:rPr/w:highlight', 'w:rPr/(w:b,w:highlight)'),
        ('w:rPr/w:u', 'w:rPr/(w:b,w:u)'),
        ('w:rPr/w:effect', 'w:rPr/(w:b,w:effect)'),
        ('w:rPr/w:bdr', 'w:rPr/(w:b,w:bdr)'),
        ('w:rPr/w:shd', 'w:rPr/(w:b,w:shd)'),
        ('w:rPr/w:fitText', 'w:rPr/(w:b,w:fitText)'),
        ('w:rPr/w:vertAlign', 'w:rPr/(w:b,w:vertAlign)'),
        ('w:rPr/w:rtl', 'w:rPr/(w:b,w:rtl)'),
        ('w:rPr/w:cs', 'w:rPr/(w:b,w:cs)'),
        ('w:rPr/w:em', 'w:rPr/(w:b,w:em)'),
        ('w:rPr/w:lang', 'w:rPr/(w:b,w:lang)'),
        ('w:rPr/w:eastAsianLayout', 'w:rPr/(w:b,w:eastAsianLayout)'),
        ('w:rPr/w:specVanish', 'w:rPr/(w:b,w:specVanish)'),
        ('w:rPr/w:oMath', 'w:rPr/(w:b,w:oMath)'),
        ('w:rPr/w:rPrChange', 'w:rPr/(w:b,w:rPrChange)')
    ])
    def add_b_fixture(self, request):
        return self.add_x_fixture(request)

    @pytest.fixture(params=[
        ('w:rPr/w:rStyle', 'w:rPr/(w:rStyle,w:bCs)'),
        ('w:rPr/w:rFonts', 'w:rPr/(w:rFonts,w:bCs)'),
        ('w:rPr/w:b', 'w:rPr/(w:b,w:bCs)'),
        ('w:rPr/w:i', 'w:rPr/(w:bCs,w:i)'),
        ('w:rPr/w:iCs', 'w:rPr/(w:bCs,w:iCs)'),
        ('w:rPr/w:caps', 'w:rPr/(w:bCs,w:caps)'),
        ('w:rPr/w:smallCaps', 'w:rPr/(w:bCs,w:smallCaps)'),
        ('w:rPr/w:strike', 'w:rPr/(w:bCs,w:strike)'),
        ('w:rPr/w:dstrike', 'w:rPr/(w:bCs,w:dstrike)'),
        ('w:rPr/w:outline', 'w:rPr/(w:bCs,w:outline)'),
        ('w:rPr/w:shadow', 'w:rPr/(w:bCs,w:shadow)'),
        ('w:rPr/w:emboss', 'w:rPr/(w:bCs,w:emboss)'),
        ('w:rPr/w:imprint', 'w:rPr/(w:bCs,w:imprint)'),
        ('w:rPr/w:noProof', 'w:rPr/(w:bCs,w:noProof)'),
        ('w:rPr/w:snapToGrid', 'w:rPr/(w:bCs,w:snapToGrid)'),
        ('w:rPr/w:vanish', 'w:rPr/(w:bCs,w:vanish)'),
        ('w:rPr/w:webHidden', 'w:rPr/(w:bCs,w:webHidden)'),
        ('w:rPr/w:color', 'w:rPr/(w:bCs,w:color)'),
        ('w:rPr/w:spacing', 'w:rPr/(w:bCs,w:spacing)'),
        ('w:rPr/w:w', 'w:rPr/(w:bCs,w:w)'),
        ('w:rPr/w:kern', 'w:rPr/(w:bCs,w:kern)'),
        ('w:rPr/w:position', 'w:rPr/(w:bCs,w:position)'),
        ('w:rPr/w:sz', 'w:rPr/(w:bCs,w:sz)'),
        ('w:rPr/w:szCs', 'w:rPr/(w:bCs,w:szCs)'),
        ('w:rPr/w:highlight', 'w:rPr/(w:bCs,w:highlight)'),
        ('w:rPr/w:u', 'w:rPr/(w:bCs,w:u)'),
        ('w:rPr/w:effect', 'w:rPr/(w:bCs,w:effect)'),
        ('w:rPr/w:bdr', 'w:rPr/(w:bCs,w:bdr)'),
        ('w:rPr/w:shd', 'w:rPr/(w:bCs,w:shd)'),
        ('w:rPr/w:fitText', 'w:rPr/(w:bCs,w:fitText)'),
        ('w:rPr/w:vertAlign', 'w:rPr/(w:bCs,w:vertAlign)'),
        ('w:rPr/w:rtl', 'w:rPr/(w:bCs,w:rtl)'),
        ('w:rPr/w:cs', 'w:rPr/(w:bCs,w:cs)'),
        ('w:rPr/w:em', 'w:rPr/(w:bCs,w:em)'),
        ('w:rPr/w:lang', 'w:rPr/(w:bCs,w:lang)'),
        ('w:rPr/w:eastAsianLayout', 'w:rPr/(w:bCs,w:eastAsianLayout)'),
        ('w:rPr/w:specVanish', 'w:rPr/(w:bCs,w:specVanish)'),
        ('w:rPr/w:oMath', 'w:rPr/(w:bCs,w:oMath)'),
        ('w:rPr/w:rPrChange', 'w:rPr/(w:bCs,w:rPrChange)')
    ])
    def add_bCs_fixture(self, request):
        return self.add_x_fixture(request)

    @pytest.fixture(params=[
        ('w:rPr/w:rStyle', 'w:rPr/(w:rStyle,w:i)'),
        ('w:rPr/w:rFonts', 'w:rPr/(w:rFonts,w:i)'),
        ('w:rPr/w:b', 'w:rPr/(w:b,w:i)'),
        ('w:rPr/w:bCs', 'w:rPr/(w:bCs,w:i)'),
        ('w:rPr/w:iCs', 'w:rPr/(w:i,w:iCs)'),
        ('w:rPr/w:caps', 'w:rPr/(w:i,w:caps)'),
        ('w:rPr/w:smallCaps', 'w:rPr/(w:i,w:smallCaps)'),
        ('w:rPr/w:strike', 'w:rPr/(w:i,w:strike)'),
        ('w:rPr/w:dstrike', 'w:rPr/(w:i,w:dstrike)'),
        ('w:rPr/w:outline', 'w:rPr/(w:i,w:outline)'),
        ('w:rPr/w:shadow', 'w:rPr/(w:i,w:shadow)'),
        ('w:rPr/w:emboss', 'w:rPr/(w:i,w:emboss)'),
        ('w:rPr/w:imprint', 'w:rPr/(w:i,w:imprint)'),
        ('w:rPr/w:noProof', 'w:rPr/(w:i,w:noProof)'),
        ('w:rPr/w:snapToGrid', 'w:rPr/(w:i,w:snapToGrid)'),
        ('w:rPr/w:vanish', 'w:rPr/(w:i,w:vanish)'),
        ('w:rPr/w:webHidden', 'w:rPr/(w:i,w:webHidden)'),
        ('w:rPr/w:color', 'w:rPr/(w:i,w:color)'),
        ('w:rPr/w:spacing', 'w:rPr/(w:i,w:spacing)'),
        ('w:rPr/w:w', 'w:rPr/(w:i,w:w)'),
        ('w:rPr/w:kern', 'w:rPr/(w:i,w:kern)'),
        ('w:rPr/w:position', 'w:rPr/(w:i,w:position)'),
        ('w:rPr/w:sz', 'w:rPr/(w:i,w:sz)'),
        ('w:rPr/w:szCs', 'w:rPr/(w:i,w:szCs)'),
        ('w:rPr/w:highlight', 'w:rPr/(w:i,w:highlight)'),
        ('w:rPr/w:u', 'w:rPr/(w:i,w:u)'),
        ('w:rPr/w:effect', 'w:rPr/(w:i,w:effect)'),
        ('w:rPr/w:bdr', 'w:rPr/(w:i,w:bdr)'),
        ('w:rPr/w:shd', 'w:rPr/(w:i,w:shd)'),
        ('w:rPr/w:fitText', 'w:rPr/(w:i,w:fitText)'),
        ('w:rPr/w:vertAlign', 'w:rPr/(w:i,w:vertAlign)'),
        ('w:rPr/w:rtl', 'w:rPr/(w:i,w:rtl)'),
        ('w:rPr/w:cs', 'w:rPr/(w:i,w:cs)'),
        ('w:rPr/w:em', 'w:rPr/(w:i,w:em)'),
        ('w:rPr/w:lang', 'w:rPr/(w:i,w:lang)'),
        ('w:rPr/w:eastAsianLayout', 'w:rPr/(w:i,w:eastAsianLayout)'),
        ('w:rPr/w:specVanish', 'w:rPr/(w:i,w:specVanish)'),
        ('w:rPr/w:oMath', 'w:rPr/(w:i,w:oMath)'),
        ('w:rPr/w:rPrChange', 'w:rPr/(w:i,w:rPrChange)')
    ])
    def add_i_fixture(self, request):
        return self.add_x_fixture(request)

    @pytest.fixture(params=[
        ('w:rPr/w:rStyle', 'w:rPr/(w:rStyle,w:iCs)'),
        ('w:rPr/w:rFonts', 'w:rPr/(w:rFonts,w:iCs)'),
        ('w:rPr/w:b', 'w:rPr/(w:b,w:iCs)'),
        ('w:rPr/w:bCs', 'w:rPr/(w:bCs,w:iCs)'),
        ('w:rPr/w:i', 'w:rPr/(w:i,w:iCs)'),
        ('w:rPr/w:caps', 'w:rPr/(w:iCs,w:caps)'),
        ('w:rPr/w:smallCaps', 'w:rPr/(w:iCs,w:smallCaps)'),
        ('w:rPr/w:strike', 'w:rPr/(w:iCs,w:strike)'),
        ('w:rPr/w:dstrike', 'w:rPr/(w:iCs,w:dstrike)'),
        ('w:rPr/w:outline', 'w:rPr/(w:iCs,w:outline)'),
        ('w:rPr/w:shadow', 'w:rPr/(w:iCs,w:shadow)'),
        ('w:rPr/w:emboss', 'w:rPr/(w:iCs,w:emboss)'),
        ('w:rPr/w:imprint', 'w:rPr/(w:iCs,w:imprint)'),
        ('w:rPr/w:noProof', 'w:rPr/(w:iCs,w:noProof)'),
        ('w:rPr/w:snapToGrid', 'w:rPr/(w:iCs,w:snapToGrid)'),
        ('w:rPr/w:vanish', 'w:rPr/(w:iCs,w:vanish)'),
        ('w:rPr/w:webHidden', 'w:rPr/(w:iCs,w:webHidden)'),
        ('w:rPr/w:color', 'w:rPr/(w:iCs,w:color)'),
        ('w:rPr/w:spacing', 'w:rPr/(w:iCs,w:spacing)'),
        ('w:rPr/w:w', 'w:rPr/(w:iCs,w:w)'),
        ('w:rPr/w:kern', 'w:rPr/(w:iCs,w:kern)'),
        ('w:rPr/w:position', 'w:rPr/(w:iCs,w:position)'),
        ('w:rPr/w:sz', 'w:rPr/(w:iCs,w:sz)'),
        ('w:rPr/w:szCs', 'w:rPr/(w:iCs,w:szCs)'),
        ('w:rPr/w:highlight', 'w:rPr/(w:iCs,w:highlight)'),
        ('w:rPr/w:u', 'w:rPr/(w:iCs,w:u)'),
        ('w:rPr/w:effect', 'w:rPr/(w:iCs,w:effect)'),
        ('w:rPr/w:bdr', 'w:rPr/(w:iCs,w:bdr)'),
        ('w:rPr/w:shd', 'w:rPr/(w:iCs,w:shd)'),
        ('w:rPr/w:fitText', 'w:rPr/(w:iCs,w:fitText)'),
        ('w:rPr/w:vertAlign', 'w:rPr/(w:iCs,w:vertAlign)'),
        ('w:rPr/w:rtl', 'w:rPr/(w:iCs,w:rtl)'),
        ('w:rPr/w:cs', 'w:rPr/(w:iCs,w:cs)'),
        ('w:rPr/w:em', 'w:rPr/(w:iCs,w:em)'),
        ('w:rPr/w:lang', 'w:rPr/(w:iCs,w:lang)'),
        ('w:rPr/w:eastAsianLayout', 'w:rPr/(w:iCs,w:eastAsianLayout)'),
        ('w:rPr/w:specVanish', 'w:rPr/(w:iCs,w:specVanish)'),
        ('w:rPr/w:oMath', 'w:rPr/(w:iCs,w:oMath)'),
        ('w:rPr/w:rPrChange', 'w:rPr/(w:iCs,w:rPrChange)')
    ])
    def add_iCs_fixture(self, request):
        return self.add_x_fixture(request)

    @pytest.fixture(params=[
        ('w:rPr/w:rStyle', 'w:rPr/(w:rStyle,w:caps)'),
        ('w:rPr/w:rFonts', 'w:rPr/(w:rFonts,w:caps)'),
        ('w:rPr/w:b', 'w:rPr/(w:b,w:caps)'),
        ('w:rPr/w:bCs', 'w:rPr/(w:bCs,w:caps)'),
        ('w:rPr/w:i', 'w:rPr/(w:i,w:caps)'),
        ('w:rPr/w:iCs', 'w:rPr/(w:iCs,w:caps)'),
        ('w:rPr/w:smallCaps', 'w:rPr/(w:caps,w:smallCaps)'),
        ('w:rPr/w:strike', 'w:rPr/(w:caps,w:strike)'),
        ('w:rPr/w:dstrike', 'w:rPr/(w:caps,w:dstrike)'),
        ('w:rPr/w:outline', 'w:rPr/(w:caps,w:outline)'),
        ('w:rPr/w:shadow', 'w:rPr/(w:caps,w:shadow)'),
        ('w:rPr/w:emboss', 'w:rPr/(w:caps,w:emboss)'),
        ('w:rPr/w:imprint', 'w:rPr/(w:caps,w:imprint)'),
        ('w:rPr/w:noProof', 'w:rPr/(w:caps,w:noProof)'),
        ('w:rPr/w:snapToGrid', 'w:rPr/(w:caps,w:snapToGrid)'),
        ('w:rPr/w:vanish', 'w:rPr/(w:caps,w:vanish)'),
        ('w:rPr/w:webHidden', 'w:rPr/(w:caps,w:webHidden)'),
        ('w:rPr/w:color', 'w:rPr/(w:caps,w:color)'),
        ('w:rPr/w:spacing', 'w:rPr/(w:caps,w:spacing)'),
        ('w:rPr/w:w', 'w:rPr/(w:caps,w:w)'),
        ('w:rPr/w:kern', 'w:rPr/(w:caps,w:kern)'),
        ('w:rPr/w:position', 'w:rPr/(w:caps,w:position)'),
        ('w:rPr/w:sz', 'w:rPr/(w:caps,w:sz)'),
        ('w:rPr/w:szCs', 'w:rPr/(w:caps,w:szCs)'),
        ('w:rPr/w:highlight', 'w:rPr/(w:caps,w:highlight)'),
        ('w:rPr/w:u', 'w:rPr/(w:caps,w:u)'),
        ('w:rPr/w:effect', 'w:rPr/(w:caps,w:effect)'),
        ('w:rPr/w:bdr', 'w:rPr/(w:caps,w:bdr)'),
        ('w:rPr/w:shd', 'w:rPr/(w:caps,w:shd)'),
        ('w:rPr/w:fitText', 'w:rPr/(w:caps,w:fitText)'),
        ('w:rPr/w:vertAlign', 'w:rPr/(w:caps,w:vertAlign)'),
        ('w:rPr/w:rtl', 'w:rPr/(w:caps,w:rtl)'),
        ('w:rPr/w:cs', 'w:rPr/(w:caps,w:cs)'),
        ('w:rPr/w:em', 'w:rPr/(w:caps,w:em)'),
        ('w:rPr/w:lang', 'w:rPr/(w:caps,w:lang)'),
        ('w:rPr/w:eastAsianLayout', 'w:rPr/(w:caps,w:eastAsianLayout)'),
        ('w:rPr/w:specVanish', 'w:rPr/(w:caps,w:specVanish)'),
        ('w:rPr/w:oMath', 'w:rPr/(w:caps,w:oMath)'),
        ('w:rPr/w:rPrChange', 'w:rPr/(w:caps,w:rPrChange)')
    ])
    def add_caps_fixture(self, request):
        return self.add_x_fixture(request)

    @pytest.fixture(params=[
        ('w:rPr/w:rStyle', 'w:rPr/(w:rStyle,w:smallCaps)'),
        ('w:rPr/w:rFonts', 'w:rPr/(w:rFonts,w:smallCaps)'),
        ('w:rPr/w:b', 'w:rPr/(w:b,w:smallCaps)'),
        ('w:rPr/w:bCs', 'w:rPr/(w:bCs,w:smallCaps)'),
        ('w:rPr/w:i', 'w:rPr/(w:i,w:smallCaps)'),
        ('w:rPr/w:iCs', 'w:rPr/(w:iCs,w:smallCaps)'),
        ('w:rPr/w:caps', 'w:rPr/(w:caps,w:smallCaps)'),
        ('w:rPr/w:strike', 'w:rPr/(w:smallCaps,w:strike)'),
        ('w:rPr/w:dstrike', 'w:rPr/(w:smallCaps,w:dstrike)'),
        ('w:rPr/w:outline', 'w:rPr/(w:smallCaps,w:outline)'),
        ('w:rPr/w:shadow', 'w:rPr/(w:smallCaps,w:shadow)'),
        ('w:rPr/w:emboss', 'w:rPr/(w:smallCaps,w:emboss)'),
        ('w:rPr/w:imprint', 'w:rPr/(w:smallCaps,w:imprint)'),
        ('w:rPr/w:noProof', 'w:rPr/(w:smallCaps,w:noProof)'),
        ('w:rPr/w:snapToGrid', 'w:rPr/(w:smallCaps,w:snapToGrid)'),
        ('w:rPr/w:vanish', 'w:rPr/(w:smallCaps,w:vanish)'),
        ('w:rPr/w:webHidden', 'w:rPr/(w:smallCaps,w:webHidden)'),
        ('w:rPr/w:color', 'w:rPr/(w:smallCaps,w:color)'),
        ('w:rPr/w:spacing', 'w:rPr/(w:smallCaps,w:spacing)'),
        ('w:rPr/w:w', 'w:rPr/(w:smallCaps,w:w)'),
        ('w:rPr/w:kern', 'w:rPr/(w:smallCaps,w:kern)'),
        ('w:rPr/w:position', 'w:rPr/(w:smallCaps,w:position)'),
        ('w:rPr/w:sz', 'w:rPr/(w:smallCaps,w:sz)'),
        ('w:rPr/w:szCs', 'w:rPr/(w:smallCaps,w:szCs)'),
        ('w:rPr/w:highlight', 'w:rPr/(w:smallCaps,w:highlight)'),
        ('w:rPr/w:u', 'w:rPr/(w:smallCaps,w:u)'),
        ('w:rPr/w:effect', 'w:rPr/(w:smallCaps,w:effect)'),
        ('w:rPr/w:bdr', 'w:rPr/(w:smallCaps,w:bdr)'),
        ('w:rPr/w:shd', 'w:rPr/(w:smallCaps,w:shd)'),
        ('w:rPr/w:fitText', 'w:rPr/(w:smallCaps,w:fitText)'),
        ('w:rPr/w:vertAlign', 'w:rPr/(w:smallCaps,w:vertAlign)'),
        ('w:rPr/w:rtl', 'w:rPr/(w:smallCaps,w:rtl)'),
        ('w:rPr/w:cs', 'w:rPr/(w:smallCaps,w:cs)'),
        ('w:rPr/w:em', 'w:rPr/(w:smallCaps,w:em)'),
        ('w:rPr/w:lang', 'w:rPr/(w:smallCaps,w:lang)'),
        ('w:rPr/w:eastAsianLayout', 'w:rPr/(w:smallCaps,w:eastAsianLayout)'),
        ('w:rPr/w:specVanish', 'w:rPr/(w:smallCaps,w:specVanish)'),
        ('w:rPr/w:oMath', 'w:rPr/(w:smallCaps,w:oMath)'),
        ('w:rPr/w:rPrChange', 'w:rPr/(w:smallCaps,w:rPrChange)')
    ])
    def add_smallCaps_fixture(self, request):
        return self.add_x_fixture(request)

    @pytest.fixture(params=[
        ('w:rPr/w:rStyle', 'w:rPr/(w:rStyle,w:strike)'),
        ('w:rPr/w:rFonts', 'w:rPr/(w:rFonts,w:strike)'),
        ('w:rPr/w:b', 'w:rPr/(w:b,w:strike)'),
        ('w:rPr/w:bCs', 'w:rPr/(w:bCs,w:strike)'),
        ('w:rPr/w:i', 'w:rPr/(w:i,w:strike)'),
        ('w:rPr/w:iCs', 'w:rPr/(w:iCs,w:strike)'),
        ('w:rPr/w:caps', 'w:rPr/(w:caps,w:strike)'),
        ('w:rPr/w:smallCaps', 'w:rPr/(w:smallCaps,w:strike)'),
        ('w:rPr/w:dstrike', 'w:rPr/(w:strike,w:dstrike)'),
        ('w:rPr/w:outline', 'w:rPr/(w:strike,w:outline)'),
        ('w:rPr/w:shadow', 'w:rPr/(w:strike,w:shadow)'),
        ('w:rPr/w:emboss', 'w:rPr/(w:strike,w:emboss)'),
        ('w:rPr/w:imprint', 'w:rPr/(w:strike,w:imprint)'),
        ('w:rPr/w:noProof', 'w:rPr/(w:strike,w:noProof)'),
        ('w:rPr/w:snapToGrid', 'w:rPr/(w:strike,w:snapToGrid)'),
        ('w:rPr/w:vanish', 'w:rPr/(w:strike,w:vanish)'),
        ('w:rPr/w:webHidden', 'w:rPr/(w:strike,w:webHidden)'),
        ('w:rPr/w:color', 'w:rPr/(w:strike,w:color)'),
        ('w:rPr/w:spacing', 'w:rPr/(w:strike,w:spacing)'),
        ('w:rPr/w:w', 'w:rPr/(w:strike,w:w)'),
        ('w:rPr/w:kern', 'w:rPr/(w:strike,w:kern)'),
        ('w:rPr/w:position', 'w:rPr/(w:strike,w:position)'),
        ('w:rPr/w:sz', 'w:rPr/(w:strike,w:sz)'),
        ('w:rPr/w:szCs', 'w:rPr/(w:strike,w:szCs)'),
        ('w:rPr/w:highlight', 'w:rPr/(w:strike,w:highlight)'),
        ('w:rPr/w:u', 'w:rPr/(w:strike,w:u)'),
        ('w:rPr/w:effect', 'w:rPr/(w:strike,w:effect)'),
        ('w:rPr/w:bdr', 'w:rPr/(w:strike,w:bdr)'),
        ('w:rPr/w:shd', 'w:rPr/(w:strike,w:shd)'),
        ('w:rPr/w:fitText', 'w:rPr/(w:strike,w:fitText)'),
        ('w:rPr/w:vertAlign', 'w:rPr/(w:strike,w:vertAlign)'),
        ('w:rPr/w:rtl', 'w:rPr/(w:strike,w:rtl)'),
        ('w:rPr/w:cs', 'w:rPr/(w:strike,w:cs)'),
        ('w:rPr/w:em', 'w:rPr/(w:strike,w:em)'),
        ('w:rPr/w:lang', 'w:rPr/(w:strike,w:lang)'),
        ('w:rPr/w:eastAsianLayout', 'w:rPr/(w:strike,w:eastAsianLayout)'),
        ('w:rPr/w:specVanish', 'w:rPr/(w:strike,w:specVanish)'),
        ('w:rPr/w:oMath', 'w:rPr/(w:strike,w:oMath)'),
        ('w:rPr/w:rPrChange', 'w:rPr/(w:strike,w:rPrChange)')
    ])
    def add_strike_fixture(self, request):
        return self.add_x_fixture(request)

    @pytest.fixture(params=[
        ('w:rPr/w:rStyle', 'w:rPr/(w:rStyle,w:dstrike)'),
        ('w:rPr/w:rFonts', 'w:rPr/(w:rFonts,w:dstrike)'),
        ('w:rPr/w:b', 'w:rPr/(w:b,w:dstrike)'),
        ('w:rPr/w:bCs', 'w:rPr/(w:bCs,w:dstrike)'),
        ('w:rPr/w:i', 'w:rPr/(w:i,w:dstrike)'),
        ('w:rPr/w:iCs', 'w:rPr/(w:iCs,w:dstrike)'),
        ('w:rPr/w:caps', 'w:rPr/(w:caps,w:dstrike)'),
        ('w:rPr/w:smallCaps', 'w:rPr/(w:smallCaps,w:dstrike)'),
        ('w:rPr/w:strike', 'w:rPr/(w:strike,w:dstrike)'),
        ('w:rPr/w:outline', 'w:rPr/(w:dstrike,w:outline)'),
        ('w:rPr/w:shadow', 'w:rPr/(w:dstrike,w:shadow)'),
        ('w:rPr/w:emboss', 'w:rPr/(w:dstrike,w:emboss)'),
        ('w:rPr/w:imprint', 'w:rPr/(w:dstrike,w:imprint)'),
        ('w:rPr/w:noProof', 'w:rPr/(w:dstrike,w:noProof)'),
        ('w:rPr/w:snapToGrid', 'w:rPr/(w:dstrike,w:snapToGrid)'),
        ('w:rPr/w:vanish', 'w:rPr/(w:dstrike,w:vanish)'),
        ('w:rPr/w:webHidden', 'w:rPr/(w:dstrike,w:webHidden)'),
        ('w:rPr/w:color', 'w:rPr/(w:dstrike,w:color)'),
        ('w:rPr/w:spacing', 'w:rPr/(w:dstrike,w:spacing)'),
        ('w:rPr/w:w', 'w:rPr/(w:dstrike,w:w)'),
        ('w:rPr/w:kern', 'w:rPr/(w:dstrike,w:kern)'),
        ('w:rPr/w:position', 'w:rPr/(w:dstrike,w:position)'),
        ('w:rPr/w:sz', 'w:rPr/(w:dstrike,w:sz)'),
        ('w:rPr/w:szCs', 'w:rPr/(w:dstrike,w:szCs)'),
        ('w:rPr/w:highlight', 'w:rPr/(w:dstrike,w:highlight)'),
        ('w:rPr/w:u', 'w:rPr/(w:dstrike,w:u)'),
        ('w:rPr/w:effect', 'w:rPr/(w:dstrike,w:effect)'),
        ('w:rPr/w:bdr', 'w:rPr/(w:dstrike,w:bdr)'),
        ('w:rPr/w:shd', 'w:rPr/(w:dstrike,w:shd)'),
        ('w:rPr/w:fitText', 'w:rPr/(w:dstrike,w:fitText)'),
        ('w:rPr/w:vertAlign', 'w:rPr/(w:dstrike,w:vertAlign)'),
        ('w:rPr/w:rtl', 'w:rPr/(w:dstrike,w:rtl)'),
        ('w:rPr/w:cs', 'w:rPr/(w:dstrike,w:cs)'),
        ('w:rPr/w:em', 'w:rPr/(w:dstrike,w:em)'),
        ('w:rPr/w:lang', 'w:rPr/(w:dstrike,w:lang)'),
        ('w:rPr/w:eastAsianLayout', 'w:rPr/(w:dstrike,w:eastAsianLayout)'),
        ('w:rPr/w:specVanish', 'w:rPr/(w:dstrike,w:specVanish)'),
        ('w:rPr/w:oMath', 'w:rPr/(w:dstrike,w:oMath)'),
        ('w:rPr/w:rPrChange', 'w:rPr/(w:dstrike,w:rPrChange)')
    ])
    def add_dstrike_fixture(self, request):
        return self.add_x_fixture(request)

    @pytest.fixture(params=[
        ('w:rPr/w:rStyle', 'w:rPr/(w:rStyle,w:outline)'),
        ('w:rPr/w:rFonts', 'w:rPr/(w:rFonts,w:outline)'),
        ('w:rPr/w:b', 'w:rPr/(w:b,w:outline)'),
        ('w:rPr/w:bCs', 'w:rPr/(w:bCs,w:outline)'),
        ('w:rPr/w:i', 'w:rPr/(w:i,w:outline)'),
        ('w:rPr/w:iCs', 'w:rPr/(w:iCs,w:outline)'),
        ('w:rPr/w:caps', 'w:rPr/(w:caps,w:outline)'),
        ('w:rPr/w:smallCaps', 'w:rPr/(w:smallCaps,w:outline)'),
        ('w:rPr/w:strike', 'w:rPr/(w:strike,w:outline)'),
        ('w:rPr/w:dstrike', 'w:rPr/(w:dstrike,w:outline)'),
        ('w:rPr/w:shadow', 'w:rPr/(w:outline,w:shadow)'),
        ('w:rPr/w:emboss', 'w:rPr/(w:outline,w:emboss)'),
        ('w:rPr/w:imprint', 'w:rPr/(w:outline,w:imprint)'),
        ('w:rPr/w:noProof', 'w:rPr/(w:outline,w:noProof)'),
        ('w:rPr/w:snapToGrid', 'w:rPr/(w:outline,w:snapToGrid)'),
        ('w:rPr/w:vanish', 'w:rPr/(w:outline,w:vanish)'),
        ('w:rPr/w:webHidden', 'w:rPr/(w:outline,w:webHidden)'),
        ('w:rPr/w:color', 'w:rPr/(w:outline,w:color)'),
        ('w:rPr/w:spacing', 'w:rPr/(w:outline,w:spacing)'),
        ('w:rPr/w:w', 'w:rPr/(w:outline,w:w)'),
        ('w:rPr/w:kern', 'w:rPr/(w:outline,w:kern)'),
        ('w:rPr/w:position', 'w:rPr/(w:outline,w:position)'),
        ('w:rPr/w:sz', 'w:rPr/(w:outline,w:sz)'),
        ('w:rPr/w:szCs', 'w:rPr/(w:outline,w:szCs)'),
        ('w:rPr/w:highlight', 'w:rPr/(w:outline,w:highlight)'),
        ('w:rPr/w:u', 'w:rPr/(w:outline,w:u)'),
        ('w:rPr/w:effect', 'w:rPr/(w:outline,w:effect)'),
        ('w:rPr/w:bdr', 'w:rPr/(w:outline,w:bdr)'),
        ('w:rPr/w:shd', 'w:rPr/(w:outline,w:shd)'),
        ('w:rPr/w:fitText', 'w:rPr/(w:outline,w:fitText)'),
        ('w:rPr/w:vertAlign', 'w:rPr/(w:outline,w:vertAlign)'),
        ('w:rPr/w:rtl', 'w:rPr/(w:outline,w:rtl)'),
        ('w:rPr/w:cs', 'w:rPr/(w:outline,w:cs)'),
        ('w:rPr/w:em', 'w:rPr/(w:outline,w:em)'),
        ('w:rPr/w:lang', 'w:rPr/(w:outline,w:lang)'),
        ('w:rPr/w:eastAsianLayout', 'w:rPr/(w:outline,w:eastAsianLayout)'),
        ('w:rPr/w:specVanish', 'w:rPr/(w:outline,w:specVanish)'),
        ('w:rPr/w:oMath', 'w:rPr/(w:outline,w:oMath)'),
        ('w:rPr/w:rPrChange', 'w:rPr/(w:outline,w:rPrChange)')
    ])
    def add_outline_fixture(self, request):
        return self.add_x_fixture(request)

    @pytest.fixture(params=[
        ('w:rPr/w:rStyle', 'w:rPr/(w:rStyle,w:shadow)'),
        ('w:rPr/w:rFonts', 'w:rPr/(w:rFonts,w:shadow)'),
        ('w:rPr/w:b', 'w:rPr/(w:b,w:shadow)'),
        ('w:rPr/w:bCs', 'w:rPr/(w:bCs,w:shadow)'),
        ('w:rPr/w:i', 'w:rPr/(w:i,w:shadow)'),
        ('w:rPr/w:iCs', 'w:rPr/(w:iCs,w:shadow)'),
        ('w:rPr/w:caps', 'w:rPr/(w:caps,w:shadow)'),
        ('w:rPr/w:smallCaps', 'w:rPr/(w:smallCaps,w:shadow)'),
        ('w:rPr/w:strike', 'w:rPr/(w:strike,w:shadow)'),
        ('w:rPr/w:dstrike', 'w:rPr/(w:dstrike,w:shadow)'),
        ('w:rPr/w:outline', 'w:rPr/(w:outline,w:shadow)'),
        ('w:rPr/w:emboss', 'w:rPr/(w:shadow,w:emboss)'),
        ('w:rPr/w:imprint', 'w:rPr/(w:shadow,w:imprint)'),
        ('w:rPr/w:noProof', 'w:rPr/(w:shadow,w:noProof)'),
        ('w:rPr/w:snapToGrid', 'w:rPr/(w:shadow,w:snapToGrid)'),
        ('w:rPr/w:vanish', 'w:rPr/(w:shadow,w:vanish)'),
        ('w:rPr/w:webHidden', 'w:rPr/(w:shadow,w:webHidden)'),
        ('w:rPr/w:color', 'w:rPr/(w:shadow,w:color)'),
        ('w:rPr/w:spacing', 'w:rPr/(w:shadow,w:spacing)'),
        ('w:rPr/w:w', 'w:rPr/(w:shadow,w:w)'),
        ('w:rPr/w:kern', 'w:rPr/(w:shadow,w:kern)'),
        ('w:rPr/w:position', 'w:rPr/(w:shadow,w:position)'),
        ('w:rPr/w:sz', 'w:rPr/(w:shadow,w:sz)'),
        ('w:rPr/w:szCs', 'w:rPr/(w:shadow,w:szCs)'),
        ('w:rPr/w:highlight', 'w:rPr/(w:shadow,w:highlight)'),
        ('w:rPr/w:u', 'w:rPr/(w:shadow,w:u)'),
        ('w:rPr/w:effect', 'w:rPr/(w:shadow,w:effect)'),
        ('w:rPr/w:bdr', 'w:rPr/(w:shadow,w:bdr)'),
        ('w:rPr/w:shd', 'w:rPr/(w:shadow,w:shd)'),
        ('w:rPr/w:fitText', 'w:rPr/(w:shadow,w:fitText)'),
        ('w:rPr/w:vertAlign', 'w:rPr/(w:shadow,w:vertAlign)'),
        ('w:rPr/w:rtl', 'w:rPr/(w:shadow,w:rtl)'),
        ('w:rPr/w:cs', 'w:rPr/(w:shadow,w:cs)'),
        ('w:rPr/w:em', 'w:rPr/(w:shadow,w:em)'),
        ('w:rPr/w:lang', 'w:rPr/(w:shadow,w:lang)'),
        ('w:rPr/w:eastAsianLayout', 'w:rPr/(w:shadow,w:eastAsianLayout)'),
        ('w:rPr/w:specVanish', 'w:rPr/(w:shadow,w:specVanish)'),
        ('w:rPr/w:oMath', 'w:rPr/(w:shadow,w:oMath)'),
        ('w:rPr/w:rPrChange', 'w:rPr/(w:shadow,w:rPrChange)')
    ])
    def add_shadow_fixture(self, request):
        return self.add_x_fixture(request)

    @pytest.fixture(params=[
        ('w:rPr/w:rStyle', 'w:rPr/(w:rStyle,w:emboss)'),
        ('w:rPr/w:rFonts', 'w:rPr/(w:rFonts,w:emboss)'),
        ('w:rPr/w:b', 'w:rPr/(w:b,w:emboss)'),
        ('w:rPr/w:bCs', 'w:rPr/(w:bCs,w:emboss)'),
        ('w:rPr/w:i', 'w:rPr/(w:i,w:emboss)'),
        ('w:rPr/w:iCs', 'w:rPr/(w:iCs,w:emboss)'),
        ('w:rPr/w:caps', 'w:rPr/(w:caps,w:emboss)'),
        ('w:rPr/w:smallCaps', 'w:rPr/(w:smallCaps,w:emboss)'),
        ('w:rPr/w:strike', 'w:rPr/(w:strike,w:emboss)'),
        ('w:rPr/w:dstrike', 'w:rPr/(w:dstrike,w:emboss)'),
        ('w:rPr/w:outline', 'w:rPr/(w:outline,w:emboss)'),
        ('w:rPr/w:shadow', 'w:rPr/(w:shadow,w:emboss)'),
        ('w:rPr/w:imprint', 'w:rPr/(w:emboss,w:imprint)'),
        ('w:rPr/w:noProof', 'w:rPr/(w:emboss,w:noProof)'),
        ('w:rPr/w:snapToGrid', 'w:rPr/(w:emboss,w:snapToGrid)'),
        ('w:rPr/w:vanish', 'w:rPr/(w:emboss,w:vanish)'),
        ('w:rPr/w:webHidden', 'w:rPr/(w:emboss,w:webHidden)'),
        ('w:rPr/w:color', 'w:rPr/(w:emboss,w:color)'),
        ('w:rPr/w:spacing', 'w:rPr/(w:emboss,w:spacing)'),
        ('w:rPr/w:w', 'w:rPr/(w:emboss,w:w)'),
        ('w:rPr/w:kern', 'w:rPr/(w:emboss,w:kern)'),
        ('w:rPr/w:position', 'w:rPr/(w:emboss,w:position)'),
        ('w:rPr/w:sz', 'w:rPr/(w:emboss,w:sz)'),
        ('w:rPr/w:szCs', 'w:rPr/(w:emboss,w:szCs)'),
        ('w:rPr/w:highlight', 'w:rPr/(w:emboss,w:highlight)'),
        ('w:rPr/w:u', 'w:rPr/(w:emboss,w:u)'),
        ('w:rPr/w:effect', 'w:rPr/(w:emboss,w:effect)'),
        ('w:rPr/w:bdr', 'w:rPr/(w:emboss,w:bdr)'),
        ('w:rPr/w:shd', 'w:rPr/(w:emboss,w:shd)'),
        ('w:rPr/w:fitText', 'w:rPr/(w:emboss,w:fitText)'),
        ('w:rPr/w:vertAlign', 'w:rPr/(w:emboss,w:vertAlign)'),
        ('w:rPr/w:rtl', 'w:rPr/(w:emboss,w:rtl)'),
        ('w:rPr/w:cs', 'w:rPr/(w:emboss,w:cs)'),
        ('w:rPr/w:em', 'w:rPr/(w:emboss,w:em)'),
        ('w:rPr/w:lang', 'w:rPr/(w:emboss,w:lang)'),
        ('w:rPr/w:eastAsianLayout', 'w:rPr/(w:emboss,w:eastAsianLayout)'),
        ('w:rPr/w:specVanish', 'w:rPr/(w:emboss,w:specVanish)'),
        ('w:rPr/w:oMath', 'w:rPr/(w:emboss,w:oMath)'),
        ('w:rPr/w:rPrChange', 'w:rPr/(w:emboss,w:rPrChange)')
    ])
    def add_emboss_fixture(self, request):
        return self.add_x_fixture(request)

    @pytest.fixture(params=[
        ('w:rPr/w:rStyle', 'w:rPr/(w:rStyle,w:imprint)'),
        ('w:rPr/w:rFonts', 'w:rPr/(w:rFonts,w:imprint)'),
        ('w:rPr/w:b', 'w:rPr/(w:b,w:imprint)'),
        ('w:rPr/w:bCs', 'w:rPr/(w:bCs,w:imprint)'),
        ('w:rPr/w:i', 'w:rPr/(w:i,w:imprint)'),
        ('w:rPr/w:iCs', 'w:rPr/(w:iCs,w:imprint)'),
        ('w:rPr/w:caps', 'w:rPr/(w:caps,w:imprint)'),
        ('w:rPr/w:smallCaps', 'w:rPr/(w:smallCaps,w:imprint)'),
        ('w:rPr/w:strike', 'w:rPr/(w:strike,w:imprint)'),
        ('w:rPr/w:dstrike', 'w:rPr/(w:dstrike,w:imprint)'),
        ('w:rPr/w:outline', 'w:rPr/(w:outline,w:imprint)'),
        ('w:rPr/w:shadow', 'w:rPr/(w:shadow,w:imprint)'),
        ('w:rPr/w:emboss', 'w:rPr/(w:emboss,w:imprint)'),
        ('w:rPr/w:noProof', 'w:rPr/(w:imprint,w:noProof)'),
        ('w:rPr/w:snapToGrid', 'w:rPr/(w:imprint,w:snapToGrid)'),
        ('w:rPr/w:vanish', 'w:rPr/(w:imprint,w:vanish)'),
        ('w:rPr/w:webHidden', 'w:rPr/(w:imprint,w:webHidden)'),
        ('w:rPr/w:color', 'w:rPr/(w:imprint,w:color)'),
        ('w:rPr/w:spacing', 'w:rPr/(w:imprint,w:spacing)'),
        ('w:rPr/w:w', 'w:rPr/(w:imprint,w:w)'),
        ('w:rPr/w:kern', 'w:rPr/(w:imprint,w:kern)'),
        ('w:rPr/w:position', 'w:rPr/(w:imprint,w:position)'),
        ('w:rPr/w:sz', 'w:rPr/(w:imprint,w:sz)'),
        ('w:rPr/w:szCs', 'w:rPr/(w:imprint,w:szCs)'),
        ('w:rPr/w:highlight', 'w:rPr/(w:imprint,w:highlight)'),
        ('w:rPr/w:u', 'w:rPr/(w:imprint,w:u)'),
        ('w:rPr/w:effect', 'w:rPr/(w:imprint,w:effect)'),
        ('w:rPr/w:bdr', 'w:rPr/(w:imprint,w:bdr)'),
        ('w:rPr/w:shd', 'w:rPr/(w:imprint,w:shd)'),
        ('w:rPr/w:fitText', 'w:rPr/(w:imprint,w:fitText)'),
        ('w:rPr/w:vertAlign', 'w:rPr/(w:imprint,w:vertAlign)'),
        ('w:rPr/w:rtl', 'w:rPr/(w:imprint,w:rtl)'),
        ('w:rPr/w:cs', 'w:rPr/(w:imprint,w:cs)'),
        ('w:rPr/w:em', 'w:rPr/(w:imprint,w:em)'),
        ('w:rPr/w:lang', 'w:rPr/(w:imprint,w:lang)'),
        ('w:rPr/w:eastAsianLayout', 'w:rPr/(w:imprint,w:eastAsianLayout)'),
        ('w:rPr/w:specVanish', 'w:rPr/(w:imprint,w:specVanish)'),
        ('w:rPr/w:oMath', 'w:rPr/(w:imprint,w:oMath)'),
        ('w:rPr/w:rPrChange', 'w:rPr/(w:imprint,w:rPrChange)')
    ])
    def add_imprint_fixture(self, request):
        return self.add_x_fixture(request)

    @pytest.fixture(params=[
        ('w:rPr/w:rStyle', 'w:rPr/(w:rStyle,w:noProof)'),
        ('w:rPr/w:rFonts', 'w:rPr/(w:rFonts,w:noProof)'),
        ('w:rPr/w:b', 'w:rPr/(w:b,w:noProof)'),
        ('w:rPr/w:bCs', 'w:rPr/(w:bCs,w:noProof)'),
        ('w:rPr/w:i', 'w:rPr/(w:i,w:noProof)'),
        ('w:rPr/w:iCs', 'w:rPr/(w:iCs,w:noProof)'),
        ('w:rPr/w:caps', 'w:rPr/(w:caps,w:noProof)'),
        ('w:rPr/w:smallCaps', 'w:rPr/(w:smallCaps,w:noProof)'),
        ('w:rPr/w:strike', 'w:rPr/(w:strike,w:noProof)'),
        ('w:rPr/w:dstrike', 'w:rPr/(w:dstrike,w:noProof)'),
        ('w:rPr/w:outline', 'w:rPr/(w:outline,w:noProof)'),
        ('w:rPr/w:shadow', 'w:rPr/(w:shadow,w:noProof)'),
        ('w:rPr/w:emboss', 'w:rPr/(w:emboss,w:noProof)'),
        ('w:rPr/w:imprint', 'w:rPr/(w:imprint,w:noProof)'),
        ('w:rPr/w:snapToGrid', 'w:rPr/(w:noProof,w:snapToGrid)'),
        ('w:rPr/w:vanish', 'w:rPr/(w:noProof,w:vanish)'),
        ('w:rPr/w:webHidden', 'w:rPr/(w:noProof,w:webHidden)'),
        ('w:rPr/w:color', 'w:rPr/(w:noProof,w:color)'),
        ('w:rPr/w:spacing', 'w:rPr/(w:noProof,w:spacing)'),
        ('w:rPr/w:w', 'w:rPr/(w:noProof,w:w)'),
        ('w:rPr/w:kern', 'w:rPr/(w:noProof,w:kern)'),
        ('w:rPr/w:position', 'w:rPr/(w:noProof,w:position)'),
        ('w:rPr/w:sz', 'w:rPr/(w:noProof,w:sz)'),
        ('w:rPr/w:szCs', 'w:rPr/(w:noProof,w:szCs)'),
        ('w:rPr/w:highlight', 'w:rPr/(w:noProof,w:highlight)'),
        ('w:rPr/w:u', 'w:rPr/(w:noProof,w:u)'),
        ('w:rPr/w:effect', 'w:rPr/(w:noProof,w:effect)'),
        ('w:rPr/w:bdr', 'w:rPr/(w:noProof,w:bdr)'),
        ('w:rPr/w:shd', 'w:rPr/(w:noProof,w:shd)'),
        ('w:rPr/w:fitText', 'w:rPr/(w:noProof,w:fitText)'),
        ('w:rPr/w:vertAlign', 'w:rPr/(w:noProof,w:vertAlign)'),
        ('w:rPr/w:rtl', 'w:rPr/(w:noProof,w:rtl)'),
        ('w:rPr/w:cs', 'w:rPr/(w:noProof,w:cs)'),
        ('w:rPr/w:em', 'w:rPr/(w:noProof,w:em)'),
        ('w:rPr/w:lang', 'w:rPr/(w:noProof,w:lang)'),
        ('w:rPr/w:eastAsianLayout', 'w:rPr/(w:noProof,w:eastAsianLayout)'),
        ('w:rPr/w:specVanish', 'w:rPr/(w:noProof,w:specVanish)'),
        ('w:rPr/w:oMath', 'w:rPr/(w:noProof,w:oMath)'),
        ('w:rPr/w:rPrChange', 'w:rPr/(w:noProof,w:rPrChange)')
    ])
    def add_noProof_fixture(self, request):
        return self.add_x_fixture(request)

    @pytest.fixture(params=[
        ('w:rPr/w:rStyle', 'w:rPr/(w:rStyle,w:snapToGrid)'),
        ('w:rPr/w:rFonts', 'w:rPr/(w:rFonts,w:snapToGrid)'),
        ('w:rPr/w:b', 'w:rPr/(w:b,w:snapToGrid)'),
        ('w:rPr/w:bCs', 'w:rPr/(w:bCs,w:snapToGrid)'),
        ('w:rPr/w:i', 'w:rPr/(w:i,w:snapToGrid)'),
        ('w:rPr/w:iCs', 'w:rPr/(w:iCs,w:snapToGrid)'),
        ('w:rPr/w:caps', 'w:rPr/(w:caps,w:snapToGrid)'),
        ('w:rPr/w:smallCaps', 'w:rPr/(w:smallCaps,w:snapToGrid)'),
        ('w:rPr/w:strike', 'w:rPr/(w:strike,w:snapToGrid)'),
        ('w:rPr/w:dstrike', 'w:rPr/(w:dstrike,w:snapToGrid)'),
        ('w:rPr/w:outline', 'w:rPr/(w:outline,w:snapToGrid)'),
        ('w:rPr/w:shadow', 'w:rPr/(w:shadow,w:snapToGrid)'),
        ('w:rPr/w:emboss', 'w:rPr/(w:emboss,w:snapToGrid)'),
        ('w:rPr/w:imprint', 'w:rPr/(w:imprint,w:snapToGrid)'),
        ('w:rPr/w:noProof', 'w:rPr/(w:noProof,w:snapToGrid)'),
        ('w:rPr/w:vanish', 'w:rPr/(w:snapToGrid,w:vanish)'),
        ('w:rPr/w:webHidden', 'w:rPr/(w:snapToGrid,w:webHidden)'),
        ('w:rPr/w:color', 'w:rPr/(w:snapToGrid,w:color)'),
        ('w:rPr/w:spacing', 'w:rPr/(w:snapToGrid,w:spacing)'),
        ('w:rPr/w:w', 'w:rPr/(w:snapToGrid,w:w)'),
        ('w:rPr/w:kern', 'w:rPr/(w:snapToGrid,w:kern)'),
        ('w:rPr/w:position', 'w:rPr/(w:snapToGrid,w:position)'),
        ('w:rPr/w:sz', 'w:rPr/(w:snapToGrid,w:sz)'),
        ('w:rPr/w:szCs', 'w:rPr/(w:snapToGrid,w:szCs)'),
        ('w:rPr/w:highlight', 'w:rPr/(w:snapToGrid,w:highlight)'),
        ('w:rPr/w:u', 'w:rPr/(w:snapToGrid,w:u)'),
        ('w:rPr/w:effect', 'w:rPr/(w:snapToGrid,w:effect)'),
        ('w:rPr/w:bdr', 'w:rPr/(w:snapToGrid,w:bdr)'),
        ('w:rPr/w:shd', 'w:rPr/(w:snapToGrid,w:shd)'),
        ('w:rPr/w:fitText', 'w:rPr/(w:snapToGrid,w:fitText)'),
        ('w:rPr/w:vertAlign', 'w:rPr/(w:snapToGrid,w:vertAlign)'),
        ('w:rPr/w:rtl', 'w:rPr/(w:snapToGrid,w:rtl)'),
        ('w:rPr/w:cs', 'w:rPr/(w:snapToGrid,w:cs)'),
        ('w:rPr/w:em', 'w:rPr/(w:snapToGrid,w:em)'),
        ('w:rPr/w:lang', 'w:rPr/(w:snapToGrid,w:lang)'),
        ('w:rPr/w:eastAsianLayout', 'w:rPr/(w:snapToGrid,w:eastAsianLayout)'),
        ('w:rPr/w:specVanish', 'w:rPr/(w:snapToGrid,w:specVanish)'),
        ('w:rPr/w:oMath', 'w:rPr/(w:snapToGrid,w:oMath)'),
        ('w:rPr/w:rPrChange', 'w:rPr/(w:snapToGrid,w:rPrChange)')
    ])
    def add_snapToGrid_fixture(self, request):
        return self.add_x_fixture(request)

    @pytest.fixture(params=[
        ('w:rPr/w:rStyle', 'w:rPr/(w:rStyle,w:vanish)'),
        ('w:rPr/w:rFonts', 'w:rPr/(w:rFonts,w:vanish)'),
        ('w:rPr/w:b', 'w:rPr/(w:b,w:vanish)'),
        ('w:rPr/w:bCs', 'w:rPr/(w:bCs,w:vanish)'),
        ('w:rPr/w:i', 'w:rPr/(w:i,w:vanish)'),
        ('w:rPr/w:iCs', 'w:rPr/(w:iCs,w:vanish)'),
        ('w:rPr/w:caps', 'w:rPr/(w:caps,w:vanish)'),
        ('w:rPr/w:smallCaps', 'w:rPr/(w:smallCaps,w:vanish)'),
        ('w:rPr/w:strike', 'w:rPr/(w:strike,w:vanish)'),
        ('w:rPr/w:dstrike', 'w:rPr/(w:dstrike,w:vanish)'),
        ('w:rPr/w:outline', 'w:rPr/(w:outline,w:vanish)'),
        ('w:rPr/w:shadow', 'w:rPr/(w:shadow,w:vanish)'),
        ('w:rPr/w:emboss', 'w:rPr/(w:emboss,w:vanish)'),
        ('w:rPr/w:imprint', 'w:rPr/(w:imprint,w:vanish)'),
        ('w:rPr/w:noProof', 'w:rPr/(w:noProof,w:vanish)'),
        ('w:rPr/w:snapToGrid', 'w:rPr/(w:snapToGrid,w:vanish)'),
        ('w:rPr/w:webHidden', 'w:rPr/(w:vanish,w:webHidden)'),
        ('w:rPr/w:color', 'w:rPr/(w:vanish,w:color)'),
        ('w:rPr/w:spacing', 'w:rPr/(w:vanish,w:spacing)'),
        ('w:rPr/w:w', 'w:rPr/(w:vanish,w:w)'),
        ('w:rPr/w:kern', 'w:rPr/(w:vanish,w:kern)'),
        ('w:rPr/w:position', 'w:rPr/(w:vanish,w:position)'),
        ('w:rPr/w:sz', 'w:rPr/(w:vanish,w:sz)'),
        ('w:rPr/w:szCs', 'w:rPr/(w:vanish,w:szCs)'),
        ('w:rPr/w:highlight', 'w:rPr/(w:vanish,w:highlight)'),
        ('w:rPr/w:u', 'w:rPr/(w:vanish,w:u)'),
        ('w:rPr/w:effect', 'w:rPr/(w:vanish,w:effect)'),
        ('w:rPr/w:bdr', 'w:rPr/(w:vanish,w:bdr)'),
        ('w:rPr/w:shd', 'w:rPr/(w:vanish,w:shd)'),
        ('w:rPr/w:fitText', 'w:rPr/(w:vanish,w:fitText)'),
        ('w:rPr/w:vertAlign', 'w:rPr/(w:vanish,w:vertAlign)'),
        ('w:rPr/w:rtl', 'w:rPr/(w:vanish,w:rtl)'),
        ('w:rPr/w:cs', 'w:rPr/(w:vanish,w:cs)'),
        ('w:rPr/w:em', 'w:rPr/(w:vanish,w:em)'),
        ('w:rPr/w:lang', 'w:rPr/(w:vanish,w:lang)'),
        ('w:rPr/w:eastAsianLayout', 'w:rPr/(w:vanish,w:eastAsianLayout)'),
        ('w:rPr/w:specVanish', 'w:rPr/(w:vanish,w:specVanish)'),
        ('w:rPr/w:oMath', 'w:rPr/(w:vanish,w:oMath)'),
        ('w:rPr/w:rPrChange', 'w:rPr/(w:vanish,w:rPrChange)')
    ])
    def add_vanish_fixture(self, request):
        return self.add_x_fixture(request)

    @pytest.fixture(params=[
        ('w:rPr/w:rStyle', 'w:rPr/(w:rStyle,w:webHidden)'),
        ('w:rPr/w:rFonts', 'w:rPr/(w:rFonts,w:webHidden)'),
        ('w:rPr/w:b', 'w:rPr/(w:b,w:webHidden)'),
        ('w:rPr/w:bCs', 'w:rPr/(w:bCs,w:webHidden)'),
        ('w:rPr/w:i', 'w:rPr/(w:i,w:webHidden)'),
        ('w:rPr/w:iCs', 'w:rPr/(w:iCs,w:webHidden)'),
        ('w:rPr/w:caps', 'w:rPr/(w:caps,w:webHidden)'),
        ('w:rPr/w:smallCaps', 'w:rPr/(w:smallCaps,w:webHidden)'),
        ('w:rPr/w:strike', 'w:rPr/(w:strike,w:webHidden)'),
        ('w:rPr/w:dstrike', 'w:rPr/(w:dstrike,w:webHidden)'),
        ('w:rPr/w:outline', 'w:rPr/(w:outline,w:webHidden)'),
        ('w:rPr/w:shadow', 'w:rPr/(w:shadow,w:webHidden)'),
        ('w:rPr/w:emboss', 'w:rPr/(w:emboss,w:webHidden)'),
        ('w:rPr/w:imprint', 'w:rPr/(w:imprint,w:webHidden)'),
        ('w:rPr/w:noProof', 'w:rPr/(w:noProof,w:webHidden)'),
        ('w:rPr/w:snapToGrid', 'w:rPr/(w:snapToGrid,w:webHidden)'),
        ('w:rPr/w:vanish', 'w:rPr/(w:vanish,w:webHidden)'),
        ('w:rPr/w:color', 'w:rPr/(w:webHidden,w:color)'),
        ('w:rPr/w:spacing', 'w:rPr/(w:webHidden,w:spacing)'),
        ('w:rPr/w:w', 'w:rPr/(w:webHidden,w:w)'),
        ('w:rPr/w:kern', 'w:rPr/(w:webHidden,w:kern)'),
        ('w:rPr/w:position', 'w:rPr/(w:webHidden,w:position)'),
        ('w:rPr/w:sz', 'w:rPr/(w:webHidden,w:sz)'),
        ('w:rPr/w:szCs', 'w:rPr/(w:webHidden,w:szCs)'),
        ('w:rPr/w:highlight', 'w:rPr/(w:webHidden,w:highlight)'),
        ('w:rPr/w:u', 'w:rPr/(w:webHidden,w:u)'),
        ('w:rPr/w:effect', 'w:rPr/(w:webHidden,w:effect)'),
        ('w:rPr/w:bdr', 'w:rPr/(w:webHidden,w:bdr)'),
        ('w:rPr/w:shd', 'w:rPr/(w:webHidden,w:shd)'),
        ('w:rPr/w:fitText', 'w:rPr/(w:webHidden,w:fitText)'),
        ('w:rPr/w:vertAlign', 'w:rPr/(w:webHidden,w:vertAlign)'),
        ('w:rPr/w:rtl', 'w:rPr/(w:webHidden,w:rtl)'),
        ('w:rPr/w:cs', 'w:rPr/(w:webHidden,w:cs)'),
        ('w:rPr/w:em', 'w:rPr/(w:webHidden,w:em)'),
        ('w:rPr/w:lang', 'w:rPr/(w:webHidden,w:lang)'),
        ('w:rPr/w:eastAsianLayout', 'w:rPr/(w:webHidden,w:eastAsianLayout)'),
        ('w:rPr/w:specVanish', 'w:rPr/(w:webHidden,w:specVanish)'),
        ('w:rPr/w:oMath', 'w:rPr/(w:webHidden,w:oMath)'),
        ('w:rPr/w:rPrChange', 'w:rPr/(w:webHidden,w:rPrChange)')
    ])
    def add_webHidden_fixture(self, request):
        return self.add_x_fixture(request)

    @pytest.fixture(params=[
        ('w:rPr/w:rStyle', 'w:rPr/(w:rStyle,w:color{w:val=000000})'),
        ('w:rPr/w:rFonts', 'w:rPr/(w:rFonts,w:color{w:val=000000})'),
        ('w:rPr/w:b', 'w:rPr/(w:b,w:color{w:val=000000})'),
        ('w:rPr/w:bCs', 'w:rPr/(w:bCs,w:color{w:val=000000})'),
        ('w:rPr/w:i', 'w:rPr/(w:i,w:color{w:val=000000})'),
        ('w:rPr/w:iCs', 'w:rPr/(w:iCs,w:color{w:val=000000})'),
        ('w:rPr/w:caps', 'w:rPr/(w:caps,w:color{w:val=000000})'),
        ('w:rPr/w:smallCaps', 'w:rPr/(w:smallCaps,w:color{w:val=000000})'),
        ('w:rPr/w:strike', 'w:rPr/(w:strike,w:color{w:val=000000})'),
        ('w:rPr/w:dstrike', 'w:rPr/(w:dstrike,w:color{w:val=000000})'),
        ('w:rPr/w:outline', 'w:rPr/(w:outline,w:color{w:val=000000})'),
        ('w:rPr/w:shadow', 'w:rPr/(w:shadow,w:color{w:val=000000})'),
        ('w:rPr/w:emboss', 'w:rPr/(w:emboss,w:color{w:val=000000})'),
        ('w:rPr/w:imprint', 'w:rPr/(w:imprint,w:color{w:val=000000})'),
        ('w:rPr/w:noProof', 'w:rPr/(w:noProof,w:color{w:val=000000})'),
        ('w:rPr/w:snapToGrid', 'w:rPr/(w:snapToGrid,w:color{w:val=000000})'),
        ('w:rPr/w:vanish', 'w:rPr/(w:vanish,w:color{w:val=000000})'),
        ('w:rPr/w:webHidden', 'w:rPr/(w:webHidden,w:color{w:val=000000})'),
        ('w:rPr/w:spacing', 'w:rPr/(w:color{w:val=000000},w:spacing)'),
        ('w:rPr/w:w', 'w:rPr/(w:color{w:val=000000},w:w)'),
        ('w:rPr/w:kern', 'w:rPr/(w:color{w:val=000000},w:kern)'),
        ('w:rPr/w:position', 'w:rPr/(w:color{w:val=000000},w:position)'),
        ('w:rPr/w:sz', 'w:rPr/(w:color{w:val=000000},w:sz)'),
        ('w:rPr/w:szCs', 'w:rPr/(w:color{w:val=000000},w:szCs)'),
        ('w:rPr/w:highlight', 'w:rPr/(w:color{w:val=000000},w:highlight)'),
        ('w:rPr/w:u', 'w:rPr/(w:color{w:val=000000},w:u)'),
        ('w:rPr/w:effect', 'w:rPr/(w:color{w:val=000000},w:effect)'),
        ('w:rPr/w:bdr', 'w:rPr/(w:color{w:val=000000},w:bdr)'),
        ('w:rPr/w:shd', 'w:rPr/(w:color{w:val=000000},w:shd)'),
        ('w:rPr/w:fitText', 'w:rPr/(w:color{w:val=000000},w:fitText)'),
        ('w:rPr/w:vertAlign', 'w:rPr/(w:color{w:val=000000},w:vertAlign)'),
        ('w:rPr/w:rtl', 'w:rPr/(w:color{w:val=000000},w:rtl)'),
        ('w:rPr/w:cs', 'w:rPr/(w:color{w:val=000000},w:cs)'),
        ('w:rPr/w:em', 'w:rPr/(w:color{w:val=000000},w:em)'),
        ('w:rPr/w:lang', 'w:rPr/(w:color{w:val=000000},w:lang)'),
        ('w:rPr/w:eastAsianLayout', 'w:rPr/(w:color{w:val=000000},w:eastAsianLayout)'),
        ('w:rPr/w:specVanish', 'w:rPr/(w:color{w:val=000000},w:specVanish)'),
        ('w:rPr/w:oMath', 'w:rPr/(w:color{w:val=000000},w:oMath)'),
        ('w:rPr/w:rPrChange', 'w:rPr/(w:color{w:val=000000},w:rPrChange)')
    ])
    def add_color_fixture(self, request):
        return self.add_x_fixture(request)

    @pytest.fixture(params=[
        ('w:rPr/w:rStyle', 'w:rPr/(w:rStyle,w:spacing)'),
        ('w:rPr/w:rFonts', 'w:rPr/(w:rFonts,w:spacing)'),
        ('w:rPr/w:b', 'w:rPr/(w:b,w:spacing)'),
        ('w:rPr/w:bCs', 'w:rPr/(w:bCs,w:spacing)'),
        ('w:rPr/w:i', 'w:rPr/(w:i,w:spacing)'),
        ('w:rPr/w:iCs', 'w:rPr/(w:iCs,w:spacing)'),
        ('w:rPr/w:caps', 'w:rPr/(w:caps,w:spacing)'),
        ('w:rPr/w:smallCaps', 'w:rPr/(w:smallCaps,w:spacing)'),
        ('w:rPr/w:strike', 'w:rPr/(w:strike,w:spacing)'),
        ('w:rPr/w:dstrike', 'w:rPr/(w:dstrike,w:spacing)'),
        ('w:rPr/w:outline', 'w:rPr/(w:outline,w:spacing)'),
        ('w:rPr/w:shadow', 'w:rPr/(w:shadow,w:spacing)'),
        ('w:rPr/w:emboss', 'w:rPr/(w:emboss,w:spacing)'),
        ('w:rPr/w:imprint', 'w:rPr/(w:imprint,w:spacing)'),
        ('w:rPr/w:noProof', 'w:rPr/(w:noProof,w:spacing)'),
        ('w:rPr/w:snapToGrid', 'w:rPr/(w:snapToGrid,w:spacing)'),
        ('w:rPr/w:vanish', 'w:rPr/(w:vanish,w:spacing)'),
        ('w:rPr/w:webHidden', 'w:rPr/(w:webHidden,w:spacing)'),
        ('w:rPr/w:color', 'w:rPr/(w:color,w:spacing)'),
        ('w:rPr/w:w', 'w:rPr/(w:spacing,w:w)'),
        ('w:rPr/w:kern', 'w:rPr/(w:spacing,w:kern)'),
        ('w:rPr/w:position', 'w:rPr/(w:spacing,w:position)'),
        ('w:rPr/w:sz', 'w:rPr/(w:spacing,w:sz)'),
        ('w:rPr/w:szCs', 'w:rPr/(w:spacing,w:szCs)'),
        ('w:rPr/w:highlight', 'w:rPr/(w:spacing,w:highlight)'),
        ('w:rPr/w:u', 'w:rPr/(w:spacing,w:u)'),
        ('w:rPr/w:effect', 'w:rPr/(w:spacing,w:effect)'),
        ('w:rPr/w:bdr', 'w:rPr/(w:spacing,w:bdr)'),
        ('w:rPr/w:shd', 'w:rPr/(w:spacing,w:shd)'),
        ('w:rPr/w:fitText', 'w:rPr/(w:spacing,w:fitText)'),
        ('w:rPr/w:vertAlign', 'w:rPr/(w:spacing,w:vertAlign)'),
        ('w:rPr/w:rtl', 'w:rPr/(w:spacing,w:rtl)'),
        ('w:rPr/w:cs', 'w:rPr/(w:spacing,w:cs)'),
        ('w:rPr/w:em', 'w:rPr/(w:spacing,w:em)'),
        ('w:rPr/w:lang', 'w:rPr/(w:spacing,w:lang)'),
        ('w:rPr/w:eastAsianLayout', 'w:rPr/(w:spacing,w:eastAsianLayout)'),
        ('w:rPr/w:specVanish', 'w:rPr/(w:spacing,w:specVanish)'),
        ('w:rPr/w:oMath', 'w:rPr/(w:spacing,w:oMath)'),
        ('w:rPr/w:rPrChange', 'w:rPr/(w:spacing,w:rPrChange)')
    ])
    def add_spacing_fixture(self, request):
        return self.add_x_fixture(request)

    @pytest.fixture(params=[
        ('w:rPr/w:rStyle', 'w:rPr/(w:rStyle,w:w)'),
        ('w:rPr/w:rFonts', 'w:rPr/(w:rFonts,w:w)'),
        ('w:rPr/w:b', 'w:rPr/(w:b,w:w)'),
        ('w:rPr/w:bCs', 'w:rPr/(w:bCs,w:w)'),
        ('w:rPr/w:i', 'w:rPr/(w:i,w:w)'),
        ('w:rPr/w:iCs', 'w:rPr/(w:iCs,w:w)'),
        ('w:rPr/w:caps', 'w:rPr/(w:caps,w:w)'),
        ('w:rPr/w:smallCaps', 'w:rPr/(w:smallCaps,w:w)'),
        ('w:rPr/w:strike', 'w:rPr/(w:strike,w:w)'),
        ('w:rPr/w:dstrike', 'w:rPr/(w:dstrike,w:w)'),
        ('w:rPr/w:outline', 'w:rPr/(w:outline,w:w)'),
        ('w:rPr/w:shadow', 'w:rPr/(w:shadow,w:w)'),
        ('w:rPr/w:emboss', 'w:rPr/(w:emboss,w:w)'),
        ('w:rPr/w:imprint', 'w:rPr/(w:imprint,w:w)'),
        ('w:rPr/w:noProof', 'w:rPr/(w:noProof,w:w)'),
        ('w:rPr/w:snapToGrid', 'w:rPr/(w:snapToGrid,w:w)'),
        ('w:rPr/w:vanish', 'w:rPr/(w:vanish,w:w)'),
        ('w:rPr/w:webHidden', 'w:rPr/(w:webHidden,w:w)'),
        ('w:rPr/w:color', 'w:rPr/(w:color,w:w)'),
        ('w:rPr/w:spacing', 'w:rPr/(w:spacing,w:w)'),
        ('w:rPr/w:kern', 'w:rPr/(w:w,w:kern)'),
        ('w:rPr/w:position', 'w:rPr/(w:w,w:position)'),
        ('w:rPr/w:sz', 'w:rPr/(w:w,w:sz)'),
        ('w:rPr/w:szCs', 'w:rPr/(w:w,w:szCs)'),
        ('w:rPr/w:highlight', 'w:rPr/(w:w,w:highlight)'),
        ('w:rPr/w:u', 'w:rPr/(w:w,w:u)'),
        ('w:rPr/w:effect', 'w:rPr/(w:w,w:effect)'),
        ('w:rPr/w:bdr', 'w:rPr/(w:w,w:bdr)'),
        ('w:rPr/w:shd', 'w:rPr/(w:w,w:shd)'),
        ('w:rPr/w:fitText', 'w:rPr/(w:w,w:fitText)'),
        ('w:rPr/w:vertAlign', 'w:rPr/(w:w,w:vertAlign)'),
        ('w:rPr/w:rtl', 'w:rPr/(w:w,w:rtl)'),
        ('w:rPr/w:cs', 'w:rPr/(w:w,w:cs)'),
        ('w:rPr/w:em', 'w:rPr/(w:w,w:em)'),
        ('w:rPr/w:lang', 'w:rPr/(w:w,w:lang)'),
        ('w:rPr/w:eastAsianLayout', 'w:rPr/(w:w,w:eastAsianLayout)'),
        ('w:rPr/w:specVanish', 'w:rPr/(w:w,w:specVanish)'),
        ('w:rPr/w:oMath', 'w:rPr/(w:w,w:oMath)'),
        ('w:rPr/w:rPrChange', 'w:rPr/(w:w,w:rPrChange)')
    ])
    def add_w_fixture(self, request):
        return self.add_x_fixture(request)

    @pytest.fixture(params=[
        ('w:rPr/w:rStyle', 'w:rPr/(w:rStyle,w:kern)'),
        ('w:rPr/w:rFonts', 'w:rPr/(w:rFonts,w:kern)'),
        ('w:rPr/w:b', 'w:rPr/(w:b,w:kern)'),
        ('w:rPr/w:bCs', 'w:rPr/(w:bCs,w:kern)'),
        ('w:rPr/w:i', 'w:rPr/(w:i,w:kern)'),
        ('w:rPr/w:iCs', 'w:rPr/(w:iCs,w:kern)'),
        ('w:rPr/w:caps', 'w:rPr/(w:caps,w:kern)'),
        ('w:rPr/w:smallCaps', 'w:rPr/(w:smallCaps,w:kern)'),
        ('w:rPr/w:strike', 'w:rPr/(w:strike,w:kern)'),
        ('w:rPr/w:dstrike', 'w:rPr/(w:dstrike,w:kern)'),
        ('w:rPr/w:outline', 'w:rPr/(w:outline,w:kern)'),
        ('w:rPr/w:shadow', 'w:rPr/(w:shadow,w:kern)'),
        ('w:rPr/w:emboss', 'w:rPr/(w:emboss,w:kern)'),
        ('w:rPr/w:imprint', 'w:rPr/(w:imprint,w:kern)'),
        ('w:rPr/w:noProof', 'w:rPr/(w:noProof,w:kern)'),
        ('w:rPr/w:snapToGrid', 'w:rPr/(w:snapToGrid,w:kern)'),
        ('w:rPr/w:vanish', 'w:rPr/(w:vanish,w:kern)'),
        ('w:rPr/w:webHidden', 'w:rPr/(w:webHidden,w:kern)'),
        ('w:rPr/w:color', 'w:rPr/(w:color,w:kern)'),
        ('w:rPr/w:spacing', 'w:rPr/(w:spacing,w:kern)'),
        ('w:rPr/w:w', 'w:rPr/(w:w,w:kern)'),
        ('w:rPr/w:position', 'w:rPr/(w:kern,w:position)'),
        ('w:rPr/w:sz', 'w:rPr/(w:kern,w:sz)'),
        ('w:rPr/w:szCs', 'w:rPr/(w:kern,w:szCs)'),
        ('w:rPr/w:highlight', 'w:rPr/(w:kern,w:highlight)'),
        ('w:rPr/w:u', 'w:rPr/(w:kern,w:u)'),
        ('w:rPr/w:effect', 'w:rPr/(w:kern,w:effect)'),
        ('w:rPr/w:bdr', 'w:rPr/(w:kern,w:bdr)'),
        ('w:rPr/w:shd', 'w:rPr/(w:kern,w:shd)'),
        ('w:rPr/w:fitText', 'w:rPr/(w:kern,w:fitText)'),
        ('w:rPr/w:vertAlign', 'w:rPr/(w:kern,w:vertAlign)'),
        ('w:rPr/w:rtl', 'w:rPr/(w:kern,w:rtl)'),
        ('w:rPr/w:cs', 'w:rPr/(w:kern,w:cs)'),
        ('w:rPr/w:em', 'w:rPr/(w:kern,w:em)'),
        ('w:rPr/w:lang', 'w:rPr/(w:kern,w:lang)'),
        ('w:rPr/w:eastAsianLayout', 'w:rPr/(w:kern,w:eastAsianLayout)'),
        ('w:rPr/w:specVanish', 'w:rPr/(w:kern,w:specVanish)'),
        ('w:rPr/w:oMath', 'w:rPr/(w:kern,w:oMath)'),
        ('w:rPr/w:rPrChange', 'w:rPr/(w:kern,w:rPrChange)')
    ])
    def add_kern_fixture(self, request):
        return self.add_x_fixture(request)

    @pytest.fixture(params=[
        ('w:rPr/w:rStyle', 'w:rPr/(w:rStyle,w:position)'),
        ('w:rPr/w:rFonts', 'w:rPr/(w:rFonts,w:position)'),
        ('w:rPr/w:b', 'w:rPr/(w:b,w:position)'),
        ('w:rPr/w:bCs', 'w:rPr/(w:bCs,w:position)'),
        ('w:rPr/w:i', 'w:rPr/(w:i,w:position)'),
        ('w:rPr/w:iCs', 'w:rPr/(w:iCs,w:position)'),
        ('w:rPr/w:caps', 'w:rPr/(w:caps,w:position)'),
        ('w:rPr/w:smallCaps', 'w:rPr/(w:smallCaps,w:position)'),
        ('w:rPr/w:strike', 'w:rPr/(w:strike,w:position)'),
        ('w:rPr/w:dstrike', 'w:rPr/(w:dstrike,w:position)'),
        ('w:rPr/w:outline', 'w:rPr/(w:outline,w:position)'),
        ('w:rPr/w:shadow', 'w:rPr/(w:shadow,w:position)'),
        ('w:rPr/w:emboss', 'w:rPr/(w:emboss,w:position)'),
        ('w:rPr/w:imprint', 'w:rPr/(w:imprint,w:position)'),
        ('w:rPr/w:noProof', 'w:rPr/(w:noProof,w:position)'),
        ('w:rPr/w:snapToGrid', 'w:rPr/(w:snapToGrid,w:position)'),
        ('w:rPr/w:vanish', 'w:rPr/(w:vanish,w:position)'),
        ('w:rPr/w:webHidden', 'w:rPr/(w:webHidden,w:position)'),
        ('w:rPr/w:color', 'w:rPr/(w:color,w:position)'),
        ('w:rPr/w:spacing', 'w:rPr/(w:spacing,w:position)'),
        ('w:rPr/w:w', 'w:rPr/(w:w,w:position)'),
        ('w:rPr/w:kern', 'w:rPr/(w:kern,w:position)'),
        ('w:rPr/w:sz', 'w:rPr/(w:position,w:sz)'),
        ('w:rPr/w:szCs', 'w:rPr/(w:position,w:szCs)'),
        ('w:rPr/w:highlight', 'w:rPr/(w:position,w:highlight)'),
        ('w:rPr/w:u', 'w:rPr/(w:position,w:u)'),
        ('w:rPr/w:effect', 'w:rPr/(w:position,w:effect)'),
        ('w:rPr/w:bdr', 'w:rPr/(w:position,w:bdr)'),
        ('w:rPr/w:shd', 'w:rPr/(w:position,w:shd)'),
        ('w:rPr/w:fitText', 'w:rPr/(w:position,w:fitText)'),
        ('w:rPr/w:vertAlign', 'w:rPr/(w:position,w:vertAlign)'),
        ('w:rPr/w:rtl', 'w:rPr/(w:position,w:rtl)'),
        ('w:rPr/w:cs', 'w:rPr/(w:position,w:cs)'),
        ('w:rPr/w:em', 'w:rPr/(w:position,w:em)'),
        ('w:rPr/w:lang', 'w:rPr/(w:position,w:lang)'),
        ('w:rPr/w:eastAsianLayout', 'w:rPr/(w:position,w:eastAsianLayout)'),
        ('w:rPr/w:specVanish', 'w:rPr/(w:position,w:specVanish)'),
        ('w:rPr/w:oMath', 'w:rPr/(w:position,w:oMath)'),
        ('w:rPr/w:rPrChange', 'w:rPr/(w:position,w:rPrChange)')
    ])
    def add_position_fixture(self, request):
        return self.add_x_fixture(request)

    @pytest.fixture(params=[
        ('w:rPr/w:rStyle', 'w:rPr/(w:rStyle,w:sz)'),
        ('w:rPr/w:rFonts', 'w:rPr/(w:rFonts,w:sz)'),
        ('w:rPr/w:b', 'w:rPr/(w:b,w:sz)'),
        ('w:rPr/w:bCs', 'w:rPr/(w:bCs,w:sz)'),
        ('w:rPr/w:i', 'w:rPr/(w:i,w:sz)'),
        ('w:rPr/w:iCs', 'w:rPr/(w:iCs,w:sz)'),
        ('w:rPr/w:caps', 'w:rPr/(w:caps,w:sz)'),
        ('w:rPr/w:smallCaps', 'w:rPr/(w:smallCaps,w:sz)'),
        ('w:rPr/w:strike', 'w:rPr/(w:strike,w:sz)'),
        ('w:rPr/w:dstrike', 'w:rPr/(w:dstrike,w:sz)'),
        ('w:rPr/w:outline', 'w:rPr/(w:outline,w:sz)'),
        ('w:rPr/w:shadow', 'w:rPr/(w:shadow,w:sz)'),
        ('w:rPr/w:emboss', 'w:rPr/(w:emboss,w:sz)'),
        ('w:rPr/w:imprint', 'w:rPr/(w:imprint,w:sz)'),
        ('w:rPr/w:noProof', 'w:rPr/(w:noProof,w:sz)'),
        ('w:rPr/w:snapToGrid', 'w:rPr/(w:snapToGrid,w:sz)'),
        ('w:rPr/w:vanish', 'w:rPr/(w:vanish,w:sz)'),
        ('w:rPr/w:webHidden', 'w:rPr/(w:webHidden,w:sz)'),
        ('w:rPr/w:color', 'w:rPr/(w:color,w:sz)'),
        ('w:rPr/w:spacing', 'w:rPr/(w:spacing,w:sz)'),
        ('w:rPr/w:w', 'w:rPr/(w:w,w:sz)'),
        ('w:rPr/w:kern', 'w:rPr/(w:kern,w:sz)'),
        ('w:rPr/w:position', 'w:rPr/(w:position,w:sz)'),
        ('w:rPr/w:szCs', 'w:rPr/(w:sz,w:szCs)'),
        ('w:rPr/w:highlight', 'w:rPr/(w:sz,w:highlight)'),
        ('w:rPr/w:u', 'w:rPr/(w:sz,w:u)'),
        ('w:rPr/w:effect', 'w:rPr/(w:sz,w:effect)'),
        ('w:rPr/w:bdr', 'w:rPr/(w:sz,w:bdr)'),
        ('w:rPr/w:shd', 'w:rPr/(w:sz,w:shd)'),
        ('w:rPr/w:fitText', 'w:rPr/(w:sz,w:fitText)'),
        ('w:rPr/w:vertAlign', 'w:rPr/(w:sz,w:vertAlign)'),
        ('w:rPr/w:rtl', 'w:rPr/(w:sz,w:rtl)'),
        ('w:rPr/w:cs', 'w:rPr/(w:sz,w:cs)'),
        ('w:rPr/w:em', 'w:rPr/(w:sz,w:em)'),
        ('w:rPr/w:lang', 'w:rPr/(w:sz,w:lang)'),
        ('w:rPr/w:eastAsianLayout', 'w:rPr/(w:sz,w:eastAsianLayout)'),
        ('w:rPr/w:specVanish', 'w:rPr/(w:sz,w:specVanish)'),
        ('w:rPr/w:oMath', 'w:rPr/(w:sz,w:oMath)'),
        ('w:rPr/w:rPrChange', 'w:rPr/(w:sz,w:rPrChange)')
    ])
    def add_sz_fixture(self, request):
        return self.add_x_fixture(request)

    @pytest.fixture(params=[
        ('w:rPr/w:rStyle', 'w:rPr/(w:rStyle,w:szCs)'),
        ('w:rPr/w:rFonts', 'w:rPr/(w:rFonts,w:szCs)'),
        ('w:rPr/w:b', 'w:rPr/(w:b,w:szCs)'),
        ('w:rPr/w:bCs', 'w:rPr/(w:bCs,w:szCs)'),
        ('w:rPr/w:i', 'w:rPr/(w:i,w:szCs)'),
        ('w:rPr/w:iCs', 'w:rPr/(w:iCs,w:szCs)'),
        ('w:rPr/w:caps', 'w:rPr/(w:caps,w:szCs)'),
        ('w:rPr/w:smallCaps', 'w:rPr/(w:smallCaps,w:szCs)'),
        ('w:rPr/w:strike', 'w:rPr/(w:strike,w:szCs)'),
        ('w:rPr/w:dstrike', 'w:rPr/(w:dstrike,w:szCs)'),
        ('w:rPr/w:outline', 'w:rPr/(w:outline,w:szCs)'),
        ('w:rPr/w:shadow', 'w:rPr/(w:shadow,w:szCs)'),
        ('w:rPr/w:emboss', 'w:rPr/(w:emboss,w:szCs)'),
        ('w:rPr/w:imprint', 'w:rPr/(w:imprint,w:szCs)'),
        ('w:rPr/w:noProof', 'w:rPr/(w:noProof,w:szCs)'),
        ('w:rPr/w:snapToGrid', 'w:rPr/(w:snapToGrid,w:szCs)'),
        ('w:rPr/w:vanish', 'w:rPr/(w:vanish,w:szCs)'),
        ('w:rPr/w:webHidden', 'w:rPr/(w:webHidden,w:szCs)'),
        ('w:rPr/w:color', 'w:rPr/(w:color,w:szCs)'),
        ('w:rPr/w:spacing', 'w:rPr/(w:spacing,w:szCs)'),
        ('w:rPr/w:w', 'w:rPr/(w:w,w:szCs)'),
        ('w:rPr/w:kern', 'w:rPr/(w:kern,w:szCs)'),
        ('w:rPr/w:position', 'w:rPr/(w:position,w:szCs)'),
        ('w:rPr/w:sz', 'w:rPr/(w:sz,w:szCs)'),
        ('w:rPr/w:highlight', 'w:rPr/(w:szCs,w:highlight)'),
        ('w:rPr/w:u', 'w:rPr/(w:szCs,w:u)'),
        ('w:rPr/w:effect', 'w:rPr/(w:szCs,w:effect)'),
        ('w:rPr/w:bdr', 'w:rPr/(w:szCs,w:bdr)'),
        ('w:rPr/w:shd', 'w:rPr/(w:szCs,w:shd)'),
        ('w:rPr/w:fitText', 'w:rPr/(w:szCs,w:fitText)'),
        ('w:rPr/w:vertAlign', 'w:rPr/(w:szCs,w:vertAlign)'),
        ('w:rPr/w:rtl', 'w:rPr/(w:szCs,w:rtl)'),
        ('w:rPr/w:cs', 'w:rPr/(w:szCs,w:cs)'),
        ('w:rPr/w:em', 'w:rPr/(w:szCs,w:em)'),
        ('w:rPr/w:lang', 'w:rPr/(w:szCs,w:lang)'),
        ('w:rPr/w:eastAsianLayout', 'w:rPr/(w:szCs,w:eastAsianLayout)'),
        ('w:rPr/w:specVanish', 'w:rPr/(w:szCs,w:specVanish)'),
        ('w:rPr/w:oMath', 'w:rPr/(w:szCs,w:oMath)'),
        ('w:rPr/w:rPrChange', 'w:rPr/(w:szCs,w:rPrChange)')
    ])
    def add_szCs_fixture(self, request):
        return self.add_x_fixture(request)

    @pytest.fixture(params=[
        ('w:rPr/w:rStyle', 'w:rPr/(w:rStyle,w:highlight)'),
        ('w:rPr/w:rFonts', 'w:rPr/(w:rFonts,w:highlight)'),
        ('w:rPr/w:b', 'w:rPr/(w:b,w:highlight)'),
        ('w:rPr/w:bCs', 'w:rPr/(w:bCs,w:highlight)'),
        ('w:rPr/w:i', 'w:rPr/(w:i,w:highlight)'),
        ('w:rPr/w:iCs', 'w:rPr/(w:iCs,w:highlight)'),
        ('w:rPr/w:caps', 'w:rPr/(w:caps,w:highlight)'),
        ('w:rPr/w:smallCaps', 'w:rPr/(w:smallCaps,w:highlight)'),
        ('w:rPr/w:strike', 'w:rPr/(w:strike,w:highlight)'),
        ('w:rPr/w:dstrike', 'w:rPr/(w:dstrike,w:highlight)'),
        ('w:rPr/w:outline', 'w:rPr/(w:outline,w:highlight)'),
        ('w:rPr/w:shadow', 'w:rPr/(w:shadow,w:highlight)'),
        ('w:rPr/w:emboss', 'w:rPr/(w:emboss,w:highlight)'),
        ('w:rPr/w:imprint', 'w:rPr/(w:imprint,w:highlight)'),
        ('w:rPr/w:noProof', 'w:rPr/(w:noProof,w:highlight)'),
        ('w:rPr/w:snapToGrid', 'w:rPr/(w:snapToGrid,w:highlight)'),
        ('w:rPr/w:vanish', 'w:rPr/(w:vanish,w:highlight)'),
        ('w:rPr/w:webHidden', 'w:rPr/(w:webHidden,w:highlight)'),
        ('w:rPr/w:color', 'w:rPr/(w:color,w:highlight)'),
        ('w:rPr/w:spacing', 'w:rPr/(w:spacing,w:highlight)'),
        ('w:rPr/w:w', 'w:rPr/(w:w,w:highlight)'),
        ('w:rPr/w:kern', 'w:rPr/(w:kern,w:highlight)'),
        ('w:rPr/w:position', 'w:rPr/(w:position,w:highlight)'),
        ('w:rPr/w:sz', 'w:rPr/(w:sz,w:highlight)'),
        ('w:rPr/w:szCs', 'w:rPr/(w:szCs,w:highlight)'),
        ('w:rPr/w:u', 'w:rPr/(w:highlight,w:u)'),
        ('w:rPr/w:effect', 'w:rPr/(w:highlight,w:effect)'),
        ('w:rPr/w:bdr', 'w:rPr/(w:highlight,w:bdr)'),
        ('w:rPr/w:shd', 'w:rPr/(w:highlight,w:shd)'),
        ('w:rPr/w:fitText', 'w:rPr/(w:highlight,w:fitText)'),
        ('w:rPr/w:vertAlign', 'w:rPr/(w:highlight,w:vertAlign)'),
        ('w:rPr/w:rtl', 'w:rPr/(w:highlight,w:rtl)'),
        ('w:rPr/w:cs', 'w:rPr/(w:highlight,w:cs)'),
        ('w:rPr/w:em', 'w:rPr/(w:highlight,w:em)'),
        ('w:rPr/w:lang', 'w:rPr/(w:highlight,w:lang)'),
        ('w:rPr/w:eastAsianLayout', 'w:rPr/(w:highlight,w:eastAsianLayout)'),
        ('w:rPr/w:specVanish', 'w:rPr/(w:highlight,w:specVanish)'),
        ('w:rPr/w:oMath', 'w:rPr/(w:highlight,w:oMath)'),
        ('w:rPr/w:rPrChange', 'w:rPr/(w:highlight,w:rPrChange)')
    ])
    def add_highlight_fixture(self, request):
        return self.add_x_fixture(request)

    @pytest.fixture(params=[
        ('w:rPr/w:rStyle', 'w:rPr/(w:rStyle,w:u)'),
        ('w:rPr/w:rFonts', 'w:rPr/(w:rFonts,w:u)'),
        ('w:rPr/w:b', 'w:rPr/(w:b,w:u)'),
        ('w:rPr/w:bCs', 'w:rPr/(w:bCs,w:u)'),
        ('w:rPr/w:i', 'w:rPr/(w:i,w:u)'),
        ('w:rPr/w:iCs', 'w:rPr/(w:iCs,w:u)'),
        ('w:rPr/w:caps', 'w:rPr/(w:caps,w:u)'),
        ('w:rPr/w:smallCaps', 'w:rPr/(w:smallCaps,w:u)'),
        ('w:rPr/w:strike', 'w:rPr/(w:strike,w:u)'),
        ('w:rPr/w:dstrike', 'w:rPr/(w:dstrike,w:u)'),
        ('w:rPr/w:outline', 'w:rPr/(w:outline,w:u)'),
        ('w:rPr/w:shadow', 'w:rPr/(w:shadow,w:u)'),
        ('w:rPr/w:emboss', 'w:rPr/(w:emboss,w:u)'),
        ('w:rPr/w:imprint', 'w:rPr/(w:imprint,w:u)'),
        ('w:rPr/w:noProof', 'w:rPr/(w:noProof,w:u)'),
        ('w:rPr/w:snapToGrid', 'w:rPr/(w:snapToGrid,w:u)'),
        ('w:rPr/w:vanish', 'w:rPr/(w:vanish,w:u)'),
        ('w:rPr/w:webHidden', 'w:rPr/(w:webHidden,w:u)'),
        ('w:rPr/w:color', 'w:rPr/(w:color,w:u)'),
        ('w:rPr/w:spacing', 'w:rPr/(w:spacing,w:u)'),
        ('w:rPr/w:w', 'w:rPr/(w:w,w:u)'),
        ('w:rPr/w:kern', 'w:rPr/(w:kern,w:u)'),
        ('w:rPr/w:position', 'w:rPr/(w:position,w:u)'),
        ('w:rPr/w:sz', 'w:rPr/(w:sz,w:u)'),
        ('w:rPr/w:szCs', 'w:rPr/(w:szCs,w:u)'),
        ('w:rPr/w:highlight', 'w:rPr/(w:highlight,w:u)'),
        ('w:rPr/w:effect', 'w:rPr/(w:u,w:effect)'),
        ('w:rPr/w:bdr', 'w:rPr/(w:u,w:bdr)'),
        ('w:rPr/w:shd', 'w:rPr/(w:u,w:shd)'),
        ('w:rPr/w:fitText', 'w:rPr/(w:u,w:fitText)'),
        ('w:rPr/w:vertAlign', 'w:rPr/(w:u,w:vertAlign)'),
        ('w:rPr/w:rtl', 'w:rPr/(w:u,w:rtl)'),
        ('w:rPr/w:cs', 'w:rPr/(w:u,w:cs)'),
        ('w:rPr/w:em', 'w:rPr/(w:u,w:em)'),
        ('w:rPr/w:lang', 'w:rPr/(w:u,w:lang)'),
        ('w:rPr/w:eastAsianLayout', 'w:rPr/(w:u,w:eastAsianLayout)'),
        ('w:rPr/w:specVanish', 'w:rPr/(w:u,w:specVanish)'),
        ('w:rPr/w:oMath', 'w:rPr/(w:u,w:oMath)'),
        ('w:rPr/w:rPrChange', 'w:rPr/(w:u,w:rPrChange)')
    ])
    def add_u_fixture(self, request):
        return self.add_x_fixture(request)

    @pytest.fixture(params=[
        ('w:rPr/w:rStyle', 'w:rPr/(w:rStyle,w:effect)'),
        ('w:rPr/w:rFonts', 'w:rPr/(w:rFonts,w:effect)'),
        ('w:rPr/w:b', 'w:rPr/(w:b,w:effect)'),
        ('w:rPr/w:bCs', 'w:rPr/(w:bCs,w:effect)'),
        ('w:rPr/w:i', 'w:rPr/(w:i,w:effect)'),
        ('w:rPr/w:iCs', 'w:rPr/(w:iCs,w:effect)'),
        ('w:rPr/w:caps', 'w:rPr/(w:caps,w:effect)'),
        ('w:rPr/w:smallCaps', 'w:rPr/(w:smallCaps,w:effect)'),
        ('w:rPr/w:strike', 'w:rPr/(w:strike,w:effect)'),
        ('w:rPr/w:dstrike', 'w:rPr/(w:dstrike,w:effect)'),
        ('w:rPr/w:outline', 'w:rPr/(w:outline,w:effect)'),
        ('w:rPr/w:shadow', 'w:rPr/(w:shadow,w:effect)'),
        ('w:rPr/w:emboss', 'w:rPr/(w:emboss,w:effect)'),
        ('w:rPr/w:imprint', 'w:rPr/(w:imprint,w:effect)'),
        ('w:rPr/w:noProof', 'w:rPr/(w:noProof,w:effect)'),
        ('w:rPr/w:snapToGrid', 'w:rPr/(w:snapToGrid,w:effect)'),
        ('w:rPr/w:vanish', 'w:rPr/(w:vanish,w:effect)'),
        ('w:rPr/w:webHidden', 'w:rPr/(w:webHidden,w:effect)'),
        ('w:rPr/w:color', 'w:rPr/(w:color,w:effect)'),
        ('w:rPr/w:spacing', 'w:rPr/(w:spacing,w:effect)'),
        ('w:rPr/w:w', 'w:rPr/(w:w,w:effect)'),
        ('w:rPr/w:kern', 'w:rPr/(w:kern,w:effect)'),
        ('w:rPr/w:position', 'w:rPr/(w:position,w:effect)'),
        ('w:rPr/w:sz', 'w:rPr/(w:sz,w:effect)'),
        ('w:rPr/w:szCs', 'w:rPr/(w:szCs,w:effect)'),
        ('w:rPr/w:highlight', 'w:rPr/(w:highlight,w:effect)'),
        ('w:rPr/w:u', 'w:rPr/(w:u,w:effect)'),
        ('w:rPr/w:bdr', 'w:rPr/(w:effect,w:bdr)'),
        ('w:rPr/w:shd', 'w:rPr/(w:effect,w:shd)'),
        ('w:rPr/w:fitText', 'w:rPr/(w:effect,w:fitText)'),
        ('w:rPr/w:vertAlign', 'w:rPr/(w:effect,w:vertAlign)'),
        ('w:rPr/w:rtl', 'w:rPr/(w:effect,w:rtl)'),
        ('w:rPr/w:cs', 'w:rPr/(w:effect,w:cs)'),
        ('w:rPr/w:em', 'w:rPr/(w:effect,w:em)'),
        ('w:rPr/w:lang', 'w:rPr/(w:effect,w:lang)'),
        ('w:rPr/w:eastAsianLayout', 'w:rPr/(w:effect,w:eastAsianLayout)'),
        ('w:rPr/w:specVanish', 'w:rPr/(w:effect,w:specVanish)'),
        ('w:rPr/w:oMath', 'w:rPr/(w:effect,w:oMath)'),
        ('w:rPr/w:rPrChange', 'w:rPr/(w:effect,w:rPrChange)')
    ])
    def add_effect_fixture(self, request):
        return self.add_x_fixture(request)

    @pytest.fixture(params=[
        ('w:rPr/w:rStyle', 'w:rPr/(w:rStyle,w:bdr)'),
        ('w:rPr/w:rFonts', 'w:rPr/(w:rFonts,w:bdr)'),
        ('w:rPr/w:b', 'w:rPr/(w:b,w:bdr)'),
        ('w:rPr/w:bCs', 'w:rPr/(w:bCs,w:bdr)'),
        ('w:rPr/w:i', 'w:rPr/(w:i,w:bdr)'),
        ('w:rPr/w:iCs', 'w:rPr/(w:iCs,w:bdr)'),
        ('w:rPr/w:caps', 'w:rPr/(w:caps,w:bdr)'),
        ('w:rPr/w:smallCaps', 'w:rPr/(w:smallCaps,w:bdr)'),
        ('w:rPr/w:strike', 'w:rPr/(w:strike,w:bdr)'),
        ('w:rPr/w:dstrike', 'w:rPr/(w:dstrike,w:bdr)'),
        ('w:rPr/w:outline', 'w:rPr/(w:outline,w:bdr)'),
        ('w:rPr/w:shadow', 'w:rPr/(w:shadow,w:bdr)'),
        ('w:rPr/w:emboss', 'w:rPr/(w:emboss,w:bdr)'),
        ('w:rPr/w:imprint', 'w:rPr/(w:imprint,w:bdr)'),
        ('w:rPr/w:noProof', 'w:rPr/(w:noProof,w:bdr)'),
        ('w:rPr/w:snapToGrid', 'w:rPr/(w:snapToGrid,w:bdr)'),
        ('w:rPr/w:vanish', 'w:rPr/(w:vanish,w:bdr)'),
        ('w:rPr/w:webHidden', 'w:rPr/(w:webHidden,w:bdr)'),
        ('w:rPr/w:color', 'w:rPr/(w:color,w:bdr)'),
        ('w:rPr/w:spacing', 'w:rPr/(w:spacing,w:bdr)'),
        ('w:rPr/w:w', 'w:rPr/(w:w,w:bdr)'),
        ('w:rPr/w:kern', 'w:rPr/(w:kern,w:bdr)'),
        ('w:rPr/w:position', 'w:rPr/(w:position,w:bdr)'),
        ('w:rPr/w:sz', 'w:rPr/(w:sz,w:bdr)'),
        ('w:rPr/w:szCs', 'w:rPr/(w:szCs,w:bdr)'),
        ('w:rPr/w:highlight', 'w:rPr/(w:highlight,w:bdr)'),
        ('w:rPr/w:u', 'w:rPr/(w:u,w:bdr)'),
        ('w:rPr/w:effect', 'w:rPr/(w:effect,w:bdr)'),
        ('w:rPr/w:shd', 'w:rPr/(w:bdr,w:shd)'),
        ('w:rPr/w:fitText', 'w:rPr/(w:bdr,w:fitText)'),
        ('w:rPr/w:vertAlign', 'w:rPr/(w:bdr,w:vertAlign)'),
        ('w:rPr/w:rtl', 'w:rPr/(w:bdr,w:rtl)'),
        ('w:rPr/w:cs', 'w:rPr/(w:bdr,w:cs)'),
        ('w:rPr/w:em', 'w:rPr/(w:bdr,w:em)'),
        ('w:rPr/w:lang', 'w:rPr/(w:bdr,w:lang)'),
        ('w:rPr/w:eastAsianLayout', 'w:rPr/(w:bdr,w:eastAsianLayout)'),
        ('w:rPr/w:specVanish', 'w:rPr/(w:bdr,w:specVanish)'),
        ('w:rPr/w:oMath', 'w:rPr/(w:bdr,w:oMath)'),
        ('w:rPr/w:rPrChange', 'w:rPr/(w:bdr,w:rPrChange)')
    ])
    def add_bdr_fixture(self, request):
        return self.add_x_fixture(request)

    @pytest.fixture(params=[
        ('w:rPr/w:rStyle', 'w:rPr/(w:rStyle,w:shd)'),
        ('w:rPr/w:rFonts', 'w:rPr/(w:rFonts,w:shd)'),
        ('w:rPr/w:b', 'w:rPr/(w:b,w:shd)'),
        ('w:rPr/w:bCs', 'w:rPr/(w:bCs,w:shd)'),
        ('w:rPr/w:i', 'w:rPr/(w:i,w:shd)'),
        ('w:rPr/w:iCs', 'w:rPr/(w:iCs,w:shd)'),
        ('w:rPr/w:caps', 'w:rPr/(w:caps,w:shd)'),
        ('w:rPr/w:smallCaps', 'w:rPr/(w:smallCaps,w:shd)'),
        ('w:rPr/w:strike', 'w:rPr/(w:strike,w:shd)'),
        ('w:rPr/w:dstrike', 'w:rPr/(w:dstrike,w:shd)'),
        ('w:rPr/w:outline', 'w:rPr/(w:outline,w:shd)'),
        ('w:rPr/w:shadow', 'w:rPr/(w:shadow,w:shd)'),
        ('w:rPr/w:emboss', 'w:rPr/(w:emboss,w:shd)'),
        ('w:rPr/w:imprint', 'w:rPr/(w:imprint,w:shd)'),
        ('w:rPr/w:noProof', 'w:rPr/(w:noProof,w:shd)'),
        ('w:rPr/w:snapToGrid', 'w:rPr/(w:snapToGrid,w:shd)'),
        ('w:rPr/w:vanish', 'w:rPr/(w:vanish,w:shd)'),
        ('w:rPr/w:webHidden', 'w:rPr/(w:webHidden,w:shd)'),
        ('w:rPr/w:color', 'w:rPr/(w:color,w:shd)'),
        ('w:rPr/w:spacing', 'w:rPr/(w:spacing,w:shd)'),
        ('w:rPr/w:w', 'w:rPr/(w:w,w:shd)'),
        ('w:rPr/w:kern', 'w:rPr/(w:kern,w:shd)'),
        ('w:rPr/w:position', 'w:rPr/(w:position,w:shd)'),
        ('w:rPr/w:sz', 'w:rPr/(w:sz,w:shd)'),
        ('w:rPr/w:szCs', 'w:rPr/(w:szCs,w:shd)'),
        ('w:rPr/w:highlight', 'w:rPr/(w:highlight,w:shd)'),
        ('w:rPr/w:u', 'w:rPr/(w:u,w:shd)'),
        ('w:rPr/w:effect', 'w:rPr/(w:effect,w:shd)'),
        ('w:rPr/w:bdr', 'w:rPr/(w:bdr,w:shd)'),
        ('w:rPr/w:fitText', 'w:rPr/(w:shd,w:fitText)'),
        ('w:rPr/w:vertAlign', 'w:rPr/(w:shd,w:vertAlign)'),
        ('w:rPr/w:rtl', 'w:rPr/(w:shd,w:rtl)'),
        ('w:rPr/w:cs', 'w:rPr/(w:shd,w:cs)'),
        ('w:rPr/w:em', 'w:rPr/(w:shd,w:em)'),
        ('w:rPr/w:lang', 'w:rPr/(w:shd,w:lang)'),
        ('w:rPr/w:eastAsianLayout', 'w:rPr/(w:shd,w:eastAsianLayout)'),
        ('w:rPr/w:specVanish', 'w:rPr/(w:shd,w:specVanish)'),
        ('w:rPr/w:oMath', 'w:rPr/(w:shd,w:oMath)'),
        ('w:rPr/w:rPrChange', 'w:rPr/(w:shd,w:rPrChange)')
    ])
    def add_shd_fixture(self, request):
        return self.add_x_fixture(request)

    @pytest.fixture(params=[
        ('w:rPr/w:rStyle', 'w:rPr/(w:rStyle,w:fitText)'),
        ('w:rPr/w:rFonts', 'w:rPr/(w:rFonts,w:fitText)'),
        ('w:rPr/w:b', 'w:rPr/(w:b,w:fitText)'),
        ('w:rPr/w:bCs', 'w:rPr/(w:bCs,w:fitText)'),
        ('w:rPr/w:i', 'w:rPr/(w:i,w:fitText)'),
        ('w:rPr/w:iCs', 'w:rPr/(w:iCs,w:fitText)'),
        ('w:rPr/w:caps', 'w:rPr/(w:caps,w:fitText)'),
        ('w:rPr/w:smallCaps', 'w:rPr/(w:smallCaps,w:fitText)'),
        ('w:rPr/w:strike', 'w:rPr/(w:strike,w:fitText)'),
        ('w:rPr/w:dstrike', 'w:rPr/(w:dstrike,w:fitText)'),
        ('w:rPr/w:outline', 'w:rPr/(w:outline,w:fitText)'),
        ('w:rPr/w:shadow', 'w:rPr/(w:shadow,w:fitText)'),
        ('w:rPr/w:emboss', 'w:rPr/(w:emboss,w:fitText)'),
        ('w:rPr/w:imprint', 'w:rPr/(w:imprint,w:fitText)'),
        ('w:rPr/w:noProof', 'w:rPr/(w:noProof,w:fitText)'),
        ('w:rPr/w:snapToGrid', 'w:rPr/(w:snapToGrid,w:fitText)'),
        ('w:rPr/w:vanish', 'w:rPr/(w:vanish,w:fitText)'),
        ('w:rPr/w:webHidden', 'w:rPr/(w:webHidden,w:fitText)'),
        ('w:rPr/w:color', 'w:rPr/(w:color,w:fitText)'),
        ('w:rPr/w:spacing', 'w:rPr/(w:spacing,w:fitText)'),
        ('w:rPr/w:w', 'w:rPr/(w:w,w:fitText)'),
        ('w:rPr/w:kern', 'w:rPr/(w:kern,w:fitText)'),
        ('w:rPr/w:position', 'w:rPr/(w:position,w:fitText)'),
        ('w:rPr/w:sz', 'w:rPr/(w:sz,w:fitText)'),
        ('w:rPr/w:szCs', 'w:rPr/(w:szCs,w:fitText)'),
        ('w:rPr/w:highlight', 'w:rPr/(w:highlight,w:fitText)'),
        ('w:rPr/w:u', 'w:rPr/(w:u,w:fitText)'),
        ('w:rPr/w:effect', 'w:rPr/(w:effect,w:fitText)'),
        ('w:rPr/w:bdr', 'w:rPr/(w:bdr,w:fitText)'),
        ('w:rPr/w:shd', 'w:rPr/(w:shd,w:fitText)'),
        ('w:rPr/w:vertAlign', 'w:rPr/(w:fitText,w:vertAlign)'),
        ('w:rPr/w:rtl', 'w:rPr/(w:fitText,w:rtl)'),
        ('w:rPr/w:cs', 'w:rPr/(w:fitText,w:cs)'),
        ('w:rPr/w:em', 'w:rPr/(w:fitText,w:em)'),
        ('w:rPr/w:lang', 'w:rPr/(w:fitText,w:lang)'),
        ('w:rPr/w:eastAsianLayout', 'w:rPr/(w:fitText,w:eastAsianLayout)'),
        ('w:rPr/w:specVanish', 'w:rPr/(w:fitText,w:specVanish)'),
        ('w:rPr/w:oMath', 'w:rPr/(w:fitText,w:oMath)'),
        ('w:rPr/w:rPrChange', 'w:rPr/(w:fitText,w:rPrChange)')
    ])
    def add_fitText_fixture(self, request):
        return self.add_x_fixture(request)

    @pytest.fixture(params=[
        ('w:rPr/w:rStyle', 'w:rPr/(w:rStyle,w:vertAlign)'),
        ('w:rPr/w:rFonts', 'w:rPr/(w:rFonts,w:vertAlign)'),
        ('w:rPr/w:b', 'w:rPr/(w:b,w:vertAlign)'),
        ('w:rPr/w:bCs', 'w:rPr/(w:bCs,w:vertAlign)'),
        ('w:rPr/w:i', 'w:rPr/(w:i,w:vertAlign)'),
        ('w:rPr/w:iCs', 'w:rPr/(w:iCs,w:vertAlign)'),
        ('w:rPr/w:caps', 'w:rPr/(w:caps,w:vertAlign)'),
        ('w:rPr/w:smallCaps', 'w:rPr/(w:smallCaps,w:vertAlign)'),
        ('w:rPr/w:strike', 'w:rPr/(w:strike,w:vertAlign)'),
        ('w:rPr/w:dstrike', 'w:rPr/(w:dstrike,w:vertAlign)'),
        ('w:rPr/w:outline', 'w:rPr/(w:outline,w:vertAlign)'),
        ('w:rPr/w:shadow', 'w:rPr/(w:shadow,w:vertAlign)'),
        ('w:rPr/w:emboss', 'w:rPr/(w:emboss,w:vertAlign)'),
        ('w:rPr/w:imprint', 'w:rPr/(w:imprint,w:vertAlign)'),
        ('w:rPr/w:noProof', 'w:rPr/(w:noProof,w:vertAlign)'),
        ('w:rPr/w:snapToGrid', 'w:rPr/(w:snapToGrid,w:vertAlign)'),
        ('w:rPr/w:vanish', 'w:rPr/(w:vanish,w:vertAlign)'),
        ('w:rPr/w:webHidden', 'w:rPr/(w:webHidden,w:vertAlign)'),
        ('w:rPr/w:color', 'w:rPr/(w:color,w:vertAlign)'),
        ('w:rPr/w:spacing', 'w:rPr/(w:spacing,w:vertAlign)'),
        ('w:rPr/w:w', 'w:rPr/(w:w,w:vertAlign)'),
        ('w:rPr/w:kern', 'w:rPr/(w:kern,w:vertAlign)'),
        ('w:rPr/w:position', 'w:rPr/(w:position,w:vertAlign)'),
        ('w:rPr/w:sz', 'w:rPr/(w:sz,w:vertAlign)'),
        ('w:rPr/w:szCs', 'w:rPr/(w:szCs,w:vertAlign)'),
        ('w:rPr/w:highlight', 'w:rPr/(w:highlight,w:vertAlign)'),
        ('w:rPr/w:u', 'w:rPr/(w:u,w:vertAlign)'),
        ('w:rPr/w:effect', 'w:rPr/(w:effect,w:vertAlign)'),
        ('w:rPr/w:bdr', 'w:rPr/(w:bdr,w:vertAlign)'),
        ('w:rPr/w:shd', 'w:rPr/(w:shd,w:vertAlign)'),
        ('w:rPr/w:fitText', 'w:rPr/(w:fitText,w:vertAlign)'),
        ('w:rPr/w:rtl', 'w:rPr/(w:vertAlign,w:rtl)'),
        ('w:rPr/w:cs', 'w:rPr/(w:vertAlign,w:cs)'),
        ('w:rPr/w:em', 'w:rPr/(w:vertAlign,w:em)'),
        ('w:rPr/w:lang', 'w:rPr/(w:vertAlign,w:lang)'),
        ('w:rPr/w:eastAsianLayout', 'w:rPr/(w:vertAlign,w:eastAsianLayout)'),
        ('w:rPr/w:specVanish', 'w:rPr/(w:vertAlign,w:specVanish)'),
        ('w:rPr/w:oMath', 'w:rPr/(w:vertAlign,w:oMath)'),
        ('w:rPr/w:rPrChange', 'w:rPr/(w:vertAlign,w:rPrChange)')
    ])
    def add_vertAlign_fixture(self, request):
        return self.add_x_fixture(request)

    @pytest.fixture(params=[
        ('w:rPr/w:rStyle', 'w:rPr/(w:rStyle,w:rtl)'),
        ('w:rPr/w:rFonts', 'w:rPr/(w:rFonts,w:rtl)'),
        ('w:rPr/w:b', 'w:rPr/(w:b,w:rtl)'),
        ('w:rPr/w:bCs', 'w:rPr/(w:bCs,w:rtl)'),
        ('w:rPr/w:i', 'w:rPr/(w:i,w:rtl)'),
        ('w:rPr/w:iCs', 'w:rPr/(w:iCs,w:rtl)'),
        ('w:rPr/w:caps', 'w:rPr/(w:caps,w:rtl)'),
        ('w:rPr/w:smallCaps', 'w:rPr/(w:smallCaps,w:rtl)'),
        ('w:rPr/w:strike', 'w:rPr/(w:strike,w:rtl)'),
        ('w:rPr/w:dstrike', 'w:rPr/(w:dstrike,w:rtl)'),
        ('w:rPr/w:outline', 'w:rPr/(w:outline,w:rtl)'),
        ('w:rPr/w:shadow', 'w:rPr/(w:shadow,w:rtl)'),
        ('w:rPr/w:emboss', 'w:rPr/(w:emboss,w:rtl)'),
        ('w:rPr/w:imprint', 'w:rPr/(w:imprint,w:rtl)'),
        ('w:rPr/w:noProof', 'w:rPr/(w:noProof,w:rtl)'),
        ('w:rPr/w:snapToGrid', 'w:rPr/(w:snapToGrid,w:rtl)'),
        ('w:rPr/w:vanish', 'w:rPr/(w:vanish,w:rtl)'),
        ('w:rPr/w:webHidden', 'w:rPr/(w:webHidden,w:rtl)'),
        ('w:rPr/w:color', 'w:rPr/(w:color,w:rtl)'),
        ('w:rPr/w:spacing', 'w:rPr/(w:spacing,w:rtl)'),
        ('w:rPr/w:w', 'w:rPr/(w:w,w:rtl)'),
        ('w:rPr/w:kern', 'w:rPr/(w:kern,w:rtl)'),
        ('w:rPr/w:position', 'w:rPr/(w:position,w:rtl)'),
        ('w:rPr/w:sz', 'w:rPr/(w:sz,w:rtl)'),
        ('w:rPr/w:szCs', 'w:rPr/(w:szCs,w:rtl)'),
        ('w:rPr/w:highlight', 'w:rPr/(w:highlight,w:rtl)'),
        ('w:rPr/w:u', 'w:rPr/(w:u,w:rtl)'),
        ('w:rPr/w:effect', 'w:rPr/(w:effect,w:rtl)'),
        ('w:rPr/w:bdr', 'w:rPr/(w:bdr,w:rtl)'),
        ('w:rPr/w:shd', 'w:rPr/(w:shd,w:rtl)'),
        ('w:rPr/w:fitText', 'w:rPr/(w:fitText,w:rtl)'),
        ('w:rPr/w:vertAlign', 'w:rPr/(w:vertAlign,w:rtl)'),
        ('w:rPr/w:cs', 'w:rPr/(w:rtl,w:cs)'),
        ('w:rPr/w:em', 'w:rPr/(w:rtl,w:em)'),
        ('w:rPr/w:lang', 'w:rPr/(w:rtl,w:lang)'),
        ('w:rPr/w:eastAsianLayout', 'w:rPr/(w:rtl,w:eastAsianLayout)'),
        ('w:rPr/w:specVanish', 'w:rPr/(w:rtl,w:specVanish)'),
        ('w:rPr/w:oMath', 'w:rPr/(w:rtl,w:oMath)'),
        ('w:rPr/w:rPrChange', 'w:rPr/(w:rtl,w:rPrChange)')
    ])
    def add_rtl_fixture(self, request):
        return self.add_x_fixture(request)

    @pytest.fixture(params=[
        ('w:rPr/w:rStyle', 'w:rPr/(w:rStyle,w:cs)'),
        ('w:rPr/w:rFonts', 'w:rPr/(w:rFonts,w:cs)'),
        ('w:rPr/w:b', 'w:rPr/(w:b,w:cs)'),
        ('w:rPr/w:bCs', 'w:rPr/(w:bCs,w:cs)'),
        ('w:rPr/w:i', 'w:rPr/(w:i,w:cs)'),
        ('w:rPr/w:iCs', 'w:rPr/(w:iCs,w:cs)'),
        ('w:rPr/w:caps', 'w:rPr/(w:caps,w:cs)'),
        ('w:rPr/w:smallCaps', 'w:rPr/(w:smallCaps,w:cs)'),
        ('w:rPr/w:strike', 'w:rPr/(w:strike,w:cs)'),
        ('w:rPr/w:dstrike', 'w:rPr/(w:dstrike,w:cs)'),
        ('w:rPr/w:outline', 'w:rPr/(w:outline,w:cs)'),
        ('w:rPr/w:shadow', 'w:rPr/(w:shadow,w:cs)'),
        ('w:rPr/w:emboss', 'w:rPr/(w:emboss,w:cs)'),
        ('w:rPr/w:imprint', 'w:rPr/(w:imprint,w:cs)'),
        ('w:rPr/w:noProof', 'w:rPr/(w:noProof,w:cs)'),
        ('w:rPr/w:snapToGrid', 'w:rPr/(w:snapToGrid,w:cs)'),
        ('w:rPr/w:vanish', 'w:rPr/(w:vanish,w:cs)'),
        ('w:rPr/w:webHidden', 'w:rPr/(w:webHidden,w:cs)'),
        ('w:rPr/w:color', 'w:rPr/(w:color,w:cs)'),
        ('w:rPr/w:spacing', 'w:rPr/(w:spacing,w:cs)'),
        ('w:rPr/w:w', 'w:rPr/(w:w,w:cs)'),
        ('w:rPr/w:kern', 'w:rPr/(w:kern,w:cs)'),
        ('w:rPr/w:position', 'w:rPr/(w:position,w:cs)'),
        ('w:rPr/w:sz', 'w:rPr/(w:sz,w:cs)'),
        ('w:rPr/w:szCs', 'w:rPr/(w:szCs,w:cs)'),
        ('w:rPr/w:highlight', 'w:rPr/(w:highlight,w:cs)'),
        ('w:rPr/w:u', 'w:rPr/(w:u,w:cs)'),
        ('w:rPr/w:effect', 'w:rPr/(w:effect,w:cs)'),
        ('w:rPr/w:bdr', 'w:rPr/(w:bdr,w:cs)'),
        ('w:rPr/w:shd', 'w:rPr/(w:shd,w:cs)'),
        ('w:rPr/w:fitText', 'w:rPr/(w:fitText,w:cs)'),
        ('w:rPr/w:vertAlign', 'w:rPr/(w:vertAlign,w:cs)'),
        ('w:rPr/w:rtl', 'w:rPr/(w:rtl,w:cs)'),
        ('w:rPr/w:em', 'w:rPr/(w:cs,w:em)'),
        ('w:rPr/w:lang', 'w:rPr/(w:cs,w:lang)'),
        ('w:rPr/w:eastAsianLayout', 'w:rPr/(w:cs,w:eastAsianLayout)'),
        ('w:rPr/w:specVanish', 'w:rPr/(w:cs,w:specVanish)'),
        ('w:rPr/w:oMath', 'w:rPr/(w:cs,w:oMath)'),
        ('w:rPr/w:rPrChange', 'w:rPr/(w:cs,w:rPrChange)')
    ])
    def add_cs_fixture(self, request):
        return self.add_x_fixture(request)

    @pytest.fixture(params=[
        ('w:rPr/w:rStyle', 'w:rPr/(w:rStyle,w:em)'),
        ('w:rPr/w:rFonts', 'w:rPr/(w:rFonts,w:em)'),
        ('w:rPr/w:b', 'w:rPr/(w:b,w:em)'),
        ('w:rPr/w:bCs', 'w:rPr/(w:bCs,w:em)'),
        ('w:rPr/w:i', 'w:rPr/(w:i,w:em)'),
        ('w:rPr/w:iCs', 'w:rPr/(w:iCs,w:em)'),
        ('w:rPr/w:caps', 'w:rPr/(w:caps,w:em)'),
        ('w:rPr/w:smallCaps', 'w:rPr/(w:smallCaps,w:em)'),
        ('w:rPr/w:strike', 'w:rPr/(w:strike,w:em)'),
        ('w:rPr/w:dstrike', 'w:rPr/(w:dstrike,w:em)'),
        ('w:rPr/w:outline', 'w:rPr/(w:outline,w:em)'),
        ('w:rPr/w:shadow', 'w:rPr/(w:shadow,w:em)'),
        ('w:rPr/w:emboss', 'w:rPr/(w:emboss,w:em)'),
        ('w:rPr/w:imprint', 'w:rPr/(w:imprint,w:em)'),
        ('w:rPr/w:noProof', 'w:rPr/(w:noProof,w:em)'),
        ('w:rPr/w:snapToGrid', 'w:rPr/(w:snapToGrid,w:em)'),
        ('w:rPr/w:vanish', 'w:rPr/(w:vanish,w:em)'),
        ('w:rPr/w:webHidden', 'w:rPr/(w:webHidden,w:em)'),
        ('w:rPr/w:color', 'w:rPr/(w:color,w:em)'),
        ('w:rPr/w:spacing', 'w:rPr/(w:spacing,w:em)'),
        ('w:rPr/w:w', 'w:rPr/(w:w,w:em)'),
        ('w:rPr/w:kern', 'w:rPr/(w:kern,w:em)'),
        ('w:rPr/w:position', 'w:rPr/(w:position,w:em)'),
        ('w:rPr/w:sz', 'w:rPr/(w:sz,w:em)'),
        ('w:rPr/w:szCs', 'w:rPr/(w:szCs,w:em)'),
        ('w:rPr/w:highlight', 'w:rPr/(w:highlight,w:em)'),
        ('w:rPr/w:u', 'w:rPr/(w:u,w:em)'),
        ('w:rPr/w:effect', 'w:rPr/(w:effect,w:em)'),
        ('w:rPr/w:bdr', 'w:rPr/(w:bdr,w:em)'),
        ('w:rPr/w:shd', 'w:rPr/(w:shd,w:em)'),
        ('w:rPr/w:fitText', 'w:rPr/(w:fitText,w:em)'),
        ('w:rPr/w:vertAlign', 'w:rPr/(w:vertAlign,w:em)'),
        ('w:rPr/w:rtl', 'w:rPr/(w:rtl,w:em)'),
        ('w:rPr/w:cs', 'w:rPr/(w:cs,w:em)'),
        ('w:rPr/w:lang', 'w:rPr/(w:em,w:lang)'),
        ('w:rPr/w:eastAsianLayout', 'w:rPr/(w:em,w:eastAsianLayout)'),
        ('w:rPr/w:specVanish', 'w:rPr/(w:em,w:specVanish)'),
        ('w:rPr/w:oMath', 'w:rPr/(w:em,w:oMath)'),
        ('w:rPr/w:rPrChange', 'w:rPr/(w:em,w:rPrChange)')
    ])
    def add_em_fixture(self, request):
        return self.add_x_fixture(request)

    @pytest.fixture(params=[
        ('w:rPr/w:rStyle', 'w:rPr/(w:rStyle,w:lang)'),
        ('w:rPr/w:rFonts', 'w:rPr/(w:rFonts,w:lang)'),
        ('w:rPr/w:b', 'w:rPr/(w:b,w:lang)'),
        ('w:rPr/w:bCs', 'w:rPr/(w:bCs,w:lang)'),
        ('w:rPr/w:i', 'w:rPr/(w:i,w:lang)'),
        ('w:rPr/w:iCs', 'w:rPr/(w:iCs,w:lang)'),
        ('w:rPr/w:caps', 'w:rPr/(w:caps,w:lang)'),
        ('w:rPr/w:smallCaps', 'w:rPr/(w:smallCaps,w:lang)'),
        ('w:rPr/w:strike', 'w:rPr/(w:strike,w:lang)'),
        ('w:rPr/w:dstrike', 'w:rPr/(w:dstrike,w:lang)'),
        ('w:rPr/w:outline', 'w:rPr/(w:outline,w:lang)'),
        ('w:rPr/w:shadow', 'w:rPr/(w:shadow,w:lang)'),
        ('w:rPr/w:emboss', 'w:rPr/(w:emboss,w:lang)'),
        ('w:rPr/w:imprint', 'w:rPr/(w:imprint,w:lang)'),
        ('w:rPr/w:noProof', 'w:rPr/(w:noProof,w:lang)'),
        ('w:rPr/w:snapToGrid', 'w:rPr/(w:snapToGrid,w:lang)'),
        ('w:rPr/w:vanish', 'w:rPr/(w:vanish,w:lang)'),
        ('w:rPr/w:webHidden', 'w:rPr/(w:webHidden,w:lang)'),
        ('w:rPr/w:color', 'w:rPr/(w:color,w:lang)'),
        ('w:rPr/w:spacing', 'w:rPr/(w:spacing,w:lang)'),
        ('w:rPr/w:w', 'w:rPr/(w:w,w:lang)'),
        ('w:rPr/w:kern', 'w:rPr/(w:kern,w:lang)'),
        ('w:rPr/w:position', 'w:rPr/(w:position,w:lang)'),
        ('w:rPr/w:sz', 'w:rPr/(w:sz,w:lang)'),
        ('w:rPr/w:szCs', 'w:rPr/(w:szCs,w:lang)'),
        ('w:rPr/w:highlight', 'w:rPr/(w:highlight,w:lang)'),
        ('w:rPr/w:u', 'w:rPr/(w:u,w:lang)'),
        ('w:rPr/w:effect', 'w:rPr/(w:effect,w:lang)'),
        ('w:rPr/w:bdr', 'w:rPr/(w:bdr,w:lang)'),
        ('w:rPr/w:shd', 'w:rPr/(w:shd,w:lang)'),
        ('w:rPr/w:fitText', 'w:rPr/(w:fitText,w:lang)'),
        ('w:rPr/w:vertAlign', 'w:rPr/(w:vertAlign,w:lang)'),
        ('w:rPr/w:rtl', 'w:rPr/(w:rtl,w:lang)'),
        ('w:rPr/w:cs', 'w:rPr/(w:cs,w:lang)'),
        ('w:rPr/w:em', 'w:rPr/(w:em,w:lang)'),
        ('w:rPr/w:eastAsianLayout', 'w:rPr/(w:lang,w:eastAsianLayout)'),
        ('w:rPr/w:specVanish', 'w:rPr/(w:lang,w:specVanish)'),
        ('w:rPr/w:oMath', 'w:rPr/(w:lang,w:oMath)'),
        ('w:rPr/w:rPrChange', 'w:rPr/(w:lang,w:rPrChange)')
    ])
    def add_lang_fixture(self, request):
        return self.add_x_fixture(request)

    @pytest.fixture(params=[
        ('w:rPr/w:rStyle', 'w:rPr/(w:rStyle,w:eastAsianLayout)'),
        ('w:rPr/w:rFonts', 'w:rPr/(w:rFonts,w:eastAsianLayout)'),
        ('w:rPr/w:b', 'w:rPr/(w:b,w:eastAsianLayout)'),
        ('w:rPr/w:bCs', 'w:rPr/(w:bCs,w:eastAsianLayout)'),
        ('w:rPr/w:i', 'w:rPr/(w:i,w:eastAsianLayout)'),
        ('w:rPr/w:iCs', 'w:rPr/(w:iCs,w:eastAsianLayout)'),
        ('w:rPr/w:caps', 'w:rPr/(w:caps,w:eastAsianLayout)'),
        ('w:rPr/w:smallCaps', 'w:rPr/(w:smallCaps,w:eastAsianLayout)'),
        ('w:rPr/w:strike', 'w:rPr/(w:strike,w:eastAsianLayout)'),
        ('w:rPr/w:dstrike', 'w:rPr/(w:dstrike,w:eastAsianLayout)'),
        ('w:rPr/w:outline', 'w:rPr/(w:outline,w:eastAsianLayout)'),
        ('w:rPr/w:shadow', 'w:rPr/(w:shadow,w:eastAsianLayout)'),
        ('w:rPr/w:emboss', 'w:rPr/(w:emboss,w:eastAsianLayout)'),
        ('w:rPr/w:imprint', 'w:rPr/(w:imprint,w:eastAsianLayout)'),
        ('w:rPr/w:noProof', 'w:rPr/(w:noProof,w:eastAsianLayout)'),
        ('w:rPr/w:snapToGrid', 'w:rPr/(w:snapToGrid,w:eastAsianLayout)'),
        ('w:rPr/w:vanish', 'w:rPr/(w:vanish,w:eastAsianLayout)'),
        ('w:rPr/w:webHidden', 'w:rPr/(w:webHidden,w:eastAsianLayout)'),
        ('w:rPr/w:color', 'w:rPr/(w:color,w:eastAsianLayout)'),
        ('w:rPr/w:spacing', 'w:rPr/(w:spacing,w:eastAsianLayout)'),
        ('w:rPr/w:w', 'w:rPr/(w:w,w:eastAsianLayout)'),
        ('w:rPr/w:kern', 'w:rPr/(w:kern,w:eastAsianLayout)'),
        ('w:rPr/w:position', 'w:rPr/(w:position,w:eastAsianLayout)'),
        ('w:rPr/w:sz', 'w:rPr/(w:sz,w:eastAsianLayout)'),
        ('w:rPr/w:szCs', 'w:rPr/(w:szCs,w:eastAsianLayout)'),
        ('w:rPr/w:highlight', 'w:rPr/(w:highlight,w:eastAsianLayout)'),
        ('w:rPr/w:u', 'w:rPr/(w:u,w:eastAsianLayout)'),
        ('w:rPr/w:effect', 'w:rPr/(w:effect,w:eastAsianLayout)'),
        ('w:rPr/w:bdr', 'w:rPr/(w:bdr,w:eastAsianLayout)'),
        ('w:rPr/w:shd', 'w:rPr/(w:shd,w:eastAsianLayout)'),
        ('w:rPr/w:fitText', 'w:rPr/(w:fitText,w:eastAsianLayout)'),
        ('w:rPr/w:vertAlign', 'w:rPr/(w:vertAlign,w:eastAsianLayout)'),
        ('w:rPr/w:rtl', 'w:rPr/(w:rtl,w:eastAsianLayout)'),
        ('w:rPr/w:cs', 'w:rPr/(w:cs,w:eastAsianLayout)'),
        ('w:rPr/w:em', 'w:rPr/(w:em,w:eastAsianLayout)'),
        ('w:rPr/w:lang', 'w:rPr/(w:lang,w:eastAsianLayout)'),
        ('w:rPr/w:specVanish', 'w:rPr/(w:eastAsianLayout,w:specVanish)'),
        ('w:rPr/w:oMath', 'w:rPr/(w:eastAsianLayout,w:oMath)'),
        ('w:rPr/w:rPrChange', 'w:rPr/(w:eastAsianLayout,w:rPrChange)')
    ])
    def add_eastAsianLayout_fixture(self, request):
        return self.add_x_fixture(request)

    @pytest.fixture(params=[
        ('w:rPr/w:rStyle', 'w:rPr/(w:rStyle,w:specVanish)'),
        ('w:rPr/w:rFonts', 'w:rPr/(w:rFonts,w:specVanish)'),
        ('w:rPr/w:b', 'w:rPr/(w:b,w:specVanish)'),
        ('w:rPr/w:bCs', 'w:rPr/(w:bCs,w:specVanish)'),
        ('w:rPr/w:i', 'w:rPr/(w:i,w:specVanish)'),
        ('w:rPr/w:iCs', 'w:rPr/(w:iCs,w:specVanish)'),
        ('w:rPr/w:caps', 'w:rPr/(w:caps,w:specVanish)'),
        ('w:rPr/w:smallCaps', 'w:rPr/(w:smallCaps,w:specVanish)'),
        ('w:rPr/w:strike', 'w:rPr/(w:strike,w:specVanish)'),
        ('w:rPr/w:dstrike', 'w:rPr/(w:dstrike,w:specVanish)'),
        ('w:rPr/w:outline', 'w:rPr/(w:outline,w:specVanish)'),
        ('w:rPr/w:shadow', 'w:rPr/(w:shadow,w:specVanish)'),
        ('w:rPr/w:emboss', 'w:rPr/(w:emboss,w:specVanish)'),
        ('w:rPr/w:imprint', 'w:rPr/(w:imprint,w:specVanish)'),
        ('w:rPr/w:noProof', 'w:rPr/(w:noProof,w:specVanish)'),
        ('w:rPr/w:snapToGrid', 'w:rPr/(w:snapToGrid,w:specVanish)'),
        ('w:rPr/w:vanish', 'w:rPr/(w:vanish,w:specVanish)'),
        ('w:rPr/w:webHidden', 'w:rPr/(w:webHidden,w:specVanish)'),
        ('w:rPr/w:color', 'w:rPr/(w:color,w:specVanish)'),
        ('w:rPr/w:spacing', 'w:rPr/(w:spacing,w:specVanish)'),
        ('w:rPr/w:w', 'w:rPr/(w:w,w:specVanish)'),
        ('w:rPr/w:kern', 'w:rPr/(w:kern,w:specVanish)'),
        ('w:rPr/w:position', 'w:rPr/(w:position,w:specVanish)'),
        ('w:rPr/w:sz', 'w:rPr/(w:sz,w:specVanish)'),
        ('w:rPr/w:szCs', 'w:rPr/(w:szCs,w:specVanish)'),
        ('w:rPr/w:highlight', 'w:rPr/(w:highlight,w:specVanish)'),
        ('w:rPr/w:u', 'w:rPr/(w:u,w:specVanish)'),
        ('w:rPr/w:effect', 'w:rPr/(w:effect,w:specVanish)'),
        ('w:rPr/w:bdr', 'w:rPr/(w:bdr,w:specVanish)'),
        ('w:rPr/w:shd', 'w:rPr/(w:shd,w:specVanish)'),
        ('w:rPr/w:fitText', 'w:rPr/(w:fitText,w:specVanish)'),
        ('w:rPr/w:vertAlign', 'w:rPr/(w:vertAlign,w:specVanish)'),
        ('w:rPr/w:rtl', 'w:rPr/(w:rtl,w:specVanish)'),
        ('w:rPr/w:cs', 'w:rPr/(w:cs,w:specVanish)'),
        ('w:rPr/w:em', 'w:rPr/(w:em,w:specVanish)'),
        ('w:rPr/w:lang', 'w:rPr/(w:lang,w:specVanish)'),
        ('w:rPr/w:eastAsianLayout', 'w:rPr/(w:eastAsianLayout,w:specVanish)'),
        ('w:rPr/w:oMath', 'w:rPr/(w:specVanish,w:oMath)'),
        ('w:rPr/w:rPrChange', 'w:rPr/(w:specVanish,w:rPrChange)')
    ])
    def add_specVanish_fixture(self, request):
        return self.add_x_fixture(request)

    @pytest.fixture(params=[
        ('w:rPr/w:rStyle', 'w:rPr/(w:rStyle,w:oMath)'),
        ('w:rPr/w:rFonts', 'w:rPr/(w:rFonts,w:oMath)'),
        ('w:rPr/w:b', 'w:rPr/(w:b,w:oMath)'),
        ('w:rPr/w:bCs', 'w:rPr/(w:bCs,w:oMath)'),
        ('w:rPr/w:i', 'w:rPr/(w:i,w:oMath)'),
        ('w:rPr/w:iCs', 'w:rPr/(w:iCs,w:oMath)'),
        ('w:rPr/w:caps', 'w:rPr/(w:caps,w:oMath)'),
        ('w:rPr/w:smallCaps', 'w:rPr/(w:smallCaps,w:oMath)'),
        ('w:rPr/w:strike', 'w:rPr/(w:strike,w:oMath)'),
        ('w:rPr/w:dstrike', 'w:rPr/(w:dstrike,w:oMath)'),
        ('w:rPr/w:outline', 'w:rPr/(w:outline,w:oMath)'),
        ('w:rPr/w:shadow', 'w:rPr/(w:shadow,w:oMath)'),
        ('w:rPr/w:emboss', 'w:rPr/(w:emboss,w:oMath)'),
        ('w:rPr/w:imprint', 'w:rPr/(w:imprint,w:oMath)'),
        ('w:rPr/w:noProof', 'w:rPr/(w:noProof,w:oMath)'),
        ('w:rPr/w:snapToGrid', 'w:rPr/(w:snapToGrid,w:oMath)'),
        ('w:rPr/w:vanish', 'w:rPr/(w:vanish,w:oMath)'),
        ('w:rPr/w:webHidden', 'w:rPr/(w:webHidden,w:oMath)'),
        ('w:rPr/w:color', 'w:rPr/(w:color,w:oMath)'),
        ('w:rPr/w:spacing', 'w:rPr/(w:spacing,w:oMath)'),
        ('w:rPr/w:w', 'w:rPr/(w:w,w:oMath)'),
        ('w:rPr/w:kern', 'w:rPr/(w:kern,w:oMath)'),
        ('w:rPr/w:position', 'w:rPr/(w:position,w:oMath)'),
        ('w:rPr/w:sz', 'w:rPr/(w:sz,w:oMath)'),
        ('w:rPr/w:szCs', 'w:rPr/(w:szCs,w:oMath)'),
        ('w:rPr/w:highlight', 'w:rPr/(w:highlight,w:oMath)'),
        ('w:rPr/w:u', 'w:rPr/(w:u,w:oMath)'),
        ('w:rPr/w:effect', 'w:rPr/(w:effect,w:oMath)'),
        ('w:rPr/w:bdr', 'w:rPr/(w:bdr,w:oMath)'),
        ('w:rPr/w:shd', 'w:rPr/(w:shd,w:oMath)'),
        ('w:rPr/w:fitText', 'w:rPr/(w:fitText,w:oMath)'),
        ('w:rPr/w:vertAlign', 'w:rPr/(w:vertAlign,w:oMath)'),
        ('w:rPr/w:rtl', 'w:rPr/(w:rtl,w:oMath)'),
        ('w:rPr/w:cs', 'w:rPr/(w:cs,w:oMath)'),
        ('w:rPr/w:em', 'w:rPr/(w:em,w:oMath)'),
        ('w:rPr/w:lang', 'w:rPr/(w:lang,w:oMath)'),
        ('w:rPr/w:eastAsianLayout', 'w:rPr/(w:eastAsianLayout,w:oMath)'),
        ('w:rPr/w:specVanish', 'w:rPr/(w:specVanish,w:oMath)'),
        ('w:rPr/w:rPrChange', 'w:rPr/(w:oMath,w:rPrChange)')
    ])
    def add_oMath_fixture(self, request):
        return self.add_x_fixture(request)

    @pytest.fixture(params=[
        ('w:rPr/w:rStyle', 'w:rPr/(w:rStyle,w:rPrChange)'),
        ('w:rPr/w:rFonts', 'w:rPr/(w:rFonts,w:rPrChange)'),
        ('w:rPr/w:b', 'w:rPr/(w:b,w:rPrChange)'),
        ('w:rPr/w:bCs', 'w:rPr/(w:bCs,w:rPrChange)'),
        ('w:rPr/w:i', 'w:rPr/(w:i,w:rPrChange)'),
        ('w:rPr/w:iCs', 'w:rPr/(w:iCs,w:rPrChange)'),
        ('w:rPr/w:caps', 'w:rPr/(w:caps,w:rPrChange)'),
        ('w:rPr/w:smallCaps', 'w:rPr/(w:smallCaps,w:rPrChange)'),
        ('w:rPr/w:strike', 'w:rPr/(w:strike,w:rPrChange)'),
        ('w:rPr/w:dstrike', 'w:rPr/(w:dstrike,w:rPrChange)'),
        ('w:rPr/w:outline', 'w:rPr/(w:outline,w:rPrChange)'),
        ('w:rPr/w:shadow', 'w:rPr/(w:shadow,w:rPrChange)'),
        ('w:rPr/w:emboss', 'w:rPr/(w:emboss,w:rPrChange)'),
        ('w:rPr/w:imprint', 'w:rPr/(w:imprint,w:rPrChange)'),
        ('w:rPr/w:noProof', 'w:rPr/(w:noProof,w:rPrChange)'),
        ('w:rPr/w:snapToGrid', 'w:rPr/(w:snapToGrid,w:rPrChange)'),
        ('w:rPr/w:vanish', 'w:rPr/(w:vanish,w:rPrChange)'),
        ('w:rPr/w:webHidden', 'w:rPr/(w:webHidden,w:rPrChange)'),
        ('w:rPr/w:color', 'w:rPr/(w:color,w:rPrChange)'),
        ('w:rPr/w:spacing', 'w:rPr/(w:spacing,w:rPrChange)'),
        ('w:rPr/w:w', 'w:rPr/(w:w,w:rPrChange)'),
        ('w:rPr/w:kern', 'w:rPr/(w:kern,w:rPrChange)'),
        ('w:rPr/w:position', 'w:rPr/(w:position,w:rPrChange)'),
        ('w:rPr/w:sz', 'w:rPr/(w:sz,w:rPrChange)'),
        ('w:rPr/w:szCs', 'w:rPr/(w:szCs,w:rPrChange)'),
        ('w:rPr/w:highlight', 'w:rPr/(w:highlight,w:rPrChange)'),
        ('w:rPr/w:u', 'w:rPr/(w:u,w:rPrChange)'),
        ('w:rPr/w:effect', 'w:rPr/(w:effect,w:rPrChange)'),
        ('w:rPr/w:bdr', 'w:rPr/(w:bdr,w:rPrChange)'),
        ('w:rPr/w:shd', 'w:rPr/(w:shd,w:rPrChange)'),
        ('w:rPr/w:fitText', 'w:rPr/(w:fitText,w:rPrChange)'),
        ('w:rPr/w:vertAlign', 'w:rPr/(w:vertAlign,w:rPrChange)'),
        ('w:rPr/w:rtl', 'w:rPr/(w:rtl,w:rPrChange)'),
        ('w:rPr/w:cs', 'w:rPr/(w:cs,w:rPrChange)'),
        ('w:rPr/w:em', 'w:rPr/(w:em,w:rPrChange)'),
        ('w:rPr/w:lang', 'w:rPr/(w:lang,w:rPrChange)'),
        ('w:rPr/w:eastAsianLayout', 'w:rPr/(w:eastAsianLayout,w:rPrChange)'),
        ('w:rPr/w:specVanish', 'w:rPr/(w:specVanish,w:rPrChange)'),
        ('w:rPr/w:oMath', 'w:rPr/(w:oMath,w:rPrChange)')
    ])
    def add_rPrChange_fixture(self, request):
        return self.add_x_fixture(request)
