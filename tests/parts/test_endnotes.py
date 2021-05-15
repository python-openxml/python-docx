# encoding: utf-8

"""Unit test suite for the docx.parts.endnotes module"""

from __future__ import absolute_import, division, print_function, unicode_literals

import pytest

from docx.opc.constants import CONTENT_TYPE as CT, RELATIONSHIP_TYPE as RT
from docx.opc.part import PartFactory
from docx.package import Package
from docx.parts.endnotes import EndnotesPart

from ..unitutil.mock import instance_mock, method_mock


class DescribeEndnotesPart(object):
    def it_is_used_by_loader_to_construct_endnotes_part(
        self, package_, EndnotesPart_load_, endnotes_part_
    ):
        partname = "endnotes.xml"
        content_type = CT.WML_ENDNOTES
        reltype = RT.ENDNOTES
        blob = "<w:endnotes/>"
        EndnotesPart_load_.return_value = endnotes_part_

        part = PartFactory(partname, content_type, reltype, blob, package_)

        EndnotesPart_load_.assert_called_once_with(
            partname, content_type, blob, package_
        )
        assert part is endnotes_part_

    # fixture components ---------------------------------------------

    @pytest.fixture
    def EndnotesPart_load_(self, request):
        return method_mock(request, EndnotesPart, "load", autospec=False)

    @pytest.fixture
    def endnotes_part_(self, request):
        return instance_mock(request, EndnotesPart)

    @pytest.fixture
    def package_(self, request):
        return instance_mock(request, Package)
