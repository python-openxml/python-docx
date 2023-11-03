"""Unit-test suite for `docx.oxml.section` module."""

from __future__ import annotations

from typing import cast

from docx.oxml.section import CT_HdrFtr
from docx.oxml.table import CT_Tbl
from docx.oxml.text.paragraph import CT_P

from ..unitutil.cxml import element


class DescribeCT_HdrFtr:
    """Unit-test suite for selected units of `docx.oxml.section.CT_HdrFtr`."""

    def it_knows_its_inner_content_block_item_elements(self):
        hdr = cast(CT_HdrFtr, element("w:hdr/(w:tbl,w:tbl,w:p)"))
        assert [type(e) for e in hdr.inner_content_elements] == [CT_Tbl, CT_Tbl, CT_P]
