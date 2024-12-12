# pyright: reportPrivateUsage=false

"""Unit-test suite for the docx.text.pagebreak module."""

from typing import cast

import pytest

from docx import types as t
from docx.oxml.text.paragraph import CT_P
from docx.text.pagebreak import RenderedPageBreak

from ..unitutil.cxml import element, xml


class DescribeRenderedPageBreak:
    """Unit-test suite for the docx.text.pagebreak.RenderedPageBreak object."""

    def it_raises_on_preceding_fragment_when_page_break_is_not_first_in_paragrah(
        self, fake_parent: t.ProvidesStoryPart
    ):
        p_cxml = 'w:p/(w:r/(w:t"abc",w:lastRenderedPageBreak,w:lastRenderedPageBreak))'
        p = cast(CT_P, element(p_cxml))
        lrpb = p.lastRenderedPageBreaks[-1]
        page_break = RenderedPageBreak(lrpb, fake_parent)

        with pytest.raises(ValueError, match="only defined on first rendered page-br"):
            page_break.preceding_paragraph_fragment

    def it_produces_None_for_preceding_fragment_when_page_break_is_leading(
        self, fake_parent: t.ProvidesStoryPart
    ):
        """A page-break with no preceding content is "leading"."""
        p_cxml = 'w:p/(w:pPr/w:ind,w:r/(w:lastRenderedPageBreak,w:t"foo",w:t"bar"))'
        p = cast(CT_P, element(p_cxml))
        lrpb = p.lastRenderedPageBreaks[0]
        page_break = RenderedPageBreak(lrpb, fake_parent)

        preceding_fragment = page_break.preceding_paragraph_fragment

        assert preceding_fragment is None

    def it_can_split_off_the_preceding_paragraph_content_when_in_a_run(
        self, fake_parent: t.ProvidesStoryPart
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
        self, fake_parent: t.ProvidesStoryPart
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

    def it_raises_on_following_fragment_when_page_break_is_not_first_in_paragrah(
        self, fake_parent: t.ProvidesStoryPart
    ):
        p_cxml = 'w:p/(w:r/(w:lastRenderedPageBreak,w:lastRenderedPageBreak,w:t"abc"))'
        p = cast(CT_P, element(p_cxml))
        lrpb = p.lastRenderedPageBreaks[-1]
        page_break = RenderedPageBreak(lrpb, fake_parent)

        with pytest.raises(ValueError, match="only defined on first rendered page-br"):
            page_break.following_paragraph_fragment

    def it_produces_None_for_following_fragment_when_page_break_is_trailing(
        self, fake_parent: t.ProvidesStoryPart
    ):
        """A page-break with no following content is "trailing"."""
        p_cxml = 'w:p/(w:pPr/w:ind,w:r/(w:t"foo",w:t"bar",w:lastRenderedPageBreak))'
        p = cast(CT_P, element(p_cxml))
        lrpb = p.lastRenderedPageBreaks[0]
        page_break = RenderedPageBreak(lrpb, fake_parent)

        following_fragment = page_break.following_paragraph_fragment

        assert following_fragment is None

    def it_can_split_off_the_following_paragraph_content_when_in_a_run(
        self, fake_parent: t.ProvidesStoryPart
    ):
        p_cxml = (
            "w:p/("
            "  w:pPr/w:ind"
            '  ,w:r/(w:t"foo",w:lastRenderedPageBreak,w:t"bar")'
            '  ,w:r/w:t"foo"'
            ")"
        )
        p = cast(CT_P, element(p_cxml))
        lrpb = p.lastRenderedPageBreaks[0]
        page_break = RenderedPageBreak(lrpb, fake_parent)

        following_fragment = page_break.following_paragraph_fragment

        expected_cxml = 'w:p/(w:pPr/w:ind,w:r/w:t"bar",w:r/w:t"foo")'
        assert following_fragment is not None
        assert following_fragment._p.xml == xml(expected_cxml)

    def and_it_can_split_off_the_following_paragraph_content_when_in_a_hyperlink(
        self, fake_parent: t.ProvidesStoryPart
    ):
        p_cxml = (
            "w:p/("
            "  w:pPr/w:ind"
            '  ,w:hyperlink/w:r/(w:t"foo",w:lastRenderedPageBreak,w:t"bar")'
            '  ,w:r/w:t"baz"'
            '  ,w:r/w:t"qux"'
            ")"
        )
        p = cast(CT_P, element(p_cxml))
        lrpb = p.lastRenderedPageBreaks[0]
        page_break = RenderedPageBreak(lrpb, fake_parent)

        following_fragment = page_break.following_paragraph_fragment

        expected_cxml = 'w:p/(w:pPr/w:ind,w:r/w:t"baz",w:r/w:t"qux")'

        assert following_fragment is not None
        assert following_fragment._p.xml == xml(expected_cxml)
