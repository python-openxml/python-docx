# encoding: utf-8

"""
Test suite for the docx.header module
"""

from __future__ import (
    absolute_import, print_function, unicode_literals, division
)

import pytest

from docx.enum.header import WD_HEADER_FOOTER
from docx.header import _BaseHeaderFooter, Header, HeaderFooterBody
from docx.parts.document import DocumentPart
from docx.parts.header import HeaderPart

from .unitutil.cxml import element
from .unitutil.mock import call, instance_mock, method_mock, property_mock


class Describe_BaseHeaderFooter(object):

    def it_knows_whether_it_is_linked_to_previous(self, is_linked_fixture):
        header, expected_value = is_linked_fixture
        assert header.is_linked_to_previous is expected_value

    def it_provides_access_to_its_body(self, body_fixture):
        header, calls, expected_value = body_fixture
        body = header.body
        assert header.part.related_hdrftr_body.call_args_list == calls
        assert body == expected_value

    def it_provides_access_to_the_related_hdrftr_body(self, hdrftr_fixture):
        document_part, get_related_parts, header_part_ = hdrftr_fixture
        rId = 'rId1'
        body = document_part.related_hdrftr_body(rId)
        get_related_parts.assert_called_once_with(rId)
        assert body == header_part_.body

    # fixtures -------------------------------------------------------

    @pytest.fixture
    def hdrftr_fixture(self, request, header_part_, body_):
        header_part_.body = body_
        document_part = DocumentPart(None, None, None, None)

        get_related_part = method_mock(
            request,
            DocumentPart,
            'get_related_part')
        get_related_part.return_value = header_part_

        return document_part, get_related_part, header_part_

    @pytest.fixture(params=[
        ('w:sectPr',                                             None),
        ('w:sectPr/w:headerReference{w:type=even,r:id=rId6}',    None),
        ('w:sectPr/w:headerReference{w:type=default,r:id=rId8}', 'rId8'),
    ])
    def body_fixture(self, request, body_, part_prop_, document_part_):
        sectPr_cxml, rId = request.param
        header = Header(element(sectPr_cxml), None, WD_HEADER_FOOTER.PRIMARY)
        calls, expected_value = ([call(rId)], body_) if rId else ([], None)
        document_part_.related_hdrftr_body.return_value = body_
        return header, calls, expected_value

    @pytest.fixture(params=[
        ('w:sectPr',                                   True),
        ('w:sectPr/w:headerReference{w:type=default}', False),
        ('w:sectPr/w:headerReference{w:type=even}',    True),
    ])
    def is_linked_fixture(self, request):
        sectPr_cxml, expected_value = request.param
        header = Header(element(sectPr_cxml), None, WD_HEADER_FOOTER.PRIMARY)
        return header, expected_value

    # fixture components ---------------------------------------------

    @pytest.fixture
    def body_(self, request):
        return instance_mock(request, HeaderFooterBody)

    @pytest.fixture
    def document_part_(self, request):
        return instance_mock(request, DocumentPart)

    @pytest.fixture
    def header_part_(self, request):
        return instance_mock(request, HeaderPart)

    @pytest.fixture
    def part_prop_(self, request, document_part_):
        return property_mock(
            request, _BaseHeaderFooter, 'part', return_value=document_part_
        )
