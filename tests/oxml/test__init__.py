# encoding: utf-8

"""
Test suite for pptx.oxml.__init__.py module, primarily XML parser-related.
"""

from __future__ import print_function, unicode_literals

import pytest

from lxml import etree

from docx.oxml import oxml_parser


class DescribeOxmlParser(object):

    def it_strips_whitespace_between_elements(self, whitespace_fixture):
        pretty_xml_text, stripped_xml_text = whitespace_fixture
        element = etree.fromstring(pretty_xml_text, oxml_parser)
        xml_text = etree.tostring(element, encoding='unicode')
        assert xml_text == stripped_xml_text

    # fixtures -------------------------------------------------------

    @pytest.fixture
    def whitespace_fixture(self):
        pretty_xml_text = (
            '<foø>\n'
            '  <bår>text</bår>\n'
            '</foø>\n'
        )
        stripped_xml_text = '<foø><bår>text</bår></foø>'
        return pretty_xml_text, stripped_xml_text
