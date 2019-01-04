# encoding: utf-8

"""Unit test suite for the docx.parts.story module"""

from __future__ import absolute_import, division, print_function, unicode_literals

import pytest

from docx.enum.style import WD_STYLE_TYPE
from docx.package import Package
from docx.parts.document import DocumentPart
from docx.parts.story import BaseStoryPart
from docx.styles.style import BaseStyle

from ..unitutil.mock import instance_mock, property_mock


class DescribeBaseStoryPart(object):

    def it_can_get_a_style_id_by_style_or_name_and_type(
        self, _document_part_prop_, document_part_, style_
    ):
        style_type = WD_STYLE_TYPE.PARAGRAPH
        _document_part_prop_.return_value = document_part_
        document_part_.get_style_id.return_value = "BodyText"
        story_part = BaseStoryPart(None, None, None, None)

        style_id = story_part.get_style_id(style_, style_type)

        document_part_.get_style_id.assert_called_once_with(style_, style_type)
        assert style_id == "BodyText"

    def it_knows_the_main_document_part_to_help(self, package_, document_part_):
        package_.main_document_part = document_part_
        story_part = BaseStoryPart(None, None, None, package_)

        document_part = story_part._document_part

        assert document_part is document_part_

    # fixture components ---------------------------------------------

    @pytest.fixture
    def document_part_(self, request):
        return instance_mock(request, DocumentPart)

    @pytest.fixture
    def _document_part_prop_(self, request):
        return property_mock(request, BaseStoryPart, "_document_part")

    @pytest.fixture
    def package_(self, request):
        return instance_mock(request, Package)

    @pytest.fixture
    def style_(self, request):
        return instance_mock(request, BaseStyle)
