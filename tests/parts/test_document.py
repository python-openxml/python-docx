# encoding: utf-8

"""
Test suite for the docx.parts.document module
"""

from __future__ import absolute_import, print_function, unicode_literals

import pytest

from docx.image.image import Image
from docx.opc.constants import RELATIONSHIP_TYPE as RT
from docx.opc.coreprops import CoreProperties
from docx.package import Package
from docx.parts.document import DocumentPart
from docx.parts.image import ImagePart
from docx.parts.numbering import NumberingPart
from docx.parts.settings import SettingsPart
from docx.parts.styles import StylesPart
from docx.settings import Settings
from docx.styles.style import BaseStyle
from docx.styles.styles import Styles
from docx.text.paragraph import Paragraph

from ..oxml.parts.unitdata.document import a_body, a_document
from ..oxml.unitdata.text import a_p
from ..unitutil.file import snippet_text
from ..unitutil.mock import (
    instance_mock, class_mock, method_mock, property_mock
)


class DescribeDocumentPart(object):

    def it_can_save_the_package_to_a_file(self, save_fixture):
        document, file_ = save_fixture
        document.save(file_)
        document._package.save.assert_called_once_with(file_)

    def it_can_get_or_add_an_image(self, get_image_fixture):
        document_part, path, image_part_, rId_, image_ = get_image_fixture

        rId, image = document_part.get_or_add_image(path)

        image_parts = document_part._package.image_parts
        image_parts.get_or_add_image_part.assert_called_once_with(path)
        document_part.relate_to.assert_called_once_with(image_part_, RT.IMAGE)
        assert (rId, image) == (rId_, image_)

    def it_provides_access_to_the_document_settings(self, settings_fixture):
        document_part, settings_ = settings_fixture
        settings = document_part.settings
        assert settings is settings_

    def it_provides_access_to_the_document_styles(self, styles_fixture):
        document_part, styles_ = styles_fixture
        styles = document_part.styles
        assert styles is styles_

    def it_provides_access_to_its_core_properties(self, core_props_fixture):
        document_part, core_properties_ = core_props_fixture
        core_properties = document_part.core_properties
        assert core_properties is core_properties_

    def it_provides_access_to_the_inline_shapes_in_the_document(
            self, inline_shapes_fixture):
        document, InlineShapes_, body_elm = inline_shapes_fixture
        inline_shapes = document.inline_shapes
        InlineShapes_.assert_called_once_with(body_elm, document)
        assert inline_shapes is InlineShapes_.return_value

    def it_provides_access_to_the_numbering_part(self, nmprt_get_fixture):
        document_part, numbering_part_ = nmprt_get_fixture
        numbering_part = document_part.numbering_part
        document_part.part_related_by.assert_called_once_with(RT.NUMBERING)
        assert numbering_part is numbering_part_

    def it_creates_numbering_part_if_not_present(self, nmprt_create_fixture):
        document_part, NumberingPart_, numbering_part_ = nmprt_create_fixture
        numbering_part = document_part.numbering_part
        NumberingPart_.new.assert_called_once_with()
        document_part.relate_to.assert_called_once_with(
            numbering_part_, RT.NUMBERING
        )
        assert numbering_part is numbering_part_

    def it_knows_the_next_available_xml_id(self, next_id_fixture):
        document, expected_id = next_id_fixture
        assert document.next_id == expected_id

    def it_can_create_a_new_pic_inline(self, new_pic_fixture):
        document_part, path, width, height = new_pic_fixture[:4]
        image_, expected_xml = new_pic_fixture[4:]

        inline = document_part.new_pic_inline(path, width, height)

        document_part.get_or_add_image.assert_called_once_with(path)
        image_.scaled_dimensions.assert_called_once_with(width, height)
        assert inline.xml == expected_xml

    def it_can_get_a_style_by_id(self, get_style_fixture):
        document_part, style_id, style_type, style_ = get_style_fixture
        style = document_part.get_style(style_id, style_type)
        document_part.styles.get_by_id.assert_called_once_with(
            style_id, style_type
        )
        assert style is style_

    def it_can_get_the_id_of_a_style(self, get_style_id_fixture):
        document_part, style_or_name, style_type, style_id_ = (
            get_style_id_fixture
        )
        style_id = document_part.get_style_id(style_or_name, style_type)

        document_part.styles.get_style_id.assert_called_once_with(
            style_or_name, style_type
        )
        assert style_id is style_id_

    def it_provides_access_to_its_settings_part_to_help(
            self, settings_part_get_fixture):
        document_part, settings_part_ = settings_part_get_fixture
        settings_part = document_part._settings_part
        document_part.part_related_by.assert_called_once_with(RT.SETTINGS)
        assert settings_part is settings_part_

    def it_creates_default_settings_part_if_not_present_to_help(
            self, settings_part_create_fixture):
        document_part, SettingsPart_, settings_part_ = (
            settings_part_create_fixture
        )
        settings_part = document_part._settings_part

        SettingsPart_.default.assert_called_once_with(document_part.package)
        document_part.relate_to.assert_called_once_with(
            settings_part_, RT.SETTINGS
        )
        assert settings_part is settings_part_

    def it_provides_access_to_its_styles_part_to_help(
            self, styles_part_get_fixture):
        document_part, styles_part_ = styles_part_get_fixture
        styles_part = document_part._styles_part
        document_part.part_related_by.assert_called_once_with(RT.STYLES)
        assert styles_part is styles_part_

    def it_creates_default_styles_part_if_not_present_to_help(
            self, styles_part_create_fixture):
        document_part, StylesPart_, styles_part_ = styles_part_create_fixture
        styles_part = document_part._styles_part
        StylesPart_.default.assert_called_once_with(document_part.package)
        document_part.relate_to.assert_called_once_with(
            styles_part_, RT.STYLES
        )
        assert styles_part is styles_part_

    # fixtures -------------------------------------------------------

    @pytest.fixture
    def core_props_fixture(self, package_, core_properties_):
        document_part = DocumentPart(None, None, None, package_)
        package_.core_properties = core_properties_
        return document_part, core_properties_

    @pytest.fixture
    def get_image_fixture(self, package_, image_part_, image_, relate_to_):
        document_part = DocumentPart(None, None, None, package_)
        path, rId_ = 'foobar.png', 'rId42'

        package_.image_parts.get_or_add_image_part.return_value = image_part_
        relate_to_.return_value = rId_
        image_part_.image = image_

        return document_part, path, image_part_, rId_, image_

    @pytest.fixture
    def get_style_fixture(self, styles_prop_, style_):
        document_part = DocumentPart(None, None, None, None)
        style_id, style_type = 'Foobar', 1
        styles_prop_.return_value.get_by_id.return_value = style_
        return document_part, style_id, style_type, style_

    @pytest.fixture
    def get_style_id_fixture(self, styles_prop_):
        document_part = DocumentPart(None, None, None, None)
        style_or_name, style_type, style_id_ = 'Foo Bar', 1, 'FooBar'
        styles_prop_.return_value.get_style_id.return_value = style_id_
        return document_part, style_or_name, style_type, style_id_

    @pytest.fixture
    def inline_shapes_fixture(self, request, InlineShapes_):
        document_elm = (
            a_document().with_nsdecls().with_child(
                a_body())
        ).element
        body_elm = document_elm[0]
        document = DocumentPart(None, None, document_elm, None)
        return document, InlineShapes_, body_elm

    @pytest.fixture(params=[
        ((), 1), ((1,), 2), ((2,), 1), ((1, 2, 3), 4), ((1, 2, 4), 3),
        ((0, 0), 1), ((0, 0, 1, 3), 2), (('foo', 1, 2), 3), ((1, 'bar'), 2)
    ])
    def next_id_fixture(self, request):
        existing_ids, expected_id = request.param
        document_elm = a_document().with_nsdecls().element
        for n in existing_ids:
            p = a_p().with_nsdecls().element
            p.set('id', str(n))
            document_elm.append(p)
        document = DocumentPart(None, None, document_elm, None)
        return document, expected_id

    @pytest.fixture
    def new_pic_fixture(self, image_, get_or_add_image_, next_id_prop_):
        document_part = DocumentPart(None, None, None, None)
        path, width, height, rId = 'foo/bar.png', 111, 222, 'rId42'
        expected_xml = snippet_text('inline')

        get_or_add_image_.return_value = rId, image_
        image_.scaled_dimensions.return_value = 444, 888
        image_.filename = 'bar.png'
        next_id_prop_.return_value = 24

        return document_part, path, width, height, image_, expected_xml

    @pytest.fixture
    def nmprt_create_fixture(self, part_related_by_, relate_to_,
                             NumberingPart_, numbering_part_):
        document_part = DocumentPart(None, None, None, None)
        part_related_by_.side_effect = KeyError
        NumberingPart_.new.return_value = numbering_part_
        return document_part, NumberingPart_, numbering_part_

    @pytest.fixture
    def nmprt_get_fixture(self, part_related_by_, numbering_part_):
        document_part = DocumentPart(None, None, None, None)
        part_related_by_.return_value = numbering_part_
        return document_part, numbering_part_

    @pytest.fixture
    def save_fixture(self, package_):
        document_part = DocumentPart(None, None, None, package_)
        file_ = 'foobar.docx'
        return document_part, file_

    @pytest.fixture
    def settings_fixture(self, _settings_part_prop_, settings_part_,
                         settings_):
        document_part = DocumentPart(None, None, None, None)
        _settings_part_prop_.return_value = settings_part_
        settings_part_.settings = settings_
        return document_part, settings_

    @pytest.fixture
    def settings_part_create_fixture(
            self, package_, part_related_by_, SettingsPart_, settings_part_,
            relate_to_):
        document_part = DocumentPart(None, None, None, package_)
        part_related_by_.side_effect = KeyError
        SettingsPart_.default.return_value = settings_part_
        return document_part, SettingsPart_, settings_part_

    @pytest.fixture
    def settings_part_get_fixture(self, part_related_by_, settings_part_):
        document_part = DocumentPart(None, None, None, None)
        part_related_by_.return_value = settings_part_
        return document_part, settings_part_

    @pytest.fixture
    def styles_fixture(self, _styles_part_prop_, styles_part_, styles_):
        document_part = DocumentPart(None, None, None, None)
        _styles_part_prop_.return_value = styles_part_
        styles_part_.styles = styles_
        return document_part, styles_

    @pytest.fixture
    def styles_part_create_fixture(
            self, package_, part_related_by_, StylesPart_, styles_part_,
            relate_to_):
        document_part = DocumentPart(None, None, None, package_)
        part_related_by_.side_effect = KeyError
        StylesPart_.default.return_value = styles_part_
        return document_part, StylesPart_, styles_part_

    @pytest.fixture
    def styles_part_get_fixture(self, part_related_by_, styles_part_):
        document_part = DocumentPart(None, None, None, None)
        part_related_by_.return_value = styles_part_
        return document_part, styles_part_

    # fixture components ---------------------------------------------

    @pytest.fixture
    def core_properties_(self, request):
        return instance_mock(request, CoreProperties)

    @pytest.fixture
    def get_or_add_image_(self, request):
        return method_mock(request, DocumentPart, 'get_or_add_image')

    @pytest.fixture
    def image_(self, request):
        return instance_mock(request, Image)

    @pytest.fixture
    def image_part_(self, request):
        return instance_mock(request, ImagePart)

    @pytest.fixture
    def InlineShapes_(self, request):
        return class_mock(request, 'docx.parts.document.InlineShapes')

    @pytest.fixture
    def next_id_prop_(self, request):
        return property_mock(request, DocumentPart, 'next_id')

    @pytest.fixture
    def NumberingPart_(self, request):
        return class_mock(request, 'docx.parts.document.NumberingPart')

    @pytest.fixture
    def numbering_part_(self, request):
        return instance_mock(request, NumberingPart)

    @pytest.fixture
    def p_(self, request):
        return instance_mock(request, Paragraph)

    @pytest.fixture
    def package_(self, request):
        return instance_mock(request, Package)

    @pytest.fixture
    def part_related_by_(self, request):
        return method_mock(request, DocumentPart, 'part_related_by')

    @pytest.fixture
    def relate_to_(self, request):
        return method_mock(request, DocumentPart, 'relate_to')

    @pytest.fixture
    def SettingsPart_(self, request):
        return class_mock(request, 'docx.parts.document.SettingsPart')

    @pytest.fixture
    def settings_(self, request):
        return instance_mock(request, Settings)

    @pytest.fixture
    def settings_part_(self, request):
        return instance_mock(request, SettingsPart)

    @pytest.fixture
    def _settings_part_prop_(self, request):
        return property_mock(request, DocumentPart, '_settings_part')

    @pytest.fixture
    def style_(self, request):
        return instance_mock(request, BaseStyle)

    @pytest.fixture
    def styles_(self, request):
        return instance_mock(request, Styles)

    @pytest.fixture
    def StylesPart_(self, request):
        return class_mock(request, 'docx.parts.document.StylesPart')

    @pytest.fixture
    def styles_part_(self, request):
        return instance_mock(request, StylesPart)

    @pytest.fixture
    def styles_prop_(self, request, styles_):
        return property_mock(
            request, DocumentPart, 'styles', return_value=styles_
        )

    @pytest.fixture
    def _styles_part_prop_(self, request):
        return property_mock(request, DocumentPart, '_styles_part')
