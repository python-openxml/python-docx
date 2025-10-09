# pyright: reportPrivateUsage=false

"""Unit-test suite for `docx.oxml.comments` module."""

from __future__ import annotations

from typing import cast

import pytest

from docx.oxml.comments import CT_Comments

from ..unitutil.cxml import element


class DescribeCT_Comments:
    """Unit-test suite for `docx.oxml.comments.CT_Comments`."""

    @pytest.mark.parametrize(
        ("cxml", "expected_value"),
        [
            ("w:comments", 0),
            ("w:comments/(w:comment{w:id=1})", 2),
            ("w:comments/(w:comment{w:id=4},w:comment{w:id=2147483646})", 2147483647),
            ("w:comments/(w:comment{w:id=1},w:comment{w:id=2147483647})", 0),
            ("w:comments/(w:comment{w:id=1},w:comment{w:id=2},w:comment{w:id=3})", 4),
        ],
    )
    def it_finds_the_next_available_comment_id_to_help(self, cxml: str, expected_value: int):
        comments_elm = cast(CT_Comments, element(cxml))
        assert comments_elm._next_available_comment_id() == expected_value
