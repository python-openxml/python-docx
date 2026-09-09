# pyright: reportPrivateUsage=false

"""Unit test suite for the docx.opc.coreprops module."""

from __future__ import annotations

import datetime as dt
from typing import TYPE_CHECKING, cast

import pytest

from docx.opc.coreprops import CoreProperties
from docx.oxml.parser import parse_xml

if TYPE_CHECKING:
    from docx.oxml.coreprops import CT_CoreProperties


class DescribeCoreProperties:
    """Unit-test suite for `docx.opc.coreprops.CoreProperties` objects."""

    @pytest.mark.parametrize(
        ("prop_name", "expected_value"),
        [
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
        ],
    )
    def it_knows_the_string_property_values(
        self, prop_name: str, expected_value: str, core_properties: CoreProperties
    ):
        actual_value = getattr(core_properties, prop_name)
        assert actual_value == expected_value

    @pytest.mark.parametrize(
        ("prop_name", "tagname", "value"),
        [
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
        ],
    )
    def it_can_change_the_string_property_values(self, prop_name: str, tagname: str, value: str):
        coreProperties = self.coreProperties(tagname="", str_val="")
        core_properties = CoreProperties(cast("CT_CoreProperties", parse_xml(coreProperties)))

        setattr(core_properties, prop_name, value)

        assert core_properties._element.xml == self.coreProperties(tagname, value)

    @pytest.mark.parametrize(
        ("prop_name", "expected_datetime"),
        [
            ("created", dt.datetime(2012, 11, 17, 16, 37, 40, tzinfo=dt.timezone.utc)),
            ("last_printed", dt.datetime(2014, 6, 4, 4, 28, tzinfo=dt.timezone.utc)),
            ("modified", None),
        ],
    )
    def it_knows_the_date_property_values(
        self, prop_name: str, expected_datetime: dt.datetime, core_properties: CoreProperties
    ):
        actual_datetime = getattr(core_properties, prop_name)
        assert actual_datetime == expected_datetime

    @pytest.mark.parametrize(
        ("prop_name", "tagname"),
        [
            ("created", "dcterms:created"),
            ("modified", "dcterms:modified"),
            ("last_printed", "cp:lastPrinted"),
        ],
    )
    @pytest.mark.parametrize(
        ("str_val", "expected_datetime"),
        [
            ("1997", dt.datetime(1997, 1, 1, tzinfo=dt.timezone.utc)),
            ("1997-07", dt.datetime(1997, 7, 1, tzinfo=dt.timezone.utc)),
            ("1997-07-16", dt.datetime(1997, 7, 16, tzinfo=dt.timezone.utc)),
            ("1997-07-16T19:20:30Z", dt.datetime(1997, 7, 16, 19, 20, 30, tzinfo=dt.timezone.utc)),
            (
                "1997-07-16T19:20:30+01:00",
                dt.datetime(1997, 7, 16, 18, 20, 30, tzinfo=dt.timezone.utc),
            ),
            (
                "1997-07-16T19:20:30.45+01:00",
                dt.datetime(1997, 7, 16, 18, 20, 30, 450000, tzinfo=dt.timezone.utc),
            ),
            (
                "1997-07-16T19:20:30.1234Z",
                dt.datetime(1997, 7, 16, 19, 20, 30, 123400, tzinfo=dt.timezone.utc),
            ),
            (
                "1997-07-16T23:45:30.987654-05:30",
                dt.datetime(1997, 7, 17, 5, 15, 30, 987654, tzinfo=dt.timezone.utc),
            ),
            (
                "1997-01-01T00:15:30.1+05:45",
                dt.datetime(1996, 12, 31, 18, 30, 30, 100000, tzinfo=dt.timezone.utc),
            ),
            (
                "1997-07-16T19:20:30.123456789Z",
                dt.datetime(1997, 7, 16, 19, 20, 30, 123456, tzinfo=dt.timezone.utc),
            ),
            (
                "1997-07-16T19:20:30.0Z",
                dt.datetime(1997, 7, 16, 19, 20, 30, tzinfo=dt.timezone.utc),
            ),
            ("not a date", None),
        ],
    )
    def it_reads_date_properties_with_fractional_seconds(
        self, prop_name: str, tagname: str, str_val: str, expected_datetime: dt.datetime | None
    ):
        xml = self.coreProperties(tagname, str_val)
        core_properties = CoreProperties(cast("CT_CoreProperties", parse_xml(xml)))

        assert getattr(core_properties, prop_name) == expected_datetime

    @pytest.mark.parametrize(
        ("prop_name", "tagname", "value", "str_val", "attrs"),
        [
            (
                "created",
                "dcterms:created",
                dt.datetime(2001, 2, 3, 4, 5),
                "2001-02-03T04:05:00Z",
                ' xsi:type="dcterms:W3CDTF"',
            ),
            (
                "last_printed",
                "cp:lastPrinted",
                dt.datetime(2014, 6, 4, 4),
                "2014-06-04T04:00:00Z",
                "",
            ),
            (
                "modified",
                "dcterms:modified",
                dt.datetime(2005, 4, 3, 2, 1),
                "2005-04-03T02:01:00Z",
                ' xsi:type="dcterms:W3CDTF"',
            ),
        ],
    )
    def it_can_change_the_date_property_values(
        self, prop_name: str, tagname: str, value: dt.datetime, str_val: str, attrs: str
    ):
        coreProperties = self.coreProperties(tagname="", str_val="")
        core_properties = CoreProperties(cast("CT_CoreProperties", parse_xml(coreProperties)))
        expected_xml = self.coreProperties(tagname, str_val, attrs)

        setattr(core_properties, prop_name, value)

        assert core_properties._element.xml == expected_xml

    @pytest.mark.parametrize(
        ("str_val", "expected_value"),
        [("42", 42), (None, 0), ("foobar", 0), ("-17", 0), ("32.7", 0)],
    )
    def it_knows_the_revision_number(self, str_val: str | None, expected_value: int):
        tagname, str_val = ("cp:revision", str_val) if str_val else ("", "")
        coreProperties = self.coreProperties(tagname, str_val or "")
        core_properties = CoreProperties(cast("CT_CoreProperties", parse_xml(coreProperties)))

        assert core_properties.revision == expected_value

    @pytest.mark.parametrize(("value", "str_val"), [(42, "42")])
    def it_can_change_the_revision_number(self, value: int, str_val: str):
        coreProperties = self.coreProperties(tagname="", str_val="")
        core_properties = CoreProperties(cast("CT_CoreProperties", parse_xml(coreProperties)))
        expected_xml = self.coreProperties("cp:revision", str_val)

        core_properties.revision = value

        assert core_properties._element.xml == expected_xml

    # fixtures -------------------------------------------------------

    def coreProperties(self, tagname: str, str_val: str, attrs: str = "") -> str:
        tmpl = (
            "<cp:coreProperties"
            ' xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties"'
            ' xmlns:dc="http://purl.org/dc/elements/1.1/"'
            ' xmlns:dcmitype="http://purl.org/dc/dcmitype/"'
            ' xmlns:dcterms="http://purl.org/dc/terms/"'
            ' xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"'
            ">%s</cp:coreProperties>\n"
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
        element = cast(
            "CT_CoreProperties",
            parse_xml(
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
            ),
        )
        return CoreProperties(element)
