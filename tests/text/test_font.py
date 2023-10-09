# pyright: reportPrivateUsage=false

"""Test suite for the docx.text.run module."""

from __future__ import annotations

from typing import cast

import pytest
from _pytest.fixtures import FixtureRequest

from docx.dml.color import ColorFormat
from docx.enum.text import WD_COLOR, WD_UNDERLINE
from docx.oxml.text.run import CT_R
from docx.shared import Length, Pt
from docx.text.font import Font

from ..unitutil.cxml import element, xml
from ..unitutil.mock import Mock, class_mock, instance_mock


class DescribeFont:
    """Unit-test suite for `docx.text.font.Font`."""

    def it_provides_access_to_its_color_object(self, ColorFormat_: Mock, color_: Mock):
        r = cast(CT_R, element("w:r"))
        font = Font(r)

        color = font.color

        ColorFormat_.assert_called_once_with(font.element)
        assert color is color_

    @pytest.mark.parametrize(
        ("r_cxml", "expected_value"),
        [
            ("w:r", None),
            ("w:r/w:rPr", None),
            ("w:r/w:rPr/w:rFonts", None),
            ("w:r/w:rPr/w:rFonts{w:ascii=Arial}", "Arial"),
        ],
    )
    def it_knows_its_typeface_name(self, r_cxml: str, expected_value: str | None):
        r = cast(CT_R, element(r_cxml))
        font = Font(r)
        assert font.name == expected_value

    @pytest.mark.parametrize(
        ("r_cxml", "value", "expected_r_cxml"),
        [
            ("w:r", "Foo", "w:r/w:rPr/w:rFonts{w:ascii=Foo,w:hAnsi=Foo}"),
            ("w:r/w:rPr", "Foo", "w:r/w:rPr/w:rFonts{w:ascii=Foo,w:hAnsi=Foo}"),
            (
                "w:r/w:rPr/w:rFonts{w:hAnsi=Foo}",
                "Bar",
                "w:r/w:rPr/w:rFonts{w:ascii=Bar,w:hAnsi=Bar}",
            ),
            (
                "w:r/w:rPr/w:rFonts{w:ascii=Foo,w:hAnsi=Foo}",
                "Bar",
                "w:r/w:rPr/w:rFonts{w:ascii=Bar,w:hAnsi=Bar}",
            ),
        ],
    )
    def it_can_change_its_typeface_name(
        self, r_cxml: str, value: str, expected_r_cxml: str
    ):
        r = cast(CT_R, element(r_cxml))
        font = Font(r)
        expected_xml = xml(expected_r_cxml)

        font.name = value

        assert font._element.xml == expected_xml

    @pytest.mark.parametrize(
        ("r_cxml", "expected_value"),
        [
            ("w:r", None),
            ("w:r/w:rPr", None),
            ("w:r/w:rPr/w:sz{w:val=28}", Pt(14)),
        ],
    )
    def it_knows_its_size(self, r_cxml: str, expected_value: Length | None):
        r = cast(CT_R, element(r_cxml))
        font = Font(r)
        assert font.size == expected_value

    @pytest.mark.parametrize(
        ("r_cxml", "value", "expected_r_cxml"),
        [
            ("w:r", Pt(12), "w:r/w:rPr/w:sz{w:val=24}"),
            ("w:r/w:rPr", Pt(12), "w:r/w:rPr/w:sz{w:val=24}"),
            ("w:r/w:rPr/w:sz{w:val=24}", Pt(18), "w:r/w:rPr/w:sz{w:val=36}"),
            ("w:r/w:rPr/w:sz{w:val=36}", None, "w:r/w:rPr"),
        ],
    )
    def it_can_change_its_size(
        self, r_cxml: str, value: Length | None, expected_r_cxml: str
    ):
        r = cast(CT_R, element(r_cxml))
        font = Font(r)
        expected_xml = xml(expected_r_cxml)

        font.size = value

        assert font._element.xml == expected_xml

    @pytest.mark.parametrize(
        ("r_cxml", "bool_prop_name", "expected_value"),
        [
            ("w:r/w:rPr", "all_caps", None),
            ("w:r/w:rPr/w:caps", "all_caps", True),
            ("w:r/w:rPr/w:caps{w:val=on}", "all_caps", True),
            ("w:r/w:rPr/w:caps{w:val=off}", "all_caps", False),
            ("w:r/w:rPr/w:b{w:val=1}", "bold", True),
            ("w:r/w:rPr/w:i{w:val=0}", "italic", False),
            ("w:r/w:rPr/w:cs{w:val=true}", "complex_script", True),
            ("w:r/w:rPr/w:bCs{w:val=false}", "cs_bold", False),
            ("w:r/w:rPr/w:iCs{w:val=on}", "cs_italic", True),
            ("w:r/w:rPr/w:dstrike{w:val=off}", "double_strike", False),
            ("w:r/w:rPr/w:emboss{w:val=1}", "emboss", True),
            ("w:r/w:rPr/w:vanish{w:val=0}", "hidden", False),
            ("w:r/w:rPr/w:i{w:val=true}", "italic", True),
            ("w:r/w:rPr/w:imprint{w:val=false}", "imprint", False),
            ("w:r/w:rPr/w:oMath{w:val=on}", "math", True),
            ("w:r/w:rPr/w:noProof{w:val=off}", "no_proof", False),
            ("w:r/w:rPr/w:outline{w:val=1}", "outline", True),
            ("w:r/w:rPr/w:rtl{w:val=0}", "rtl", False),
            ("w:r/w:rPr/w:shadow{w:val=true}", "shadow", True),
            ("w:r/w:rPr/w:smallCaps{w:val=false}", "small_caps", False),
            ("w:r/w:rPr/w:snapToGrid{w:val=on}", "snap_to_grid", True),
            ("w:r/w:rPr/w:specVanish{w:val=off}", "spec_vanish", False),
            ("w:r/w:rPr/w:strike{w:val=1}", "strike", True),
            ("w:r/w:rPr/w:webHidden{w:val=0}", "web_hidden", False),
        ],
    )
    def it_knows_its_bool_prop_states(
        self, r_cxml: str, bool_prop_name: str, expected_value: bool | None
    ):
        r = cast(CT_R, element(r_cxml))
        font = Font(r)
        assert getattr(font, bool_prop_name) == expected_value

    @pytest.mark.parametrize(
        ("r_cxml", "prop_name", "value", "expected_cxml"),
        [
            # nothing to True, False, and None ---------------------------
            ("w:r", "all_caps", True, "w:r/w:rPr/w:caps"),
            ("w:r", "bold", False, "w:r/w:rPr/w:b{w:val=0}"),
            ("w:r", "italic", None, "w:r/w:rPr"),
            # default to True, False, and None ---------------------------
            ("w:r/w:rPr/w:cs", "complex_script", True, "w:r/w:rPr/w:cs"),
            ("w:r/w:rPr/w:bCs", "cs_bold", False, "w:r/w:rPr/w:bCs{w:val=0}"),
            ("w:r/w:rPr/w:iCs", "cs_italic", None, "w:r/w:rPr"),
            # True to True, False, and None ------------------------------
            (
                "w:r/w:rPr/w:dstrike{w:val=1}",
                "double_strike",
                True,
                "w:r/w:rPr/w:dstrike",
            ),
            (
                "w:r/w:rPr/w:emboss{w:val=on}",
                "emboss",
                False,
                "w:r/w:rPr/w:emboss{w:val=0}",
            ),
            ("w:r/w:rPr/w:vanish{w:val=1}", "hidden", None, "w:r/w:rPr"),
            # False to True, False, and None -----------------------------
            ("w:r/w:rPr/w:i{w:val=false}", "italic", True, "w:r/w:rPr/w:i"),
            (
                "w:r/w:rPr/w:imprint{w:val=0}",
                "imprint",
                False,
                "w:r/w:rPr/w:imprint{w:val=0}",
            ),
            ("w:r/w:rPr/w:oMath{w:val=off}", "math", None, "w:r/w:rPr"),
            # random mix -------------------------------------------------
            (
                "w:r/w:rPr/w:noProof{w:val=1}",
                "no_proof",
                False,
                "w:r/w:rPr/w:noProof{w:val=0}",
            ),
            ("w:r/w:rPr", "outline", True, "w:r/w:rPr/w:outline"),
            ("w:r/w:rPr/w:rtl{w:val=true}", "rtl", False, "w:r/w:rPr/w:rtl{w:val=0}"),
            ("w:r/w:rPr/w:shadow{w:val=on}", "shadow", True, "w:r/w:rPr/w:shadow"),
            (
                "w:r/w:rPr/w:smallCaps",
                "small_caps",
                False,
                "w:r/w:rPr/w:smallCaps{w:val=0}",
            ),
            ("w:r/w:rPr/w:snapToGrid", "snap_to_grid", True, "w:r/w:rPr/w:snapToGrid"),
            ("w:r/w:rPr/w:specVanish", "spec_vanish", None, "w:r/w:rPr"),
            ("w:r/w:rPr/w:strike{w:val=foo}", "strike", True, "w:r/w:rPr/w:strike"),
            (
                "w:r/w:rPr/w:webHidden",
                "web_hidden",
                False,
                "w:r/w:rPr/w:webHidden{w:val=0}",
            ),
        ],
    )
    def it_can_change_its_bool_prop_settings(
        self, r_cxml: str, prop_name: str, value: bool | None, expected_cxml: str
    ):
        r = cast(CT_R, element(r_cxml))
        font = Font(r)
        expected_xml = xml(expected_cxml)

        setattr(font, prop_name, value)

        assert font._element.xml == expected_xml

    @pytest.mark.parametrize(
        ("r_cxml", "expected_value"),
        [
            ("w:r", None),
            ("w:r/w:rPr", None),
            ("w:r/w:rPr/w:vertAlign{w:val=baseline}", False),
            ("w:r/w:rPr/w:vertAlign{w:val=subscript}", True),
            ("w:r/w:rPr/w:vertAlign{w:val=superscript}", False),
        ],
    )
    def it_knows_whether_it_is_subscript(
        self, r_cxml: str, expected_value: bool | None
    ):
        r = cast(CT_R, element(r_cxml))
        font = Font(r)
        assert font.subscript == expected_value

    @pytest.mark.parametrize(
        ("r_cxml", "value", "expected_r_cxml"),
        [
            ("w:r", True, "w:r/w:rPr/w:vertAlign{w:val=subscript}"),
            ("w:r", False, "w:r/w:rPr"),
            ("w:r", None, "w:r/w:rPr"),
            (
                "w:r/w:rPr/w:vertAlign{w:val=subscript}",
                True,
                "w:r/w:rPr/w:vertAlign{w:val=subscript}",
            ),
            ("w:r/w:rPr/w:vertAlign{w:val=subscript}", False, "w:r/w:rPr"),
            ("w:r/w:rPr/w:vertAlign{w:val=subscript}", None, "w:r/w:rPr"),
            (
                "w:r/w:rPr/w:vertAlign{w:val=superscript}",
                True,
                "w:r/w:rPr/w:vertAlign{w:val=subscript}",
            ),
            (
                "w:r/w:rPr/w:vertAlign{w:val=superscript}",
                False,
                "w:r/w:rPr/w:vertAlign{w:val=superscript}",
            ),
            ("w:r/w:rPr/w:vertAlign{w:val=superscript}", None, "w:r/w:rPr"),
            (
                "w:r/w:rPr/w:vertAlign{w:val=baseline}",
                True,
                "w:r/w:rPr/w:vertAlign{w:val=subscript}",
            ),
        ],
    )
    def it_can_change_whether_it_is_subscript(
        self, r_cxml: str, value: bool | None, expected_r_cxml: str
    ):
        r = cast(CT_R, element(r_cxml))
        font = Font(r)
        expected_xml = xml(expected_r_cxml)

        font.subscript = value

        assert font._element.xml == expected_xml

    @pytest.mark.parametrize(
        ("r_cxml", "expected_value"),
        [
            ("w:r", None),
            ("w:r/w:rPr", None),
            ("w:r/w:rPr/w:vertAlign{w:val=baseline}", False),
            ("w:r/w:rPr/w:vertAlign{w:val=subscript}", False),
            ("w:r/w:rPr/w:vertAlign{w:val=superscript}", True),
        ],
    )
    def it_knows_whether_it_is_superscript(
        self, r_cxml: str, expected_value: bool | None
    ):
        r = cast(CT_R, element(r_cxml))
        font = Font(r)
        assert font.superscript == expected_value

    @pytest.mark.parametrize(
        ("r_cxml", "value", "expected_r_cxml"),
        [
            ("w:r", True, "w:r/w:rPr/w:vertAlign{w:val=superscript}"),
            ("w:r", False, "w:r/w:rPr"),
            ("w:r", None, "w:r/w:rPr"),
            (
                "w:r/w:rPr/w:vertAlign{w:val=superscript}",
                True,
                "w:r/w:rPr/w:vertAlign{w:val=superscript}",
            ),
            ("w:r/w:rPr/w:vertAlign{w:val=superscript}", False, "w:r/w:rPr"),
            ("w:r/w:rPr/w:vertAlign{w:val=superscript}", None, "w:r/w:rPr"),
            (
                "w:r/w:rPr/w:vertAlign{w:val=subscript}",
                True,
                "w:r/w:rPr/w:vertAlign{w:val=superscript}",
            ),
            (
                "w:r/w:rPr/w:vertAlign{w:val=subscript}",
                False,
                "w:r/w:rPr/w:vertAlign{w:val=subscript}",
            ),
            ("w:r/w:rPr/w:vertAlign{w:val=subscript}", None, "w:r/w:rPr"),
            (
                "w:r/w:rPr/w:vertAlign{w:val=baseline}",
                True,
                "w:r/w:rPr/w:vertAlign{w:val=superscript}",
            ),
        ],
    )
    def it_can_change_whether_it_is_superscript(
        self, r_cxml: str, value: bool | None, expected_r_cxml: str
    ):
        r = cast(CT_R, element(r_cxml))
        font = Font(r)
        expected_xml = xml(expected_r_cxml)

        font.superscript = value

        assert font._element.xml == expected_xml

    @pytest.mark.parametrize(
        ("r_cxml", "expected_value"),
        [
            ("w:r", None),
            ("w:r/w:rPr/w:u", None),
            ("w:r/w:rPr/w:u{w:val=single}", True),
            ("w:r/w:rPr/w:u{w:val=none}", False),
            ("w:r/w:rPr/w:u{w:val=double}", WD_UNDERLINE.DOUBLE),
            ("w:r/w:rPr/w:u{w:val=wave}", WD_UNDERLINE.WAVY),
        ],
    )
    def it_knows_its_underline_type(
        self, r_cxml: str, expected_value: WD_UNDERLINE | bool | None
    ):
        r = cast(CT_R, element(r_cxml))
        font = Font(r)
        assert font.underline is expected_value

    @pytest.mark.parametrize(
        ("r_cxml", "value", "expected_r_cxml"),
        [
            ("w:r", True, "w:r/w:rPr/w:u{w:val=single}"),
            ("w:r", False, "w:r/w:rPr/w:u{w:val=none}"),
            ("w:r", None, "w:r/w:rPr"),
            ("w:r", WD_UNDERLINE.SINGLE, "w:r/w:rPr/w:u{w:val=single}"),
            ("w:r", WD_UNDERLINE.THICK, "w:r/w:rPr/w:u{w:val=thick}"),
            ("w:r/w:rPr/w:u{w:val=single}", True, "w:r/w:rPr/w:u{w:val=single}"),
            ("w:r/w:rPr/w:u{w:val=single}", False, "w:r/w:rPr/w:u{w:val=none}"),
            ("w:r/w:rPr/w:u{w:val=single}", None, "w:r/w:rPr"),
            (
                "w:r/w:rPr/w:u{w:val=single}",
                WD_UNDERLINE.SINGLE,
                "w:r/w:rPr/w:u{w:val=single}",
            ),
            (
                "w:r/w:rPr/w:u{w:val=single}",
                WD_UNDERLINE.DOTTED,
                "w:r/w:rPr/w:u{w:val=dotted}",
            ),
        ],
    )
    def it_can_change_its_underline_type(
        self, r_cxml: str, value: bool | None, expected_r_cxml: str
    ):
        r = cast(CT_R, element(r_cxml))
        font = Font(r)
        expected_xml = xml(expected_r_cxml)

        font.underline = value

        assert font._element.xml == expected_xml

    @pytest.mark.parametrize(
        ("r_cxml", "expected_value"),
        [
            ("w:r", None),
            ("w:r/w:rPr", None),
            ("w:r/w:rPr/w:highlight{w:val=default}", WD_COLOR.AUTO),
            ("w:r/w:rPr/w:highlight{w:val=blue}", WD_COLOR.BLUE),
        ],
    )
    def it_knows_its_highlight_color(
        self, r_cxml: str, expected_value: WD_COLOR | None
    ):
        r = cast(CT_R, element(r_cxml))
        font = Font(r)
        assert font.highlight_color is expected_value

    @pytest.mark.parametrize(
        ("r_cxml", "value", "expected_r_cxml"),
        [
            ("w:r", WD_COLOR.AUTO, "w:r/w:rPr/w:highlight{w:val=default}"),
            ("w:r/w:rPr", WD_COLOR.BRIGHT_GREEN, "w:r/w:rPr/w:highlight{w:val=green}"),
            (
                "w:r/w:rPr/w:highlight{w:val=green}",
                WD_COLOR.YELLOW,
                "w:r/w:rPr/w:highlight{w:val=yellow}",
            ),
            ("w:r/w:rPr/w:highlight{w:val=yellow}", None, "w:r/w:rPr"),
            ("w:r/w:rPr", None, "w:r/w:rPr"),
            ("w:r", None, "w:r/w:rPr"),
        ],
    )
    def it_can_change_its_highlight_color(
        self, r_cxml: str, value: WD_COLOR | None, expected_r_cxml: str
    ):
        r = cast(CT_R, element(r_cxml))
        font = Font(r)
        expected_xml = xml(expected_r_cxml)

        font.highlight_color = value

        assert font._element.xml == expected_xml

    # -- fixtures ----------------------------------------------------

    @pytest.fixture
    def color_(self, request: FixtureRequest):
        return instance_mock(request, ColorFormat)

    @pytest.fixture
    def ColorFormat_(self, request: FixtureRequest, color_: Mock):
        return class_mock(request, "docx.text.font.ColorFormat", return_value=color_)
