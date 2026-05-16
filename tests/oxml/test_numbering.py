"""Test suite for the docx.oxml.numbering module."""

from typing import cast

import pytest

from docx.oxml.numbering import CT_Numbering

from ..unitutil.cxml import element


class DescribeCT_Numbering:
    @pytest.mark.parametrize(
        ("num_ids", "expected_value"),
        [
            ([], 1),
            ([1, 2, 3], 4),
            ([1, 3, 4], 2),
        ],
    )
    def it_knows_the_next_unused_numId(self, num_ids: list[int], expected_value: int):
        children = ",".join(f"w:num{{w:numId={num_id}}}" for num_id in num_ids)
        cxml = "w:numbering" if not children else f"w:numbering/({children})"
        numbering = cast(CT_Numbering, element(cxml))

        assert numbering._next_numId == expected_value
