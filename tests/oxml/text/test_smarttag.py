"""Test suite for the docx.oxml.text.smarttag module."""

from typing import cast

import pytest

from docx.oxml.text.smarttag import CT_SmartTag

from ...unitutil.cxml import element


class DescribeCT_SmartTag:
    """Unit-test suite for the CT_SmartTag (<w:smartTag>) element."""

    @pytest.mark.parametrize(
        ("cxml", "expected_value"),
        [
            ("w:smartTag", ""),
            ('w:smartTag/w:r/w:t"0.5m"', "0.5m"),
            ('w:smartTag/(w:r/w:t"a",w:r/w:t"b")', "ab"),
            # -- nested smart tag contributes its text as well --
            ('w:smartTag/(w:r/w:t"outer ",w:smartTag/w:r/w:t"inner")', "outer inner"),
        ],
    )
    def it_knows_the_text_it_contains(self, cxml: str, expected_value: str):
        smart_tag = cast(CT_SmartTag, element(cxml))
        assert smart_tag.text == expected_value
