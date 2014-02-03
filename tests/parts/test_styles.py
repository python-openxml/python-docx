# encoding: utf-8

"""
Test suite for the docx.parts.styles module
"""

from __future__ import absolute_import, print_function, unicode_literals

import pytest

from docx.opc.constants import CONTENT_TYPE as CT, RELATIONSHIP_TYPE as RT
from docx.opc.package import PartFactory
from docx.opc.packuri import PackURI
from docx.oxml.parts.styles import CT_Styles
from docx.package import Package
from docx.parts.styles import StylesPart

from ..unitutil import (
    function_mock, initializer_mock, instance_mock, method_mock
)


class DescribeStylesPart(object):

    def it_is_used_by_PartFactory_to_construct_styles_part(
            self, load_fixture):
        # fixture ----------------------
        styles_part_load_, partname_, blob_, package_, styles_part_ = (
            load_fixture
        )
        content_type, reltype = CT.WML_STYLES, RT.STYLES
        # exercise ---------------------
        part = PartFactory(partname_, content_type, reltype, blob_, package_)
        # verify -----------------------
        styles_part_load_.assert_called_once_with(
            partname_, content_type, blob_, package_
        )
        assert part is styles_part_

    def it_can_be_constructed_by_opc_part_factory(self, construct_fixture):
        (partname_, content_type_, blob_, package_, oxml_fromstring_,
         init__, styles_elm_) = construct_fixture
        # exercise ---------------------
        styles_part = StylesPart.load(
            partname_, content_type_, blob_, package_
        )
        # verify -----------------------
        oxml_fromstring_.assert_called_once_with(blob_)
        init__.assert_called_once_with(
            partname_, content_type_, styles_elm_, package_
        )
        assert isinstance(styles_part, StylesPart)

    # fixtures -------------------------------------------------------

    @pytest.fixture
    def blob_(self, request):
        return instance_mock(request, bytes)

    @pytest.fixture
    def construct_fixture(
            self, partname_, content_type_, blob_, package_,
            oxml_fromstring_, init__, styles_elm_):
        return (
            partname_, content_type_, blob_, package_, oxml_fromstring_,
            init__, styles_elm_
        )

    @pytest.fixture
    def content_type_(self, request):
        return instance_mock(request, str)

    @pytest.fixture
    def init__(self, request):
        return initializer_mock(request, StylesPart)

    @pytest.fixture
    def load_fixture(
            self, styles_part_load_, partname_, blob_, package_,
            styles_part_):
        styles_part_load_.return_value = styles_part_
        return (
            styles_part_load_, partname_, blob_, package_, styles_part_
        )

    @pytest.fixture
    def oxml_fromstring_(self, request, styles_elm_):
        return function_mock(
            request, 'docx.parts.styles.oxml_fromstring',
            return_value=styles_elm_
        )

    @pytest.fixture
    def package_(self, request):
        return instance_mock(request, Package)

    @pytest.fixture
    def partname_(self, request):
        return instance_mock(request, PackURI)

    @pytest.fixture
    def styles_elm_(self, request):
        return instance_mock(request, CT_Styles)

    @pytest.fixture
    def styles_part_(self, request):
        return instance_mock(request, StylesPart)

    @pytest.fixture
    def styles_part_load_(self, request):
        return method_mock(request, StylesPart, 'load')
