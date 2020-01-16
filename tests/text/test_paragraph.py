# encoding: utf-8

"""Unit test suite for the docx.text.paragraph module"""

from __future__ import absolute_import, division, print_function, unicode_literals

import pytest

from docx.enum.style import WD_STYLE_TYPE
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.text.paragraph import CT_P
from docx.oxml.text.run import CT_R
from docx.parts.document import DocumentPart
from docx.parts.hdrftr import FooterPart, HeaderPart
from docx.text.paragraph import Paragraph
from docx.text.parfmt import ParagraphFormat
from docx.text.run import Run
from docx.bookmark import _Bookmark, Bookmarks

from ..unitutil.cxml import element, xml
from ..unitutil.mock import (
    ANY,
    call,
    class_mock,
    instance_mock,
    method_mock,
    property_mock,
)


class DescribeParagraph(object):
    def it_can_end_a_bookmark(self, end_bookmark_fixture):
        blockContainer, name, bookmarkStart, expected_xml = end_bookmark_fixture

        blkcntnr = Paragraph(blockContainer, None)
        bookmark_ = _Bookmark((bookmarkStart, None))

        bookmark = blkcntnr.end_bookmark(bookmark_)

        assert blkcntnr._element.xml == expected_xml
        assert bookmark.name == name
        assert bookmark is bookmark_

    def it_can_start_a_bookmark(
        self,
        start_bookmark_fixture,
        _bookmarks_prop_,
        bookmarks_,
        _Bookmark_,
        bookmark_,
    ):
        paragraph_, name, next_id, expected_xml = start_bookmark_fixture

        bookmarks_.__contains__.return_value = False
        bookmarks_.next_id = next_id
        _bookmarks_prop_.return_value = bookmarks_
        _Bookmark_.return_value = bookmark_
        paragraph = Paragraph(paragraph_, None)

        bookmark = paragraph.start_bookmark(name)

        _Bookmark_.assert_called_once_with((ANY, None))
        assert paragraph._element.xml == expected_xml
        assert bookmark is bookmark_

    def it_knows_its_paragraph_style(self, style_get_fixture):
        paragraph, style_id_, style_ = style_get_fixture
        style = paragraph.style
        paragraph.part.get_style.assert_called_once_with(
            style_id_, WD_STYLE_TYPE.PARAGRAPH
        )
        assert style is style_

    def it_can_change_its_paragraph_style(self, style_set_fixture):
        paragraph, value, expected_xml = style_set_fixture

        paragraph.style = value

        paragraph.part.get_style_id.assert_called_once_with(
            value, WD_STYLE_TYPE.PARAGRAPH
        )
        assert paragraph._p.xml == expected_xml

    def it_knows_the_text_it_contains(self, text_get_fixture):
        paragraph, expected_text = text_get_fixture
        assert paragraph.text == expected_text

    def it_can_replace_the_text_it_contains(self, text_set_fixture):
        paragraph, text, expected_text = text_set_fixture
        paragraph.text = text
        assert paragraph.text == expected_text

    def it_knows_its_alignment_value(self, alignment_get_fixture):
        paragraph, expected_value = alignment_get_fixture
        assert paragraph.alignment == expected_value

    def it_can_change_its_alignment_value(self, alignment_set_fixture):
        paragraph, value, expected_xml = alignment_set_fixture
        paragraph.alignment = value
        assert paragraph._p.xml == expected_xml

    def it_provides_access_to_its_paragraph_format(self, parfmt_fixture):
        paragraph, ParagraphFormat_, paragraph_format_ = parfmt_fixture
        paragraph_format = paragraph.paragraph_format
        ParagraphFormat_.assert_called_once_with(paragraph._element)
        assert paragraph_format is paragraph_format_

    def it_provides_access_to_the_global_bookmarks_collection_to_help(
        self, bookmarks_fixture, part_prop_, bookmarks_
    ):
        parent_part_ = bookmarks_fixture
        parent_part_.bookmarks = bookmarks_
        part_prop_.return_value = parent_part_
        blkcntnr = Paragraph(None, None)

        bookmarks = blkcntnr._bookmarks

        assert bookmarks is bookmarks_

    def it_provides_access_to_the_runs_it_contains(self, runs_fixture):
        paragraph, Run_, r_, r_2_, run_, run_2_ = runs_fixture
        runs = paragraph.runs
        assert Run_.mock_calls == [call(r_, paragraph), call(r_2_, paragraph)]
        assert runs == [run_, run_2_]

    def it_can_add_a_run_to_itself(self, add_run_fixture):
        paragraph, text, style, style_prop_, expected_xml = add_run_fixture
        run = paragraph.add_run(text, style)
        assert paragraph._p.xml == expected_xml
        assert isinstance(run, Run)
        assert run._r is paragraph._p.r_lst[0]
        if style:
            style_prop_.assert_called_once_with(style)

    def it_can_insert_a_paragraph_before_itself(self, insert_before_fixture):
        text, style, paragraph_, add_run_calls = insert_before_fixture
        paragraph = Paragraph(None, None)

        new_paragraph = paragraph.insert_paragraph_before(text, style)

        paragraph._insert_paragraph_before.assert_called_once_with(paragraph)
        assert new_paragraph.add_run.call_args_list == add_run_calls
        assert new_paragraph.style == style
        assert new_paragraph is paragraph_

    def it_can_remove_its_content_while_preserving_formatting(self, clear_fixture):
        paragraph, expected_xml = clear_fixture
        _paragraph = paragraph.clear()
        assert paragraph._p.xml == expected_xml
        assert _paragraph is paragraph

    def it_inserts_a_paragraph_before_to_help(self, _insert_before_fixture):
        paragraph, body, expected_xml = _insert_before_fixture
        new_paragraph = paragraph._insert_paragraph_before()
        assert isinstance(new_paragraph, Paragraph)
        assert body.xml == expected_xml

    # fixtures -------------------------------------------------------

    @pytest.fixture(
        params=[
            ("w:p", None, None, "w:p/w:r"),
            ("w:p", "foobar", None, 'w:p/w:r/w:t"foobar"'),
            ("w:p", None, "Strong", "w:p/w:r"),
            ("w:p", "foobar", "Strong", 'w:p/w:r/w:t"foobar"'),
        ]
    )
    def add_run_fixture(self, request, run_style_prop_):
        before_cxml, text, style, after_cxml = request.param
        paragraph = Paragraph(element(before_cxml), None)
        expected_xml = xml(after_cxml)
        return paragraph, text, style, run_style_prop_, expected_xml

    @pytest.fixture(
        params=[
            ("w:p/w:pPr/w:jc{w:val=center}", WD_ALIGN_PARAGRAPH.CENTER),
            ("w:p", None),
        ]
    )
    def alignment_get_fixture(self, request):
        cxml, expected_alignment_value = request.param
        paragraph = Paragraph(element(cxml), None)
        return paragraph, expected_alignment_value

    @pytest.fixture(
        params=[
            ("w:p", WD_ALIGN_PARAGRAPH.LEFT, "w:p/w:pPr/w:jc{w:val=left}"),
            (
                "w:p/w:pPr/w:jc{w:val=left}",
                WD_ALIGN_PARAGRAPH.CENTER,
                "w:p/w:pPr/w:jc{w:val=center}",
            ),
            ("w:p/w:pPr/w:jc{w:val=left}", None, "w:p/w:pPr"),
            ("w:p", None, "w:p/w:pPr"),
        ]
    )
    def alignment_set_fixture(self, request):
        initial_cxml, new_alignment_value, expected_cxml = request.param
        paragraph = Paragraph(element(initial_cxml), None)
        expected_xml = xml(expected_cxml)
        return paragraph, new_alignment_value, expected_xml

    @pytest.fixture(params=[DocumentPart, HeaderPart, FooterPart])
    def bookmarks_fixture(self, request):
        PartCls = request.param
        parent_part_ = instance_mock(request, PartCls)
        return parent_part_

    @pytest.fixture(
        params=[
            ("w:p", "w:p"),
            ("w:p/w:pPr", "w:p/w:pPr"),
            ('w:p/w:r/w:t"foobar"', "w:p"),
            ('w:p/(w:pPr, w:r/w:t"foobar")', "w:p/w:pPr"),
        ]
    )
    def clear_fixture(self, request):
        initial_cxml, expected_cxml = request.param
        paragraph = Paragraph(element(initial_cxml), None)
        expected_xml = xml(expected_cxml)
        return paragraph, expected_xml

    @pytest.fixture(
        params=[
            # ---at start of paragraph---
            (
                "w:p/(w:bookmarkStart{w:name=bmk-1, w:id=24})",
                "w:bookmarkStart{w:name=bmk-1, w:id=24}",
                "w:p/(w:bookmarkStart{w:name=bmk-1, w:id=24},w:bookmarkEnd{w:id=24})",
            ),
            (
                # ---run in between bookmarks---
                'w:p/(w:bookmarkStart{w:name=bmk-1, w:id=24}, w:r/w:t"foobar")',
                "w:bookmarkStart{w:name=bmk-1, w:id=24}",
                'w:p/(w:bookmarkStart{w:name=bmk-1, w:id=24},w:r/w:t"foobar", w:bookmarkEnd{w:id=24})',
            ),
        ]
    )
    def end_bookmark_fixture(self, request):
        cxml, bookmark_cxml, expected_cxml = request.param
        blockContainer = element(cxml)
        bookmarkStart = element(bookmark_cxml)
        expected_xml = xml(expected_cxml)
        name = "bmk-1"
        return blockContainer, name, bookmarkStart, expected_xml

    @pytest.fixture(params=[(None, None), ("Foo", None), (None, "Bar"), ("Foo", "Bar")])
    def insert_before_fixture(self, request, _insert_paragraph_before_, add_run_):
        text, style = request.param
        paragraph_ = _insert_paragraph_before_.return_value
        add_run_calls = [] if text is None else [call(text)]
        paragraph_.style = None
        return text, style, paragraph_, add_run_calls

    @pytest.fixture(params=[("w:body/w:p{id=42}", "w:body/(w:p,w:p{id=42})")])
    def _insert_before_fixture(self, request):
        body_cxml, expected_cxml = request.param
        body = element(body_cxml)
        paragraph = Paragraph(body[0], None)
        expected_xml = xml(expected_cxml)
        return paragraph, body, expected_xml

    @pytest.fixture
    def parfmt_fixture(self, ParagraphFormat_, paragraph_format_):
        paragraph = Paragraph(element("w:p"), None)
        return paragraph, ParagraphFormat_, paragraph_format_

    @pytest.fixture
    def runs_fixture(self, p_, Run_, r_, r_2_, runs_):
        paragraph = Paragraph(p_, None)
        run_, run_2_ = runs_
        return paragraph, Run_, r_, r_2_, run_, run_2_

    @pytest.fixture(
        params=[
            # ---bookmarkStart as first element---
            ("w:p", 0, "w:p/w:bookmarkStart{w:name=bmk-1, w:id=0}"),
            # ---bookmarkStart after a run---
            ("w:p/(w:r)", 1, "w:p/(w:r,w:bookmarkStart{w:name=bmk-1, w:id=1})"),
        ]
    )
    def start_bookmark_fixture(self, request):
        cxml, next_id, expected_cxml = request.param
        paragraph = element(cxml)
        expected_xml = xml(expected_cxml)
        name = "bmk-1"
        return paragraph, name, next_id, expected_xml

    @pytest.fixture
    def style_get_fixture(self, part_prop_):
        style_id = "Foobar"
        p_cxml = "w:p/w:pPr/w:pStyle{w:val=%s}" % style_id
        paragraph = Paragraph(element(p_cxml), None)
        style_ = part_prop_.return_value.get_style.return_value
        return paragraph, style_id, style_

    @pytest.fixture(
        params=[
            ("w:p", "Heading 1", "Heading1", "w:p/w:pPr/w:pStyle{w:val=Heading1}"),
            (
                "w:p/w:pPr",
                "Heading 1",
                "Heading1",
                "w:p/w:pPr/w:pStyle{w:val=Heading1}",
            ),
            (
                "w:p/w:pPr/w:pStyle{w:val=Heading1}",
                "Heading 2",
                "Heading2",
                "w:p/w:pPr/w:pStyle{w:val=Heading2}",
            ),
            ("w:p/w:pPr/w:pStyle{w:val=Heading1}", "Normal", None, "w:p/w:pPr"),
            ("w:p", None, None, "w:p/w:pPr"),
        ]
    )
    def style_set_fixture(self, request, part_prop_):
        p_cxml, value, style_id, expected_cxml = request.param
        paragraph = Paragraph(element(p_cxml), None)
        part_prop_.return_value.get_style_id.return_value = style_id
        expected_xml = xml(expected_cxml)
        return paragraph, value, expected_xml

    @pytest.fixture(
        params=[
            ("w:p", ""),
            ("w:p/w:r", ""),
            ("w:p/w:r/w:t", ""),
            ('w:p/w:r/w:t"foo"', "foo"),
            ('w:p/w:r/(w:t"foo", w:t"bar")', "foobar"),
            ('w:p/w:r/(w:t"fo ", w:t"bar")', "fo bar"),
            ('w:p/w:r/(w:t"foo", w:tab, w:t"bar")', "foo\tbar"),
            ('w:p/w:r/(w:t"foo", w:br,  w:t"bar")', "foo\nbar"),
            ('w:p/w:r/(w:t"foo", w:cr,  w:t"bar")', "foo\nbar"),
        ]
    )
    def text_get_fixture(self, request):
        p_cxml, expected_text_value = request.param
        paragraph = Paragraph(element(p_cxml), None)
        return paragraph, expected_text_value

    @pytest.fixture
    def text_set_fixture(self):
        paragraph = Paragraph(element("w:p"), None)
        paragraph.add_run("must not appear in result")
        new_text_value = "foo\tbar\rbaz\n"
        expected_text_value = "foo\tbar\nbaz\n"
        return paragraph, new_text_value, expected_text_value

    # fixture components ---------------------------------------------

    @pytest.fixture
    def add_run_(self, request):
        return method_mock(request, Paragraph, "add_run")

    @pytest.fixture
    def _Bookmark_(self, request):
        return class_mock(request, "docx.text.paragraph._Bookmark")

    @pytest.fixture
    def bookmark_(self, request):
        return instance_mock(request, _Bookmark)

    @pytest.fixture
    def bookmarks_(self, request):
        return instance_mock(request, Bookmarks)

    @pytest.fixture
    def _bookmarks_prop_(self, request):
        return property_mock(request, Paragraph, "_bookmarks")

    @pytest.fixture
    def document_part_(self, request):
        return instance_mock(request, DocumentPart)

    @pytest.fixture
    def _insert_paragraph_before_(self, request):
        return method_mock(request, Paragraph, "_insert_paragraph_before")

    @pytest.fixture
    def p_(self, request, r_, r_2_):
        return instance_mock(request, CT_P, r_lst=(r_, r_2_))

    @pytest.fixture
    def ParagraphFormat_(self, request, paragraph_format_):
        return class_mock(
            request,
            "docx.text.paragraph.ParagraphFormat",
            return_value=paragraph_format_,
        )

    @pytest.fixture
    def paragraph_format_(self, request):
        return instance_mock(request, ParagraphFormat)

    @pytest.fixture
    def part_prop_(self, request, document_part_):
        return property_mock(request, Paragraph, "part", return_value=document_part_)

    @pytest.fixture
    def Run_(self, request, runs_):
        run_, run_2_ = runs_
        return class_mock(
            request, "docx.text.paragraph.Run", side_effect=[run_, run_2_]
        )

    @pytest.fixture
    def r_(self, request):
        return instance_mock(request, CT_R)

    @pytest.fixture
    def r_2_(self, request):
        return instance_mock(request, CT_R)

    @pytest.fixture
    def run_style_prop_(self, request):
        return property_mock(request, Run, "style")

    @pytest.fixture
    def runs_(self, request):
        run_ = instance_mock(request, Run, name="run_")
        run_2_ = instance_mock(request, Run, name="run_2_")
        return run_, run_2_
