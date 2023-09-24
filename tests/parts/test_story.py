# encoding: utf-8

"""Unit test suite for the docx.parts.story module"""

from __future__ import absolute_import, division, print_function, unicode_literals

import pytest

from docx.enum.style import WD_STYLE_TYPE
from docx.image.image import Image
from docx.opc.constants import RELATIONSHIP_TYPE as RT
from docx.package import Package
from docx.parts.document import DocumentPart
from docx.parts.image import ImagePart
from docx.parts.story import BaseStoryPart
from docx.styles.style import BaseStyle

from ..unitutil.cxml import element
from ..unitutil.file import snippet_text
from ..unitutil.mock import instance_mock, method_mock, property_mock


class DescribeBaseStoryPart(object):
    def it_can_get_or_add_an_image(self, package_, image_part_, image_, relate_to_):
        package_.get_or_add_image_part.return_value = image_part_
        relate_to_.return_value = "rId42"
        image_part_.image = image_
        story_part = BaseStoryPart(None, None, None, package_)

        rId, image = story_part.get_or_add_image("image.png")

        package_.get_or_add_image_part.assert_called_once_with("image.png")
        relate_to_.assert_called_once_with(story_part, image_part_, RT.IMAGE)
        assert rId == "rId42"
        assert image is image_

    def it_can_get_a_style_by_id_and_type(
        self, _document_part_prop_, document_part_, style_
    ):
        style_id = "BodyText"
        style_type = WD_STYLE_TYPE.PARAGRAPH
        _document_part_prop_.return_value = document_part_
        document_part_.get_style.return_value = style_
        story_part = BaseStoryPart(None, None, None, None)

        style = story_part.get_style(style_id, style_type)

        document_part_.get_style.assert_called_once_with(style_id, style_type)
        assert style is style_

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

    def it_can_create_a_new_pic_inline(self, get_or_add_image_, image_, next_id_prop_):
        get_or_add_image_.return_value = "rId42", image_
        image_.scaled_dimensions.return_value = 444, 888
        image_.filename = "bar.png"
        next_id_prop_.return_value = 24
        expected_xml = snippet_text("inline")
        story_part = BaseStoryPart(None, None, None, None)

        inline = story_part.new_pic_inline("foo/bar.png", width=100, height=200)

        get_or_add_image_.assert_called_once_with(story_part, "foo/bar.png")
        image_.scaled_dimensions.assert_called_once_with(100, 200)
        assert inline.xml == expected_xml

    def it_knows_the_next_available_xml_id(self, next_id_fixture):
        story_element, expected_value = next_id_fixture
        story_part = BaseStoryPart(None, None, story_element, None)

        next_id = story_part.next_id

        assert next_id == expected_value

    def it_knows_the_main_document_part_to_help(self, package_, document_part_):
        package_.main_document_part = document_part_
        story_part = BaseStoryPart(None, None, None, package_)

        document_part = story_part._document_part

        assert document_part is document_part_

    # fixtures -------------------------------------------------------

    @pytest.fixture(
        params=[
            (("w:document"), 1),
            (("w:document/w:p{id=1}"), 2),
            (("w:document/w:p{id=2}"), 3),
            (("w:hdr/(w:p{id=1},w:p{id=2},w:p{id=3})"), 4),
            (("w:hdr/(w:p{id=1},w:p{id=2},w:p{id=4})"), 5),
            (("w:hdr/(w:p{id=0},w:p{id=0})"), 1),
            (("w:ftr/(w:p{id=0},w:p{id=0},w:p{id=1},w:p{id=3})"), 4),
            (("w:ftr/(w:p{id=foo},w:p{id=1},w:p{id=2})"), 3),
            (("w:ftr/(w:p{id=1},w:p{id=bar})"), 2),
        ]
    )
    def next_id_fixture(self, request):
        story_cxml, expected_value = request.param
        story_element = element(story_cxml)
        return story_element, expected_value

    # fixture components ---------------------------------------------

    @pytest.fixture
    def document_part_(self, request):
        return instance_mock(request, DocumentPart)

    @pytest.fixture
    def _document_part_prop_(self, request):
        return property_mock(request, BaseStoryPart, "_document_part")

    @pytest.fixture
    def get_or_add_image_(self, request):
        return method_mock(request, BaseStoryPart, "get_or_add_image")

    @pytest.fixture
    def image_(self, request):
        return instance_mock(request, Image)

    @pytest.fixture
    def image_part_(self, request):
        return instance_mock(request, ImagePart)

    @pytest.fixture
    def next_id_prop_(self, request):
        return property_mock(request, BaseStoryPart, "next_id")

    @pytest.fixture
    def package_(self, request):
        return instance_mock(request, Package)

    @pytest.fixture
    def relate_to_(self, request):
        return method_mock(request, BaseStoryPart, "relate_to")

    @pytest.fixture
    def style_(self, request):
        return instance_mock(request, BaseStyle)
