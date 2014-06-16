# encoding: utf-8

"""
Test suite for docx.oxml.xmlchemy
"""

from __future__ import absolute_import, print_function, unicode_literals

import pytest

from docx.compat import Unicode
from docx.oxml import parse_xml
from docx.oxml.ns import qn
from docx.oxml.xmlchemy import serialize_for_reading, XmlString

from .unitdata.text import a_b, a_u, an_i, an_rPr


class DescribeBaseOxmlElement(object):

    def it_can_find_the_first_of_its_children_named_in_a_sequence(
            self, first_fixture):
        element, tagnames, matching_child = first_fixture
        assert element.first_child_found_in(*tagnames) is matching_child

    def it_can_insert_an_element_before_named_successors(
            self, insert_fixture):
        element, child, tagnames, expected_xml = insert_fixture
        element.insert_element_before(child, *tagnames)
        assert element.xml == expected_xml

    def it_can_remove_all_children_with_name_in_sequence(
            self, remove_fixture):
        element, tagnames, expected_xml = remove_fixture
        element.remove_all(*tagnames)
        assert element.xml == expected_xml

    # fixtures ---------------------------------------------

    @pytest.fixture(params=[
        ('biu', 'iu',  'i'),
        ('bu',  'iu',  'u'),
        ('bi',  'u',   None),
        ('b',   'iu',  None),
        ('iu',  'biu', 'i'),
        ('',    'biu', None),
    ])
    def first_fixture(self, request):
        present, matching, match = request.param
        element = self.rPr_bldr(present).element
        tagnames = self.nsptags(matching)
        matching_child = element.find(qn('w:%s' % match)) if match else None
        return element, tagnames, matching_child

    @pytest.fixture(params=[
        ('iu', 'b', 'iu', 'biu'),
        ('u',  'b', 'iu', 'bu'),
        ('',   'b', 'iu', 'b'),
        ('bu', 'i', 'u',  'biu'),
        ('bi', 'u', '',   'biu'),
    ])
    def insert_fixture(self, request):
        present, new, successors, after = request.param
        element = self.rPr_bldr(present).element
        child = {
            'b': a_b(), 'i': an_i(), 'u': a_u()
        }[new].with_nsdecls().element
        tagnames = [('w:%s' % char) for char in successors]
        expected_xml = self.rPr_bldr(after).xml()
        return element, child, tagnames, expected_xml

    @pytest.fixture(params=[
        ('biu', 'b', 'iu'), ('biu', 'bi', 'u'), ('bbiiuu',  'i',   'bbuu'),
        ('biu', 'i', 'bu'), ('biu', 'bu', 'i'), ('bbiiuu',   '', 'bbiiuu'),
        ('biu', 'u', 'bi'), ('biu', 'ui', 'b'), ('bbiiuu', 'bi',     'uu'),
        ('bu',  'i', 'bu'), ('',    'ui',  ''),
    ])
    def remove_fixture(self, request):
        present, remove, after = request.param
        element = self.rPr_bldr(present).element
        tagnames = self.nsptags(remove)
        expected_xml = self.rPr_bldr(after).xml()
        return element, tagnames, expected_xml

    # fixture components ---------------------------------------------

    def nsptags(self, letters):
        return [('w:%s' % letter) for letter in letters]

    def rPr_bldr(self, children):
        rPr_bldr = an_rPr().with_nsdecls()
        for char in children:
            if char == 'b':
                rPr_bldr.with_child(a_b())
            elif char == 'i':
                rPr_bldr.with_child(an_i())
            elif char == 'u':
                rPr_bldr.with_child(a_u())
            else:
                raise NotImplementedError("got '%s'" % char)
        return rPr_bldr


class DescribeSerializeForReading(object):

    def it_pretty_prints_an_lxml_element(self, pretty_fixture):
        element, expected_xml_text = pretty_fixture
        xml_text = serialize_for_reading(element)
        assert xml_text == expected_xml_text

    def it_returns_unicode_text(self, type_fixture):
        element = type_fixture
        xml_text = serialize_for_reading(element)
        assert isinstance(xml_text, Unicode)

    # fixtures ---------------------------------------------

    @pytest.fixture
    def pretty_fixture(self, element):
        expected_xml_text = (
            '<foø>\n'
            '  <bår>text</bår>\n'
            '</foø>\n'
        )
        return element, expected_xml_text

    @pytest.fixture
    def type_fixture(self, element):
        return element

    # fixture components -----------------------------------

    @pytest.fixture
    def element(self):
        return parse_xml('<foø><bår>text</bår></foø>')


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
