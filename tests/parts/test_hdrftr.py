# encoding: utf-8

"""Unit test suite for the docx.parts.hdrftr module"""

from __future__ import absolute_import, division, print_function, unicode_literals

import pytest

from docx.opc.constants import CONTENT_TYPE as CT
from docx.package import Package
from docx.parts.hdrftr import HeaderPart

from ..unitutil.cxml import element
from ..unitutil.mock import function_mock, initializer_mock, instance_mock, method_mock


class DescribeHeaderPart(object):

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
    def _init_(self, request):
        return initializer_mock(request, HeaderPart, autospec=True)

    @pytest.fixture
    def package_(self, request):
        return instance_mock(request, Package)

    @pytest.fixture
    def parse_xml_(self, request):
        return function_mock(request, "docx.parts.hdrftr.parse_xml")
