# encoding: utf-8

"""Unit test suite for the docx.parts.hdrftr module"""

from __future__ import absolute_import, division, print_function, unicode_literals

import pytest

from docx.opc.constants import CONTENT_TYPE as CT, RELATIONSHIP_TYPE as RT
from docx.opc.part import PartFactory
from docx.package import Package
from docx.parts.hdrftr import FooterPart, HeaderPart

from ..unitutil.cxml import element
from ..unitutil.mock import function_mock, initializer_mock, instance_mock, method_mock


class DescribeFooterPart(object):

    def it_is_used_by_loader_to_construct_footer_part(
        self, package_, FooterPart_load_, footer_part_
    ):
        partname = "footer1.xml"
        content_type = CT.WML_FOOTER
        reltype = RT.FOOTER
        blob = "<w:ftr/>"
        FooterPart_load_.return_value = footer_part_

        part = PartFactory(partname, content_type, reltype, blob, package_)

        FooterPart_load_.assert_called_once_with(partname, content_type, blob, package_)
        assert part is footer_part_

    def it_can_create_a_new_footer_part(
        self, package_, _default_footer_xml_, parse_xml_, _init_
    ):
        ftr = element("w:ftr")
        package_.next_partname.return_value = "/word/footer24.xml"
        _default_footer_xml_.return_value = "<w:ftr>"
        parse_xml_.return_value = ftr

        footer_part = FooterPart.new(package_)

        package_.next_partname.assert_called_once_with("/word/footer%d.xml")
        _default_footer_xml_.assert_called_once_with()
        parse_xml_.assert_called_once_with("<w:ftr>")
        _init_.assert_called_once_with(
            footer_part, "/word/footer24.xml", CT.WML_FOOTER, ftr, package_
        )

    def it_loads_default_footer_XML_from_a_template_to_help(self):
        # ---tests integration with OS---
        xml_bytes = FooterPart._default_footer_xml()

        assert xml_bytes.startswith(
            b"<?xml version='1.0' encoding='UTF-8' standalone='yes'?>\n<w:ftr\n"
        )
        assert len(xml_bytes) == 1395

    # fixture components ---------------------------------------------

    @pytest.fixture
    def _default_footer_xml_(self, request):
        return method_mock(request, FooterPart, "_default_footer_xml", autospec=False)

    @pytest.fixture
    def footer_part_(self, request):
        return instance_mock(request, FooterPart)

    @pytest.fixture
    def FooterPart_load_(self, request):
        return method_mock(request, FooterPart, "load", autospec=False)

    @pytest.fixture
    def _init_(self, request):
        return initializer_mock(request, FooterPart)

    @pytest.fixture
    def package_(self, request):
        return instance_mock(request, Package)

    @pytest.fixture
    def parse_xml_(self, request):
        return function_mock(request, "docx.parts.hdrftr.parse_xml")


class DescribeHeaderPart(object):

    def it_is_used_by_loader_to_construct_header_part(
        self, package_, HeaderPart_load_, header_part_
    ):
        partname = "header1.xml"
        content_type = CT.WML_HEADER
        reltype = RT.HEADER
        blob = "<w:hdr/>"
        HeaderPart_load_.return_value = header_part_

        part = PartFactory(partname, content_type, reltype, blob, package_)

        HeaderPart_load_.assert_called_once_with(partname, content_type, blob, package_)
        assert part is header_part_

    def it_can_create_a_new_header_part(
        self, package_, _default_header_xml_, parse_xml_, _init_
    ):
        hdr = element("w:hdr")
        package_.next_partname.return_value = "/word/header42.xml"
        _default_header_xml_.return_value = "<w:hdr>"
        parse_xml_.return_value = hdr

        header_part = HeaderPart.new(package_)

        package_.next_partname.assert_called_once_with("/word/header%d.xml")
        _default_header_xml_.assert_called_once_with()
        parse_xml_.assert_called_once_with("<w:hdr>")
        _init_.assert_called_once_with(
            header_part, "/word/header42.xml", CT.WML_HEADER, hdr, package_
        )

    def it_loads_default_header_XML_from_a_template_to_help(self):
        # ---tests integration with OS---
        xml_bytes = HeaderPart._default_header_xml()

        assert xml_bytes.startswith(
            b"<?xml version='1.0' encoding='UTF-8' standalone='yes'?>\n<w:hdr\n"
        )
        assert len(xml_bytes) == 1395

    # fixture components ---------------------------------------------

    @pytest.fixture
    def _default_header_xml_(self, request):
        return method_mock(request, HeaderPart, "_default_header_xml", autospec=False)

    @pytest.fixture
    def HeaderPart_load_(self, request):
        return method_mock(request, HeaderPart, "load", autospec=False)

    @pytest.fixture
    def header_part_(self, request):
        return instance_mock(request, HeaderPart)

    @pytest.fixture
    def _init_(self, request):
        return initializer_mock(request, HeaderPart)

    @pytest.fixture
    def package_(self, request):
        return instance_mock(request, Package)

    @pytest.fixture
    def parse_xml_(self, request):
        return function_mock(request, "docx.parts.hdrftr.parse_xml")
