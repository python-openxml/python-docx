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
from docx.parts.numbering import NumberingPart, _NumberingDefinitions

from ..oxml.unitdata.numbering import a_num, a_numbering
from ..unitutil import (
    function_mock, class_mock, initializer_mock, instance_mock, method_mock
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
        (partname_, content_type_, blob_, package_, parse_xml_, init__,
         numbering_elm_) = construct_fixture
        # exercise ---------------------
        numbering_part = NumberingPart.load(
            partname_, content_type_, blob_, package_
        )
        # verify -----------------------
        parse_xml_.assert_called_once_with(blob_)
        init__.assert_called_once_with(
            partname_, content_type_, numbering_elm_, package_
        )
        assert isinstance(numbering_part, NumberingPart)

    def it_provides_access_to_the_numbering_definitions(
            self, num_defs_fixture):
        (numbering_part, _NumberingDefinitions_, numbering_elm_,
         numbering_definitions_) = num_defs_fixture
        numbering_definitions = numbering_part.numbering_definitions
        _NumberingDefinitions_.assert_called_once_with(numbering_elm_)
        assert numbering_definitions is numbering_definitions_

    # fixtures -------------------------------------------------------

    @pytest.fixture
    def construct_fixture(
            self, partname_, content_type_, blob_, package_, parse_xml_,
            init__, numbering_elm_):
        return (
            partname_, content_type_, blob_, package_, parse_xml_, init__,
            numbering_elm_
        )

    @pytest.fixture
    def load_fixture(
            self, numbering_part_load_, partname_, blob_, package_,
            numbering_part_):
        numbering_part_load_.return_value = numbering_part_
        return (
            numbering_part_load_, partname_, blob_, package_, numbering_part_
        )

    @pytest.fixture
    def num_defs_fixture(
            self, _NumberingDefinitions_, numbering_elm_,
            numbering_definitions_):
        numbering_part = NumberingPart(None, None, numbering_elm_, None)
        return (
            numbering_part, _NumberingDefinitions_, numbering_elm_,
            numbering_definitions_
        )

    # fixture components ---------------------------------------------

    @pytest.fixture
    def blob_(self, request):
        return instance_mock(request, bytes)

    @pytest.fixture
    def content_type_(self, request):
        return instance_mock(request, str)

    @pytest.fixture
    def init__(self, request):
        return initializer_mock(request, NumberingPart)

    @pytest.fixture
    def _NumberingDefinitions_(self, request, numbering_definitions_):
        return class_mock(
            request, 'docx.parts.numbering._NumberingDefinitions',
            return_value=numbering_definitions_
        )

    @pytest.fixture
    def numbering_definitions_(self, request):
        return instance_mock(request, _NumberingDefinitions)

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
    def parse_xml_(self, request, numbering_elm_):
        return function_mock(
            request, 'docx.parts.numbering.parse_xml',
            return_value=numbering_elm_
        )

    @pytest.fixture
    def package_(self, request):
        return instance_mock(request, Package)

    @pytest.fixture
    def partname_(self, request):
        return instance_mock(request, PackURI)


class Describe_NumberingDefinitions(object):

    def it_knows_how_many_numbering_definitions_it_contains(
            self, len_fixture):
        numbering_definitions, numbering_definition_count = len_fixture
        assert len(numbering_definitions) == numbering_definition_count

    # fixtures -------------------------------------------------------

    @pytest.fixture(params=[0, 1, 2, 3])
    def len_fixture(self, request):
        numbering_definition_count = request.param
        numbering_bldr = a_numbering().with_nsdecls()
        for idx in range(numbering_definition_count):
            numbering_bldr.with_child(a_num())
        numbering_elm = numbering_bldr.element
        numbering_definitions = _NumberingDefinitions(numbering_elm)
        return numbering_definitions, numbering_definition_count
