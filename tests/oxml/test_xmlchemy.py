# encoding: utf-8

"""
Test suite for docx.oxml.xmlchemy
"""

from __future__ import absolute_import, print_function, unicode_literals

import pytest

from docx.oxml.xmlchemy import XmlString


class DescribeXmlString(object):

    def it_parses_a_line_to_help_compare(self, parse_fixture):
        """
        This internal function is important to test separately because if it
        doesn't parse a line properly, false equality can result.
        """
        line, expected_front, expected_attrs = parse_fixture[:3]
        expected_close, expected_text = parse_fixture[3:]
        front, attrs, close, text = XmlString._parse_line(line)
        # print("'%s' '%s' '%s' %s" % (
        #     front, attrs, close, ('%s' % text) if text else text))
        assert front == expected_front
        assert attrs == expected_attrs
        assert close == expected_close
        assert text == expected_text

    def it_knows_if_two_xml_lines_are_equivalent(self, xml_line_case):
        line, other, differs = xml_line_case
        xml = XmlString(line)
        assert xml == other
        assert xml != differs

    # fixtures ---------------------------------------------

    @pytest.fixture(params=[
        ('<a>text</a>',  '<a',   '',       '>',  'text</a>'),
        ('<a:f/>',       '<a:f', '',       '/>', None),
        ('<a:f b="c"/>', '<a:f', ' b="c"', '/>', None),
        ('<a:f>t</a:f>', '<a:f', '',       '>',  't</a:f>'),
        ('<dcterms:created xsi:type="dcterms:W3CDTF">2013-12-23T23:15:00Z</d'
         'cterms:created>', '<dcterms:created', ' xsi:type="dcterms:W3CDTF"',
         '>', '2013-12-23T23:15:00Z</dcterms:created>'),
    ])
    def parse_fixture(self, request):
        line, front, attrs, close, text = request.param
        return line, front, attrs, close, text

    @pytest.fixture(params=[
        'simple_elm', 'nsp_tagname', 'indent', 'attrs', 'nsdecl_order',
        'closing_elm',
    ])
    def xml_line_case(self, request):
        cases = {
            'simple_elm': (
                '<name/>',
                '<name/>',
                '<name>',
            ),
            'nsp_tagname': (
                '<xyz:name/>',
                '<xyz:name/>',
                '<abc:name/>',
            ),
            'indent': (
                '  <xyz:name/>',
                '  <xyz:name/>',
                '<xyz:name/>',
            ),
            'attrs': (
                '  <abc:Name foo="bar" bar="foo">',
                '  <abc:Name bar="foo" foo="bar">',
                '  <abc:Name far="boo" foo="bar">',
            ),
            'nsdecl_order': (
                '    <name xmlns:a="http://ns/1" xmlns:b="http://ns/2"/>',
                '    <name xmlns:b="http://ns/2" xmlns:a="http://ns/1"/>',
                '    <name xmlns:b="http://ns/2" xmlns:a="http://ns/1">',
            ),
            'closing_elm': (
                '</xyz:name>',
                '</xyz:name>',
                '<xyz:name>',
            ),
        }
        line, other, differs = cases[request.param]
        return line, other, differs
