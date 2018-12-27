# encoding: utf-8

"""Unit test suite for the docx.parts.footnotes module"""

from __future__ import absolute_import, division, print_function, unicode_literals

import pytest

from docx.opc.constants import CONTENT_TYPE as CT, RELATIONSHIP_TYPE as RT
from docx.opc.part import PartFactory
from docx.package import Package
from docx.parts.footnotes import FootnotesPart

from ..unitutil.mock import instance_mock, method_mock


class DescribeFootnotesPart(object):
    def it_is_used_by_loader_to_construct_footnotes_part(
        self, package_, FootnotesPart_load_, footnotes_part_
    ):
        partname = "footnotes.xml"
        content_type = CT.WML_FOOTNOTES
        reltype = RT.FOOTNOTES
        blob = "<w:footnotes/>"
        FootnotesPart_load_.return_value = footnotes_part_

        part = PartFactory(partname, content_type, reltype, blob, package_)

        FootnotesPart_load_.assert_called_once_with(
            partname, content_type, blob, package_
        )
        assert part is footnotes_part_

    # fixture components ---------------------------------------------

    @pytest.fixture
    def FootnotesPart_load_(self, request):
        return method_mock(request, FootnotesPart, "load", autospec=False)

    @pytest.fixture
    def footnotes_part_(self, request):
        return instance_mock(request, FootnotesPart)

    @pytest.fixture
    def package_(self, request):
        return instance_mock(request, Package)
