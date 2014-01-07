# encoding: utf-8

"""
Test suite for docx.oxml.shared
"""

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

import pytest

from docx.oxml.shared import XmlString


class DescribeXmlString(object):

    def it_knows_if_two_xml_lines_are_equivalent(self, xml_line_case):
        line, other, differs = xml_line_case
        xml = XmlString(line)
        assert xml == other
        assert xml != differs

    # fixtures ---------------------------------------------

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
