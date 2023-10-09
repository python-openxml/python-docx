"""Test suite for docx.text.parfmt module, containing the ParagraphFormat object."""

import pytest

from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.shared import Pt
from docx.text.parfmt import ParagraphFormat
from docx.text.tabstops import TabStops

from ..unitutil.cxml import element, xml
from ..unitutil.mock import class_mock, instance_mock


class DescribeParagraphFormat:
    def it_knows_its_alignment_value(self, alignment_get_fixture):
        paragraph_format, expected_value = alignment_get_fixture
        assert paragraph_format.alignment == expected_value

    def it_can_change_its_alignment_value(self, alignment_set_fixture):
        paragraph_format, value, expected_xml = alignment_set_fixture
        paragraph_format.alignment = value
        assert paragraph_format._element.xml == expected_xml

    def it_knows_its_space_before(self, space_before_get_fixture):
        paragraph_format, expected_value = space_before_get_fixture
        assert paragraph_format.space_before == expected_value

    def it_can_change_its_space_before(self, space_before_set_fixture):
        paragraph_format, value, expected_xml = space_before_set_fixture
        paragraph_format.space_before = value
        assert paragraph_format._element.xml == expected_xml

    def it_knows_its_space_after(self, space_after_get_fixture):
        paragraph_format, expected_value = space_after_get_fixture
        assert paragraph_format.space_after == expected_value

    def it_can_change_its_space_after(self, space_after_set_fixture):
        paragraph_format, value, expected_xml = space_after_set_fixture
        paragraph_format.space_after = value
        assert paragraph_format._element.xml == expected_xml

    def it_knows_its_line_spacing(self, line_spacing_get_fixture):
        paragraph_format, expected_value = line_spacing_get_fixture
        assert paragraph_format.line_spacing == expected_value

    def it_can_change_its_line_spacing(self, line_spacing_set_fixture):
        paragraph_format, value, expected_xml = line_spacing_set_fixture
        paragraph_format.line_spacing = value
        assert paragraph_format._element.xml == expected_xml

    def it_knows_its_line_spacing_rule(self, line_spacing_rule_get_fixture):
        paragraph_format, expected_value = line_spacing_rule_get_fixture
        assert paragraph_format.line_spacing_rule == expected_value

    def it_can_change_its_line_spacing_rule(self, line_spacing_rule_set_fixture):
        paragraph_format, value, expected_xml = line_spacing_rule_set_fixture
        paragraph_format.line_spacing_rule = value
        assert paragraph_format._element.xml == expected_xml

    def it_knows_its_first_line_indent(self, first_indent_get_fixture):
        paragraph_format, expected_value = first_indent_get_fixture
        assert paragraph_format.first_line_indent == expected_value

    def it_can_change_its_first_line_indent(self, first_indent_set_fixture):
        paragraph_format, value, expected_xml = first_indent_set_fixture
        paragraph_format.first_line_indent = value
        assert paragraph_format._element.xml == expected_xml

    def it_knows_its_left_indent(self, left_indent_get_fixture):
        paragraph_format, expected_value = left_indent_get_fixture
        assert paragraph_format.left_indent == expected_value

    def it_can_change_its_left_indent(self, left_indent_set_fixture):
        paragraph_format, value, expected_xml = left_indent_set_fixture
        paragraph_format.left_indent = value
        assert paragraph_format._element.xml == expected_xml

    def it_knows_its_right_indent(self, right_indent_get_fixture):
        paragraph_format, expected_value = right_indent_get_fixture
        assert paragraph_format.right_indent == expected_value

    def it_can_change_its_right_indent(self, right_indent_set_fixture):
        paragraph_format, value, expected_xml = right_indent_set_fixture
        paragraph_format.right_indent = value
        assert paragraph_format._element.xml == expected_xml

    def it_knows_its_on_off_prop_values(self, on_off_get_fixture):
        paragraph_format, prop_name, expected_value = on_off_get_fixture
        assert getattr(paragraph_format, prop_name) == expected_value

    def it_can_change_its_on_off_props(self, on_off_set_fixture):
        paragraph_format, prop_name, value, expected_xml = on_off_set_fixture
        setattr(paragraph_format, prop_name, value)
        assert paragraph_format._element.xml == expected_xml

    def it_provides_access_to_its_tab_stops(self, tab_stops_fixture):
        paragraph_format, TabStops_, pPr, tab_stops_ = tab_stops_fixture
        tab_stops = paragraph_format.tab_stops
        TabStops_.assert_called_once_with(pPr)
        assert tab_stops is tab_stops_

    # fixtures -------------------------------------------------------

    @pytest.fixture(
        params=[
            ("w:p", None),
            ("w:p/w:pPr", None),
            ("w:p/w:pPr/w:jc{w:val=center}", WD_ALIGN_PARAGRAPH.CENTER),
        ]
    )
    def alignment_get_fixture(self, request):
        p_cxml, expected_value = request.param
        paragraph_format = ParagraphFormat(element(p_cxml))
        return paragraph_format, expected_value

    @pytest.fixture(
        params=[
            ("w:p", WD_ALIGN_PARAGRAPH.LEFT, "w:p/w:pPr/w:jc{w:val=left}"),
            ("w:p/w:pPr", WD_ALIGN_PARAGRAPH.CENTER, "w:p/w:pPr/w:jc{w:val=center}"),
            (
                "w:p/w:pPr/w:jc{w:val=center}",
                WD_ALIGN_PARAGRAPH.RIGHT,
                "w:p/w:pPr/w:jc{w:val=right}",
            ),
            ("w:p/w:pPr/w:jc{w:val=right}", None, "w:p/w:pPr"),
            ("w:p", None, "w:p/w:pPr"),
        ]
    )
    def alignment_set_fixture(self, request):
        p_cxml, value, expected_cxml = request.param
        paragraph_format = ParagraphFormat(element(p_cxml))
        expected_xml = xml(expected_cxml)
        return paragraph_format, value, expected_xml

    @pytest.fixture(
        params=[
            ("w:p", None),
            ("w:p/w:pPr", None),
            ("w:p/w:pPr/w:ind", None),
            ("w:p/w:pPr/w:ind{w:firstLine=240}", Pt(12)),
            ("w:p/w:pPr/w:ind{w:hanging=240}", Pt(-12)),
        ]
    )
    def first_indent_get_fixture(self, request):
        p_cxml, expected_value = request.param
        paragraph_format = ParagraphFormat(element(p_cxml))
        return paragraph_format, expected_value

    @pytest.fixture(
        params=[
            ("w:p", Pt(36), "w:p/w:pPr/w:ind{w:firstLine=720}"),
            ("w:p", Pt(-36), "w:p/w:pPr/w:ind{w:hanging=720}"),
            ("w:p", 0, "w:p/w:pPr/w:ind{w:firstLine=0}"),
            ("w:p", None, "w:p/w:pPr"),
            ("w:p/w:pPr/w:ind{w:firstLine=240}", None, "w:p/w:pPr/w:ind"),
            (
                "w:p/w:pPr/w:ind{w:firstLine=240}",
                Pt(-18),
                "w:p/w:pPr/w:ind{w:hanging=360}",
            ),
            (
                "w:p/w:pPr/w:ind{w:hanging=240}",
                Pt(18),
                "w:p/w:pPr/w:ind{w:firstLine=360}",
            ),
        ]
    )
    def first_indent_set_fixture(self, request):
        p_cxml, value, expected_p_cxml = request.param
        paragraph_format = ParagraphFormat(element(p_cxml))
        expected_xml = xml(expected_p_cxml)
        return paragraph_format, value, expected_xml

    @pytest.fixture(
        params=[
            ("w:p", None),
            ("w:p/w:pPr", None),
            ("w:p/w:pPr/w:ind", None),
            ("w:p/w:pPr/w:ind{w:left=120}", Pt(6)),
            ("w:p/w:pPr/w:ind{w:left=-06.3pt}", Pt(-6.3)),
        ]
    )
    def left_indent_get_fixture(self, request):
        p_cxml, expected_value = request.param
        paragraph_format = ParagraphFormat(element(p_cxml))
        return paragraph_format, expected_value

    @pytest.fixture(
        params=[
            ("w:p", Pt(36), "w:p/w:pPr/w:ind{w:left=720}"),
            ("w:p", Pt(-3), "w:p/w:pPr/w:ind{w:left=-60}"),
            ("w:p", 0, "w:p/w:pPr/w:ind{w:left=0}"),
            ("w:p", None, "w:p/w:pPr"),
            ("w:p/w:pPr/w:ind{w:left=240}", None, "w:p/w:pPr/w:ind"),
        ]
    )
    def left_indent_set_fixture(self, request):
        p_cxml, value, expected_p_cxml = request.param
        paragraph_format = ParagraphFormat(element(p_cxml))
        expected_xml = xml(expected_p_cxml)
        return paragraph_format, value, expected_xml

    @pytest.fixture(
        params=[
            ("w:p", None),
            ("w:p/w:pPr", None),
            ("w:p/w:pPr/w:spacing", None),
            ("w:p/w:pPr/w:spacing{w:line=420}", 1.75),
            ("w:p/w:pPr/w:spacing{w:line=840,w:lineRule=exact}", Pt(42)),
            ("w:p/w:pPr/w:spacing{w:line=840,w:lineRule=atLeast}", Pt(42)),
        ]
    )
    def line_spacing_get_fixture(self, request):
        p_cxml, expected_value = request.param
        paragraph_format = ParagraphFormat(element(p_cxml))
        return paragraph_format, expected_value

    @pytest.fixture(
        params=[
            ("w:p", 1, "w:p/w:pPr/w:spacing{w:line=240,w:lineRule=auto}"),
            ("w:p", 2.0, "w:p/w:pPr/w:spacing{w:line=480,w:lineRule=auto}"),
            ("w:p", Pt(42), "w:p/w:pPr/w:spacing{w:line=840,w:lineRule=exact}"),
            ("w:p/w:pPr", 2, "w:p/w:pPr/w:spacing{w:line=480,w:lineRule=auto}"),
            (
                "w:p/w:pPr/w:spacing{w:line=360}",
                1,
                "w:p/w:pPr/w:spacing{w:line=240,w:lineRule=auto}",
            ),
            (
                "w:p/w:pPr/w:spacing{w:line=240,w:lineRule=exact}",
                1.75,
                "w:p/w:pPr/w:spacing{w:line=420,w:lineRule=auto}",
            ),
            (
                "w:p/w:pPr/w:spacing{w:line=240,w:lineRule=atLeast}",
                Pt(42),
                "w:p/w:pPr/w:spacing{w:line=840,w:lineRule=atLeast}",
            ),
            (
                "w:p/w:pPr/w:spacing{w:line=240,w:lineRule=exact}",
                None,
                "w:p/w:pPr/w:spacing",
            ),
            ("w:p/w:pPr", None, "w:p/w:pPr"),
        ]
    )
    def line_spacing_set_fixture(self, request):
        p_cxml, value, expected_p_cxml = request.param
        paragraph_format = ParagraphFormat(element(p_cxml))
        expected_xml = xml(expected_p_cxml)
        return paragraph_format, value, expected_xml

    @pytest.fixture(
        params=[
            ("w:p", None),
            ("w:p/w:pPr", None),
            ("w:p/w:pPr/w:spacing", None),
            ("w:p/w:pPr/w:spacing{w:line=240}", WD_LINE_SPACING.SINGLE),
            ("w:p/w:pPr/w:spacing{w:line=360}", WD_LINE_SPACING.ONE_POINT_FIVE),
            ("w:p/w:pPr/w:spacing{w:line=480}", WD_LINE_SPACING.DOUBLE),
            ("w:p/w:pPr/w:spacing{w:line=420}", WD_LINE_SPACING.MULTIPLE),
            ("w:p/w:pPr/w:spacing{w:lineRule=auto}", WD_LINE_SPACING.MULTIPLE),
            ("w:p/w:pPr/w:spacing{w:lineRule=exact}", WD_LINE_SPACING.EXACTLY),
            ("w:p/w:pPr/w:spacing{w:lineRule=atLeast}", WD_LINE_SPACING.AT_LEAST),
        ]
    )
    def line_spacing_rule_get_fixture(self, request):
        p_cxml, expected_value = request.param
        paragraph_format = ParagraphFormat(element(p_cxml))
        return paragraph_format, expected_value

    @pytest.fixture(
        params=[
            (
                "w:p",
                WD_LINE_SPACING.SINGLE,
                "w:p/w:pPr/w:spacing{w:line=240,w:lineRule=auto}",
            ),
            (
                "w:p",
                WD_LINE_SPACING.ONE_POINT_FIVE,
                "w:p/w:pPr/w:spacing{w:line=360,w:lineRule=auto}",
            ),
            (
                "w:p",
                WD_LINE_SPACING.DOUBLE,
                "w:p/w:pPr/w:spacing{w:line=480,w:lineRule=auto}",
            ),
            ("w:p", WD_LINE_SPACING.MULTIPLE, "w:p/w:pPr/w:spacing{w:lineRule=auto}"),
            ("w:p", WD_LINE_SPACING.EXACTLY, "w:p/w:pPr/w:spacing{w:lineRule=exact}"),
            (
                "w:p/w:pPr/w:spacing{w:line=280,w:lineRule=exact}",
                WD_LINE_SPACING.AT_LEAST,
                "w:p/w:pPr/w:spacing{w:line=280,w:lineRule=atLeast}",
            ),
        ]
    )
    def line_spacing_rule_set_fixture(self, request):
        p_cxml, value, expected_p_cxml = request.param
        paragraph_format = ParagraphFormat(element(p_cxml))
        expected_xml = xml(expected_p_cxml)
        return paragraph_format, value, expected_xml

    @pytest.fixture(
        params=[
            ("w:p", "keep_together", None),
            ("w:p/w:pPr/w:keepLines{w:val=on}", "keep_together", True),
            ("w:p/w:pPr/w:keepLines{w:val=0}", "keep_together", False),
            ("w:p", "keep_with_next", None),
            ("w:p/w:pPr/w:keepNext{w:val=1}", "keep_with_next", True),
            ("w:p/w:pPr/w:keepNext{w:val=false}", "keep_with_next", False),
            ("w:p", "page_break_before", None),
            ("w:p/w:pPr/w:pageBreakBefore", "page_break_before", True),
            ("w:p/w:pPr/w:pageBreakBefore{w:val=0}", "page_break_before", False),
            ("w:p", "widow_control", None),
            ("w:p/w:pPr/w:widowControl{w:val=true}", "widow_control", True),
            ("w:p/w:pPr/w:widowControl{w:val=off}", "widow_control", False),
        ]
    )
    def on_off_get_fixture(self, request):
        p_cxml, prop_name, expected_value = request.param
        paragraph_format = ParagraphFormat(element(p_cxml))
        return paragraph_format, prop_name, expected_value

    @pytest.fixture(
        params=[
            ("w:p", "keep_together", True, "w:p/w:pPr/w:keepLines"),
            ("w:p", "keep_with_next", True, "w:p/w:pPr/w:keepNext"),
            ("w:p", "page_break_before", True, "w:p/w:pPr/w:pageBreakBefore"),
            ("w:p", "widow_control", True, "w:p/w:pPr/w:widowControl"),
            (
                "w:p/w:pPr/w:keepLines",
                "keep_together",
                False,
                "w:p/w:pPr/w:keepLines{w:val=0}",
            ),
            (
                "w:p/w:pPr/w:keepNext",
                "keep_with_next",
                False,
                "w:p/w:pPr/w:keepNext{w:val=0}",
            ),
            (
                "w:p/w:pPr/w:pageBreakBefore",
                "page_break_before",
                False,
                "w:p/w:pPr/w:pageBreakBefore{w:val=0}",
            ),
            (
                "w:p/w:pPr/w:widowControl",
                "widow_control",
                False,
                "w:p/w:pPr/w:widowControl{w:val=0}",
            ),
            ("w:p/w:pPr/w:keepLines{w:val=0}", "keep_together", None, "w:p/w:pPr"),
            ("w:p/w:pPr/w:keepNext{w:val=0}", "keep_with_next", None, "w:p/w:pPr"),
            (
                "w:p/w:pPr/w:pageBreakBefore{w:val=0}",
                "page_break_before",
                None,
                "w:p/w:pPr",
            ),
            ("w:p/w:pPr/w:widowControl{w:val=0}", "widow_control", None, "w:p/w:pPr"),
        ]
    )
    def on_off_set_fixture(self, request):
        p_cxml, prop_name, value, expected_cxml = request.param
        paragraph_format = ParagraphFormat(element(p_cxml))
        expected_xml = xml(expected_cxml)
        return paragraph_format, prop_name, value, expected_xml

    @pytest.fixture(
        params=[
            ("w:p", None),
            ("w:p/w:pPr", None),
            ("w:p/w:pPr/w:ind", None),
            ("w:p/w:pPr/w:ind{w:right=160}", Pt(8)),
            ("w:p/w:pPr/w:ind{w:right=-4.2pt}", Pt(-4.2)),
        ]
    )
    def right_indent_get_fixture(self, request):
        p_cxml, expected_value = request.param
        paragraph_format = ParagraphFormat(element(p_cxml))
        return paragraph_format, expected_value

    @pytest.fixture(
        params=[
            ("w:p", Pt(36), "w:p/w:pPr/w:ind{w:right=720}"),
            ("w:p", Pt(-3), "w:p/w:pPr/w:ind{w:right=-60}"),
            ("w:p", 0, "w:p/w:pPr/w:ind{w:right=0}"),
            ("w:p", None, "w:p/w:pPr"),
            ("w:p/w:pPr/w:ind{w:right=240}", None, "w:p/w:pPr/w:ind"),
        ]
    )
    def right_indent_set_fixture(self, request):
        p_cxml, value, expected_p_cxml = request.param
        paragraph_format = ParagraphFormat(element(p_cxml))
        expected_xml = xml(expected_p_cxml)
        return paragraph_format, value, expected_xml

    @pytest.fixture(
        params=[
            ("w:p", None),
            ("w:p/w:pPr", None),
            ("w:p/w:pPr/w:spacing", None),
            ("w:p/w:pPr/w:spacing{w:after=240}", Pt(12)),
        ]
    )
    def space_after_get_fixture(self, request):
        p_cxml, expected_value = request.param
        paragraph_format = ParagraphFormat(element(p_cxml))
        return paragraph_format, expected_value

    @pytest.fixture(
        params=[
            ("w:p", Pt(12), "w:p/w:pPr/w:spacing{w:after=240}"),
            ("w:p", None, "w:p/w:pPr"),
            ("w:p/w:pPr", Pt(12), "w:p/w:pPr/w:spacing{w:after=240}"),
            ("w:p/w:pPr", None, "w:p/w:pPr"),
            ("w:p/w:pPr/w:spacing", Pt(12), "w:p/w:pPr/w:spacing{w:after=240}"),
            ("w:p/w:pPr/w:spacing", None, "w:p/w:pPr/w:spacing"),
            (
                "w:p/w:pPr/w:spacing{w:after=240}",
                Pt(42),
                "w:p/w:pPr/w:spacing{w:after=840}",
            ),
            ("w:p/w:pPr/w:spacing{w:after=840}", None, "w:p/w:pPr/w:spacing"),
        ]
    )
    def space_after_set_fixture(self, request):
        p_cxml, value, expected_p_cxml = request.param
        paragraph_format = ParagraphFormat(element(p_cxml))
        expected_xml = xml(expected_p_cxml)
        return paragraph_format, value, expected_xml

    @pytest.fixture(
        params=[
            ("w:p", None),
            ("w:p/w:pPr", None),
            ("w:p/w:pPr/w:spacing", None),
            ("w:p/w:pPr/w:spacing{w:before=420}", Pt(21)),
        ]
    )
    def space_before_get_fixture(self, request):
        p_cxml, expected_value = request.param
        paragraph_format = ParagraphFormat(element(p_cxml))
        return paragraph_format, expected_value

    @pytest.fixture(
        params=[
            ("w:p", Pt(12), "w:p/w:pPr/w:spacing{w:before=240}"),
            ("w:p", None, "w:p/w:pPr"),
            ("w:p/w:pPr", Pt(12), "w:p/w:pPr/w:spacing{w:before=240}"),
            ("w:p/w:pPr", None, "w:p/w:pPr"),
            ("w:p/w:pPr/w:spacing", Pt(12), "w:p/w:pPr/w:spacing{w:before=240}"),
            ("w:p/w:pPr/w:spacing", None, "w:p/w:pPr/w:spacing"),
            (
                "w:p/w:pPr/w:spacing{w:before=240}",
                Pt(42),
                "w:p/w:pPr/w:spacing{w:before=840}",
            ),
            ("w:p/w:pPr/w:spacing{w:before=840}", None, "w:p/w:pPr/w:spacing"),
        ]
    )
    def space_before_set_fixture(self, request):
        p_cxml, value, expected_p_cxml = request.param
        paragraph_format = ParagraphFormat(element(p_cxml))
        expected_xml = xml(expected_p_cxml)
        return paragraph_format, value, expected_xml

    @pytest.fixture
    def tab_stops_fixture(self, TabStops_, tab_stops_):
        p = element("w:p/w:pPr")
        pPr = p.pPr
        paragraph_format = ParagraphFormat(p, None)
        return paragraph_format, TabStops_, pPr, tab_stops_

    # fixture components ---------------------------------------------

    @pytest.fixture
    def TabStops_(self, request, tab_stops_):
        return class_mock(request, "docx.text.parfmt.TabStops", return_value=tab_stops_)

    @pytest.fixture
    def tab_stops_(self, request):
        return instance_mock(request, TabStops)
