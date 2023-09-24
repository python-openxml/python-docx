# encoding: utf-8

"""
Unit test suite for the docx.opc.coreprops module
"""

from __future__ import absolute_import, division, print_function, unicode_literals

import pytest

from datetime import datetime

from docx.opc.coreprops import CoreProperties
from docx.oxml import parse_xml


class DescribeCoreProperties(object):
    def it_knows_the_string_property_values(self, text_prop_get_fixture):
        core_properties, prop_name, expected_value = text_prop_get_fixture
        actual_value = getattr(core_properties, prop_name)
        assert actual_value == expected_value

    def it_can_change_the_string_property_values(self, text_prop_set_fixture):
        core_properties, prop_name, value, expected_xml = text_prop_set_fixture
        setattr(core_properties, prop_name, value)
        assert core_properties._element.xml == expected_xml

    def it_knows_the_date_property_values(self, date_prop_get_fixture):
        core_properties, prop_name, expected_datetime = date_prop_get_fixture
        actual_datetime = getattr(core_properties, prop_name)
        assert actual_datetime == expected_datetime

    def it_can_change_the_date_property_values(self, date_prop_set_fixture):
        core_properties, prop_name, value, expected_xml = date_prop_set_fixture
        setattr(core_properties, prop_name, value)
        assert core_properties._element.xml == expected_xml

    def it_knows_the_revision_number(self, revision_get_fixture):
        core_properties, expected_revision = revision_get_fixture
        assert core_properties.revision == expected_revision

    def it_can_change_the_revision_number(self, revision_set_fixture):
        core_properties, revision, expected_xml = revision_set_fixture
        core_properties.revision = revision
        assert core_properties._element.xml == expected_xml

    # fixtures -------------------------------------------------------

    @pytest.fixture(
        params=[
            ("created", datetime(2012, 11, 17, 16, 37, 40)),
            ("last_printed", datetime(2014, 6, 4, 4, 28)),
            ("modified", None),
        ]
    )
    def date_prop_get_fixture(self, request, core_properties):
        prop_name, expected_datetime = request.param
        return core_properties, prop_name, expected_datetime

    @pytest.fixture(
        params=[
            (
                "created",
                "dcterms:created",
                datetime(2001, 2, 3, 4, 5),
                "2001-02-03T04:05:00Z",
                ' xsi:type="dcterms:W3CDTF"',
            ),
            (
                "last_printed",
                "cp:lastPrinted",
                datetime(2014, 6, 4, 4),
                "2014-06-04T04:00:00Z",
                "",
            ),
            (
                "modified",
                "dcterms:modified",
                datetime(2005, 4, 3, 2, 1),
                "2005-04-03T02:01:00Z",
                ' xsi:type="dcterms:W3CDTF"',
            ),
        ]
    )
    def date_prop_set_fixture(self, request):
        prop_name, tagname, value, str_val, attrs = request.param
        coreProperties = self.coreProperties(None, None)
        core_properties = CoreProperties(parse_xml(coreProperties))
        expected_xml = self.coreProperties(tagname, str_val, attrs)
        return core_properties, prop_name, value, expected_xml

    @pytest.fixture(
        params=[("42", 42), (None, 0), ("foobar", 0), ("-17", 0), ("32.7", 0)]
    )
    def revision_get_fixture(self, request):
        str_val, expected_revision = request.param
        tagname = "" if str_val is None else "cp:revision"
        coreProperties = self.coreProperties(tagname, str_val)
        core_properties = CoreProperties(parse_xml(coreProperties))
        return core_properties, expected_revision

    @pytest.fixture(
        params=[
            (42, "42"),
        ]
    )
    def revision_set_fixture(self, request):
        value, str_val = request.param
        coreProperties = self.coreProperties(None, None)
        core_properties = CoreProperties(parse_xml(coreProperties))
        expected_xml = self.coreProperties("cp:revision", str_val)
        return core_properties, value, expected_xml

    @pytest.fixture(
        params=[
            ("author", "python-docx"),
            ("category", ""),
            ("comments", ""),
            ("content_status", "DRAFT"),
            ("identifier", "GXS 10.2.1ab"),
            ("keywords", "foo bar baz"),
            ("language", "US-EN"),
            ("last_modified_by", "Steve Canny"),
            ("subject", "Spam"),
            ("title", "Word Document"),
            ("version", "1.2.88"),
        ]
    )
    def text_prop_get_fixture(self, request, core_properties):
        prop_name, expected_value = request.param
        return core_properties, prop_name, expected_value

    @pytest.fixture(
        params=[
            ("author", "dc:creator", "scanny"),
            ("category", "cp:category", "silly stories"),
            ("comments", "dc:description", "Bar foo to you"),
            ("content_status", "cp:contentStatus", "FINAL"),
            ("identifier", "dc:identifier", "GT 5.2.xab"),
            ("keywords", "cp:keywords", "dog cat moo"),
            ("language", "dc:language", "GB-EN"),
            ("last_modified_by", "cp:lastModifiedBy", "Billy Bob"),
            ("subject", "dc:subject", "Eggs"),
            ("title", "dc:title", "Dissertation"),
            ("version", "cp:version", "81.2.8"),
        ]
    )
    def text_prop_set_fixture(self, request):
        prop_name, tagname, value = request.param
        coreProperties = self.coreProperties(None, None)
        core_properties = CoreProperties(parse_xml(coreProperties))
        expected_xml = self.coreProperties(tagname, value)
        return core_properties, prop_name, value, expected_xml

    # fixture components ---------------------------------------------

    def coreProperties(self, tagname, str_val, attrs=""):
        tmpl = (
            '<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/'
            'package/2006/metadata/core-properties" xmlns:dc="http://purl.or'
            'g/dc/elements/1.1/" xmlns:dcmitype="http://purl.org/dc/dcmitype'
            '/" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:xsi="http://'
            'www.w3.org/2001/XMLSchema-instance">%s</cp:coreProperties>\n'
        )
        if not tagname:
            child_element = ""
        elif not str_val:
            child_element = "\n  <%s%s/>\n" % (tagname, attrs)
        else:
            child_element = "\n  <%s%s>%s</%s>\n" % (tagname, attrs, str_val, tagname)
        return tmpl % child_element

    @pytest.fixture
    def core_properties(self):
        element = parse_xml(
            b"<?xml version='1.0' encoding='UTF-8' standalone='yes'?>"
            b'\n<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.o'
            b'rg/package/2006/metadata/core-properties" xmlns:dc="http://pur'
            b'l.org/dc/elements/1.1/" xmlns:dcmitype="http://purl.org/dc/dcm'
            b'itype/" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:xsi="h'
            b'ttp://www.w3.org/2001/XMLSchema-instance">\n'
            b"  <cp:contentStatus>DRAFT</cp:contentStatus>\n"
            b"  <dc:creator>python-docx</dc:creator>\n"
            b'  <dcterms:created xsi:type="dcterms:W3CDTF">2012-11-17T11:07:'
            b"40-05:30</dcterms:created>\n"
            b"  <dc:description/>\n"
            b"  <dc:identifier>GXS 10.2.1ab</dc:identifier>\n"
            b"  <dc:language>US-EN</dc:language>\n"
            b"  <cp:lastPrinted>2014-06-04T04:28:00Z</cp:lastPrinted>\n"
            b"  <cp:keywords>foo bar baz</cp:keywords>\n"
            b"  <cp:lastModifiedBy>Steve Canny</cp:lastModifiedBy>\n"
            b"  <cp:revision>4</cp:revision>\n"
            b"  <dc:subject>Spam</dc:subject>\n"
            b"  <dc:title>Word Document</dc:title>\n"
            b"  <cp:version>1.2.88</cp:version>\n"
            b"</cp:coreProperties>\n"
        )
        return CoreProperties(element)
