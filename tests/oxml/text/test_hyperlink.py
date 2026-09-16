"""Test suite for the docx.oxml.text.hyperlink module."""

from __future__ import annotations

from typing import cast

import pytest

from docx.oxml.text.hyperlink import CT_Hyperlink
from docx.oxml.text.run import CT_R

from ...unitutil.cxml import element, xml


class DescribeCT_Hyperlink:
    """Unit-test suite for the CT_Hyperlink (<w:hyperlink>) element."""

    def it_can_create_a_detached_hyperlink(self):
        hyperlink = CT_Hyperlink.new()

        assert isinstance(hyperlink, CT_Hyperlink)
        assert hyperlink.xml == xml("w:hyperlink")
        assert hyperlink.getparent() is None

    @pytest.mark.parametrize(
        ("cxml", "expected"), [("w:hyperlink", None), ("w:hyperlink{w:tooltip=tip}", "tip")]
    )
    def it_reads_the_tooltip_attribute(self, cxml: str, expected: str | None):
        assert cast(CT_Hyperlink, element(cxml)).tooltip == expected

    @pytest.mark.parametrize("value", [None, "", 'A "tip" & more'])
    def it_sets_or_removes_the_tooltip_attribute(self, value: str | None):
        hyperlink = cast(CT_Hyperlink, element("w:hyperlink{r:id=rId7,w:tooltip=old}"))

        hyperlink.tooltip = value

        assert (
            hyperlink.get("{http://schemas.openxmlformats.org/wordprocessingml/2006/main}tooltip")
            == value
        )
        assert hyperlink.rId == "rId7"

    @pytest.mark.parametrize(("value", "exception"), [(0, TypeError), ("bad\x00tip", ValueError)])
    def it_rejects_an_invalid_tooltip_without_changing_the_attribute(
        self, value: object, exception: type[Exception]
    ):
        hyperlink = cast(CT_Hyperlink, element("w:hyperlink{w:tooltip=old}"))

        with pytest.raises(exception):
            hyperlink.tooltip = cast(str, value)

        assert hyperlink.xml == xml("w:hyperlink{w:tooltip=old}")

    def it_has_a_relationship_that_contains_the_hyperlink_address(self):
        cxml = 'w:hyperlink{r:id=rId6}/w:r/w:t"post"'
        hyperlink = cast(CT_Hyperlink, element(cxml))

        rId = hyperlink.rId

        assert rId == "rId6"

    @pytest.mark.parametrize(
        ("cxml", "expected_value"),
        [
            # -- default (when omitted) is True, somewhat surprisingly --
            ("w:hyperlink{r:id=rId6}", True),
            ("w:hyperlink{r:id=rId6,w:history=0}", False),
            ("w:hyperlink{r:id=rId6,w:history=1}", True),
        ],
    )
    def it_knows_whether_it_has_been_clicked_on_aka_visited(self, cxml: str, expected_value: bool):
        hyperlink = cast(CT_Hyperlink, element(cxml))
        assert hyperlink.history is expected_value

    def it_has_zero_or_more_runs_containing_the_hyperlink_text(self):
        cxml = 'w:hyperlink{r:id=rId6,w:history=1}/(w:r/w:t"blog",w:r/w:t" post")'
        hyperlink = cast(CT_Hyperlink, element(cxml))

        rs = hyperlink.r_lst

        assert [type(r) for r in rs] == [CT_R, CT_R]
        assert rs[0].text == "blog"
        assert rs[1].text == " post"
