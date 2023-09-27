"""Test suite for the docx.oxml.text.run module."""

from typing import cast

import pytest

from docx.oxml.text.run import CT_R

from ...unitutil.cxml import element, xml


class DescribeCT_R:
    """Unit-test suite for the CT_R (run, <w:r>) element."""

    @pytest.mark.parametrize(
        ("initial_cxml", "text", "expected_cxml"),
        [
            ("w:r", "foobar", 'w:r/w:t"foobar"'),
            ("w:r", "foobar ", 'w:r/w:t{xml:space=preserve}"foobar "'),
            (
                "w:r/(w:rPr/w:rStyle{w:val=emphasis}, w:cr)",
                "foobar",
                'w:r/(w:rPr/w:rStyle{w:val=emphasis}, w:cr, w:t"foobar")',
            ),
        ],
    )
    def it_can_add_a_t_preserving_edge_whitespace(
        self, initial_cxml: str, text: str, expected_cxml: str
    ):
        r = cast(CT_R, element(initial_cxml))
        expected_xml = xml(expected_cxml)

        r.add_t(text)

        assert r.xml == expected_xml
