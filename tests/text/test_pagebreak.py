# pyright: reportPrivateUsage=false

"""Unit-test suite for the docx.text.pagebreak module."""

from typing import cast

from docx import types as t
from docx.oxml.text.paragraph import CT_P
from docx.text.pagebreak import RenderedPageBreak

from ..unitutil.cxml import element, xml


class DescribeRenderedPageBreak:
    """Unit-test suite for the docx.text.pagebreak.RenderedPageBreak object."""

    def it_produces_None_for_preceding_fragment_when_page_break_is_leading(
        self, fake_parent: t.StoryChild
    ):
        """A page-break with no preceding content is "leading"."""
        p_cxml = 'w:p/(w:pPr/w:ind,w:r/(w:lastRenderedPageBreak,w:t"foo",w:t"bar"))'
        p = cast(CT_P, element(p_cxml))
        lrpb = p.lastRenderedPageBreaks[0]
        page_break = RenderedPageBreak(lrpb, fake_parent)

        preceding_fragment = page_break.preceding_paragraph_fragment

        assert preceding_fragment is None

    def it_can_split_off_the_preceding_paragraph_content_when_in_a_run(
        self, fake_parent: t.StoryChild
    ):
        p_cxml = (
            "w:p/("
            "  w:pPr/w:ind"
            '  ,w:r/(w:t"foo",w:lastRenderedPageBreak,w:t"bar")'
            '  ,w:r/w:t"barfoo"'
            ")"
        )
        p = cast(CT_P, element(p_cxml))
        lrpb = p.lastRenderedPageBreaks[0]
        page_break = RenderedPageBreak(lrpb, fake_parent)

        preceding_fragment = page_break.preceding_paragraph_fragment

        expected_cxml = 'w:p/(w:pPr/w:ind,w:r/w:t"foo")'
        assert preceding_fragment is not None
        assert preceding_fragment._p.xml == xml(expected_cxml)

    def and_it_can_split_off_the_preceding_paragraph_content_when_in_a_hyperlink(
        self, fake_parent: t.StoryChild
    ):
        p_cxml = (
            "w:p/("
            "  w:pPr/w:ind"
            '  ,w:hyperlink/w:r/(w:t"foo",w:lastRenderedPageBreak,w:t"bar")'
            '  ,w:r/w:t"barfoo"'
            ")"
        )
        p = cast(CT_P, element(p_cxml))
        lrpb = p.lastRenderedPageBreaks[0]
        page_break = RenderedPageBreak(lrpb, fake_parent)

        preceding_fragment = page_break.preceding_paragraph_fragment

        expected_cxml = 'w:p/(w:pPr/w:ind,w:hyperlink/w:r/(w:t"foo",w:t"bar"))'
        assert preceding_fragment is not None
        assert preceding_fragment._p.xml == xml(expected_cxml)
