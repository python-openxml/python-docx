"""Test suite for the docx.oxml.text.hyperlink module."""

from typing import cast

import pytest

from docx.oxml.text.hyperlink import CT_Hyperlink
from docx.oxml.text.run import CT_R

from ...unitutil.cxml import element


class DescribeCT_Hyperlink:
    """Unit-test suite for the CT_Hyperlink (<w:hyperlink>) element."""

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
    def it_knows_whether_it_has_been_clicked_on_aka_visited(
        self, cxml: str, expected_value: bool
    ):
        hyperlink = cast(CT_Hyperlink, element(cxml))
        assert hyperlink.history is expected_value

    def it_has_zero_or_more_runs_containing_the_hyperlink_text(self):
        cxml = 'w:hyperlink{r:id=rId6,w:history=1}/(w:r/w:t"blog",w:r/w:t" post")'
        hyperlink = cast(CT_Hyperlink, element(cxml))

        rs = hyperlink.r_lst

        assert [type(r) for r in rs] == [CT_R, CT_R]
        assert rs[0].text == "blog"
        assert rs[1].text == " post"
