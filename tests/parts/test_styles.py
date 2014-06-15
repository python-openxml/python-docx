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
from docx.parts.styles import StylesPart, _Styles

from ..oxml.unitdata.styles import a_style, a_styles
from ..unitutil import (
    function_mock, class_mock, initializer_mock, instance_mock, method_mock
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
        (partname_, content_type_, blob_, package_, parse_xml_, init__,
         styles_elm_) = construct_fixture
        # exercise ---------------------
        styles_part = StylesPart.load(
            partname_, content_type_, blob_, package_
        )
        # verify -----------------------
        parse_xml_.assert_called_once_with(blob_)
        init__.assert_called_once_with(
            partname_, content_type_, styles_elm_, package_
        )
        assert isinstance(styles_part, StylesPart)

    def it_provides_access_to_the_styles(self, styles_fixture):
        styles_part, _Styles_, styles_elm_, styles_ = styles_fixture
        styles = styles_part.styles
        _Styles_.assert_called_once_with(styles_elm_)
        assert styles is styles_

    # fixtures -------------------------------------------------------

    @pytest.fixture
    def blob_(self, request):
        return instance_mock(request, bytes)

    @pytest.fixture
    def construct_fixture(
            self, partname_, content_type_, blob_, package_, parse_xml_,
            init__, styles_elm_):
        return (
            partname_, content_type_, blob_, package_, parse_xml_, init__,
            styles_elm_
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
    def parse_xml_(self, request, styles_elm_):
        return function_mock(
            request, 'docx.parts.styles.parse_xml',
            return_value=styles_elm_
        )

    @pytest.fixture
    def package_(self, request):
        return instance_mock(request, Package)

    @pytest.fixture
    def partname_(self, request):
        return instance_mock(request, PackURI)

    @pytest.fixture
    def _Styles_(self, request, styles_):
        return class_mock(
            request, 'docx.parts.styles._Styles', return_value=styles_
        )

    @pytest.fixture
    def styles_(self, request):
        return instance_mock(request, _Styles)

    @pytest.fixture
    def styles_elm_(self, request):
        return instance_mock(request, CT_Styles)

    @pytest.fixture
    def styles_fixture(self, _Styles_, styles_elm_, styles_):
        styles_part = StylesPart(None, None, styles_elm_, None)
        return styles_part, _Styles_, styles_elm_, styles_

    @pytest.fixture
    def styles_part_(self, request):
        return instance_mock(request, StylesPart)

    @pytest.fixture
    def styles_part_load_(self, request):
        return method_mock(request, StylesPart, 'load')


class Describe_Styles(object):

    def it_knows_how_many_styles_it_contains(self, len_fixture):
        styles, style_count = len_fixture
        assert len(styles) == style_count

    # fixtures -------------------------------------------------------

    @pytest.fixture(params=[0, 1, 2, 3])
    def len_fixture(self, request):
        style_count = request.param
        styles_bldr = a_styles().with_nsdecls()
        for idx in range(style_count):
            styles_bldr.with_child(a_style())
        styles_elm = styles_bldr.element
        styles = _Styles(styles_elm)
        return styles, style_count
