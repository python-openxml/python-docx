# encoding: utf-8

"""
Test suite for the docx.parts.numbering module
"""

from __future__ import absolute_import, print_function, unicode_literals

import pytest

from docx.oxml.numbering import CT_Numbering
from docx.parts.numbering import NumberingPart, _NumberingDefinitions

from ..oxml.unitdata.numbering import a_num, a_numbering
from ..unitutil.mock import class_mock, instance_mock


class DescribeNumberingPart(object):

    def it_provides_access_to_the_numbering_definitions(
            self, num_defs_fixture):
        (numbering_part, _NumberingDefinitions_, numbering_elm_,
         numbering_definitions_) = num_defs_fixture
        numbering_definitions = numbering_part.numbering_definitions
        _NumberingDefinitions_.assert_called_once_with(numbering_elm_)
        assert numbering_definitions is numbering_definitions_

    # fixtures -------------------------------------------------------

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
