# encoding: utf-8

"""
Test suite for the docx.parts.numbering module
"""

from __future__ import absolute_import, print_function, unicode_literals

import pytest

from docx.opc.constants import CONTENT_TYPE as CT, RELATIONSHIP_TYPE as RT
from docx.opc.package import PartFactory
from docx.opc.packuri import PackURI
from docx.oxml.parts.numbering import CT_Numbering
from docx.package import Package
from docx.parts.numbering import NumberingPart

from ..unitutil import (
    function_mock, initializer_mock, instance_mock, method_mock
)


class DescribeNumberingPart(object):

    def it_is_used_by_PartFactory_to_construct_numbering_part(
            self, load_fixture):
        # fixture ----------------------
        numbering_part_load_, partname_, blob_, package_, numbering_part_ = (
            load_fixture
        )
        content_type, reltype = CT.WML_NUMBERING, RT.NUMBERING
        # exercise ---------------------
        part = PartFactory(partname_, content_type, reltype, blob_, package_)
        # verify -----------------------
        numbering_part_load_.assert_called_once_with(
            partname_, content_type, blob_, package_
        )
        assert part is numbering_part_

    def it_can_be_constructed_by_opc_part_factory(self, construct_fixture):
        (partname_, content_type_, blob_, package_, oxml_fromstring_,
         init__, numbering_elm_) = construct_fixture
        # exercise ---------------------
        numbering_part = NumberingPart.load(
            partname_, content_type_, blob_, package_
        )
        # verify -----------------------
        oxml_fromstring_.assert_called_once_with(blob_)
        init__.assert_called_once_with(
            partname_, content_type_, numbering_elm_, package_
        )
        assert isinstance(numbering_part, NumberingPart)

    # fixtures -------------------------------------------------------

    @pytest.fixture
    def blob_(self, request):
        return instance_mock(request, bytes)

    @pytest.fixture
    def construct_fixture(
            self, partname_, content_type_, blob_, package_,
            oxml_fromstring_, init__, numbering_elm_):
        return (
            partname_, content_type_, blob_, package_, oxml_fromstring_,
            init__, numbering_elm_
        )

    @pytest.fixture
    def content_type_(self, request):
        return instance_mock(request, str)

    @pytest.fixture
    def init__(self, request):
        return initializer_mock(request, NumberingPart)

    @pytest.fixture
    def load_fixture(
            self, numbering_part_load_, partname_, blob_, package_,
            numbering_part_):
        numbering_part_load_.return_value = numbering_part_
        return (
            numbering_part_load_, partname_, blob_, package_, numbering_part_
        )

    @pytest.fixture
    def numbering_elm_(self, request):
        return instance_mock(request, CT_Numbering)

    @pytest.fixture
    def numbering_part_(self, request):
        return instance_mock(request, NumberingPart)

    @pytest.fixture
    def numbering_part_load_(self, request):
        return method_mock(request, NumberingPart, 'load')

    @pytest.fixture
    def oxml_fromstring_(self, request, numbering_elm_):
        return function_mock(
            request, 'docx.parts.numbering.oxml_fromstring',
            return_value=numbering_elm_
        )

    @pytest.fixture
    def package_(self, request):
        return instance_mock(request, Package)

    @pytest.fixture
    def partname_(self, request):
        return instance_mock(request, PackURI)
