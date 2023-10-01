"""pytest fixtures that are shared across test modules."""

import pytest

from docx import types as t
from docx.parts.story import StoryPart


@pytest.fixture
def fake_parent() -> t.StoryChild:
    class StoryChild:
        @property
        def part(self) -> StoryPart:
            raise NotImplementedError

    return StoryChild()
