# encoding: utf-8

"""
Test suite for the docx.oxml.parts module.
"""

from __future__ import absolute_import, print_function, unicode_literals

import pytest

from ...unitutil.cxml import element, xml


class DescribeCT_Body(object):
    def it_can_clear_all_its_content(self, clear_fixture):
        body, expected_xml = clear_fixture
        body.clear_content()
        assert body.xml == expected_xml

    def it_can_add_a_section_break(self, section_break_fixture):
        body, expected_xml = section_break_fixture
        sectPr = body.add_section_break()
        assert body.xml == expected_xml
        assert sectPr is body.get_or_add_sectPr()

    # fixtures -------------------------------------------------------

    @pytest.fixture(
        params=[
            ("w:body", "w:body"),
            ("w:body/w:p", "w:body"),
            ("w:body/w:tbl", "w:body"),
            ("w:body/w:sectPr", "w:body/w:sectPr"),
            ("w:body/(w:p, w:sectPr)", "w:body/w:sectPr"),
        ]
    )
    def clear_fixture(self, request):
        before_cxml, after_cxml = request.param
        body = element(before_cxml)
        expected_xml = xml(after_cxml)
        return body, expected_xml

    @pytest.fixture
    def section_break_fixture(self):
        body = element("w:body/w:sectPr/w:type{w:val=foobar}")
        expected_xml = xml(
            "w:body/("
            "  w:p/w:pPr/w:sectPr/w:type{w:val=foobar},"
            "  w:sectPr/w:type{w:val=foobar}"
            ")"
        )
        return body, expected_xml
