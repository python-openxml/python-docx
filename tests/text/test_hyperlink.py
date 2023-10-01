"""Test suite for the docx.text.hyperlink module."""

from typing import cast

import pytest

from docx import types as t
from docx.opc.rel import _Relationship  # pyright: ignore[reportPrivateUsage]
from docx.oxml.text.hyperlink import CT_Hyperlink
from docx.parts.story import StoryPart
from docx.text.hyperlink import Hyperlink

from ..unitutil.cxml import element
from ..unitutil.mock import FixtureRequest, Mock, instance_mock


class DescribeHyperlink:
    """Unit-test suite for the docx.text.hyperlink.Hyperlink object."""

    def it_knows_the_hyperlink_URL(self, fake_parent: t.StoryChild):
        cxml = 'w:hyperlink{r:id=rId6}/w:r/w:t"post"'
        hlink = cast(CT_Hyperlink, element(cxml))
        hyperlink = Hyperlink(hlink, fake_parent)

        assert hyperlink.address == "https://google.com/"

    @pytest.mark.parametrize(
        ("hlink_cxml", "expected_value"),
        [
            ("w:hyperlink", False),
            ("w:hyperlink/w:r", False),
            ('w:hyperlink/w:r/(w:t"abc",w:lastRenderedPageBreak,w:t"def")', True),
            ('w:hyperlink/w:r/(w:lastRenderedPageBreak,w:t"abc",w:t"def")', True),
            ('w:hyperlink/w:r/(w:t"abc",w:t"def",w:lastRenderedPageBreak)', True),
        ],
    )
    def it_knows_whether_it_contains_a_page_break(
        self, hlink_cxml: str, expected_value: bool, fake_parent: t.StoryChild
    ):
        hlink = cast(CT_Hyperlink, element(hlink_cxml))
        hyperlink = Hyperlink(hlink, fake_parent)

        assert hyperlink.contains_page_break is expected_value

    @pytest.mark.parametrize(
        ("hlink_cxml", "count"),
        [
            ("w:hyperlink", 0),
            ("w:hyperlink/w:r", 1),
            ("w:hyperlink/(w:r,w:r)", 2),
            ("w:hyperlink/(w:r,w:lastRenderedPageBreak)", 1),
            ("w:hyperlink/(w:lastRenderedPageBreak,w:r)", 1),
            ("w:hyperlink/(w:r,w:lastRenderedPageBreak,w:r)", 2),
        ],
    )
    def it_provides_access_to_the_runs_it_contains(
        self, hlink_cxml: str, count: int, fake_parent: t.StoryChild
    ):
        hlink = cast(CT_Hyperlink, element(hlink_cxml))
        hyperlink = Hyperlink(hlink, fake_parent)

        runs = hyperlink.runs

        actual = [type(item).__name__ for item in runs]
        expected = ["Run" for _ in range(count)]
        assert actual == expected

    @pytest.mark.parametrize(
        ("hlink_cxml", "expected_text"),
        [
            ("w:hyperlink", ""),
            ("w:hyperlink/w:r", ""),
            ('w:hyperlink/w:r/w:t"foobar"', "foobar"),
            ('w:hyperlink/w:r/(w:t"foo",w:lastRenderedPageBreak,w:t"bar")', "foobar"),
            ('w:hyperlink/w:r/(w:t"abc",w:tab,w:t"def",w:noBreakHyphen)', "abc\tdef-"),
        ],
    )
    def it_knows_the_visible_text_of_the_link(
        self, hlink_cxml: str, expected_text: str, fake_parent: t.StoryChild
    ):
        hlink = cast(CT_Hyperlink, element(hlink_cxml))
        hyperlink = Hyperlink(hlink, fake_parent)

        text = hyperlink.text

        assert text == expected_text

    # -- fixtures --------------------------------------------------------------------

    @pytest.fixture
    def fake_parent(self, story_part: Mock, rel: Mock) -> t.StoryChild:
        class StoryChild:
            @property
            def part(self) -> StoryPart:
                return story_part

        return StoryChild()

    @pytest.fixture
    def rel(self, request: FixtureRequest):
        return instance_mock(request, _Relationship, target_ref="https://google.com/")

    @pytest.fixture
    def story_part(self, request: FixtureRequest, rel: Mock):
        return instance_mock(request, StoryPart, rels={"rId6": rel})
