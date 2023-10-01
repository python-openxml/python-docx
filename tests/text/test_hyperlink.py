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
