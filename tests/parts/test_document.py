"""Unit test suite for the docx.parts.document module."""

import pytest

from docx.enum.style import WD_STYLE_TYPE
from docx.opc.constants import RELATIONSHIP_TYPE as RT
from docx.opc.coreprops import CoreProperties
from docx.package import Package
from docx.parts.document import DocumentPart
from docx.parts.hdrftr import FooterPart, HeaderPart
from docx.parts.numbering import NumberingPart
from docx.parts.settings import SettingsPart
from docx.parts.styles import StylesPart
from docx.settings import Settings
from docx.styles.style import BaseStyle
from docx.styles.styles import Styles

from ..oxml.parts.unitdata.document import a_body, a_document
from ..unitutil.mock import class_mock, instance_mock, method_mock, property_mock


class DescribeDocumentPart:
    def it_can_add_a_footer_part(self, package_, FooterPart_, footer_part_, relate_to_):
        FooterPart_.new.return_value = footer_part_
        relate_to_.return_value = "rId12"
        document_part = DocumentPart(None, None, None, package_)

        footer_part, rId = document_part.add_footer_part()

        FooterPart_.new.assert_called_once_with(package_)
        relate_to_.assert_called_once_with(document_part, footer_part_, RT.FOOTER)
        assert footer_part is footer_part_
        assert rId == "rId12"

    def it_can_add_a_header_part(self, package_, HeaderPart_, header_part_, relate_to_):
        HeaderPart_.new.return_value = header_part_
        relate_to_.return_value = "rId7"
        document_part = DocumentPart(None, None, None, package_)

        header_part, rId = document_part.add_header_part()

        HeaderPart_.new.assert_called_once_with(package_)
        relate_to_.assert_called_once_with(document_part, header_part_, RT.HEADER)
        assert header_part is header_part_
        assert rId == "rId7"

    def it_can_drop_a_specified_header_part(self, drop_rel_):
        document_part = DocumentPart(None, None, None, None)

        document_part.drop_header_part("rId42")

        drop_rel_.assert_called_once_with(document_part, "rId42")

    def it_provides_access_to_a_footer_part_by_rId(
        self, related_parts_prop_, related_parts_, footer_part_
    ):
        related_parts_prop_.return_value = related_parts_
        related_parts_.__getitem__.return_value = footer_part_
        document_part = DocumentPart(None, None, None, None)

        footer_part = document_part.footer_part("rId9")

        related_parts_.__getitem__.assert_called_once_with("rId9")
        assert footer_part is footer_part_

    def it_provides_access_to_a_header_part_by_rId(
        self, related_parts_prop_, related_parts_, header_part_
    ):
        related_parts_prop_.return_value = related_parts_
        related_parts_.__getitem__.return_value = header_part_
        document_part = DocumentPart(None, None, None, None)

        header_part = document_part.header_part("rId11")

        related_parts_.__getitem__.assert_called_once_with("rId11")
        assert header_part is header_part_

    def it_can_save_the_package_to_a_file(self, save_fixture):
        document, file_ = save_fixture
        document.save(file_)
        document._package.save.assert_called_once_with(file_)

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
        self, inline_shapes_fixture
    ):
        document, InlineShapes_, body_elm = inline_shapes_fixture
        inline_shapes = document.inline_shapes
        InlineShapes_.assert_called_once_with(body_elm, document)
        assert inline_shapes is InlineShapes_.return_value

    def it_provides_access_to_the_numbering_part(
        self, part_related_by_, numbering_part_
    ):
        part_related_by_.return_value = numbering_part_
        document_part = DocumentPart(None, None, None, None)

        numbering_part = document_part.numbering_part

        part_related_by_.assert_called_once_with(document_part, RT.NUMBERING)
        assert numbering_part is numbering_part_

    def and_it_creates_a_numbering_part_if_not_present(
        self, part_related_by_, relate_to_, NumberingPart_, numbering_part_
    ):
        part_related_by_.side_effect = KeyError
        NumberingPart_.new.return_value = numbering_part_
        document_part = DocumentPart(None, None, None, None)

        numbering_part = document_part.numbering_part

        NumberingPart_.new.assert_called_once_with()
        relate_to_.assert_called_once_with(document_part, numbering_part_, RT.NUMBERING)
        assert numbering_part is numbering_part_

    def it_can_get_a_style_by_id(self, styles_prop_, styles_, style_):
        styles_prop_.return_value = styles_
        styles_.get_by_id.return_value = style_
        document_part = DocumentPart(None, None, None, None)

        style = document_part.get_style("BodyText", WD_STYLE_TYPE.PARAGRAPH)

        styles_.get_by_id.assert_called_once_with("BodyText", WD_STYLE_TYPE.PARAGRAPH)
        assert style is style_

    def it_can_get_the_id_of_a_style(self, style_, styles_prop_, styles_):
        styles_prop_.return_value = styles_
        styles_.get_style_id.return_value = "BodyCharacter"
        document_part = DocumentPart(None, None, None, None)

        style_id = document_part.get_style_id(style_, WD_STYLE_TYPE.CHARACTER)

        styles_.get_style_id.assert_called_once_with(style_, WD_STYLE_TYPE.CHARACTER)
        assert style_id == "BodyCharacter"

    def it_provides_access_to_its_settings_part_to_help(
        self, part_related_by_, settings_part_
    ):
        part_related_by_.return_value = settings_part_
        document_part = DocumentPart(None, None, None, None)

        settings_part = document_part._settings_part

        part_related_by_.assert_called_once_with(document_part, RT.SETTINGS)
        assert settings_part is settings_part_

    def and_it_creates_a_default_settings_part_if_not_present(
        self, package_, part_related_by_, SettingsPart_, settings_part_, relate_to_
    ):
        part_related_by_.side_effect = KeyError
        SettingsPart_.default.return_value = settings_part_
        document_part = DocumentPart(None, None, None, package_)

        settings_part = document_part._settings_part

        SettingsPart_.default.assert_called_once_with(package_)
        relate_to_.assert_called_once_with(document_part, settings_part_, RT.SETTINGS)
        assert settings_part is settings_part_

    def it_provides_access_to_its_styles_part_to_help(
        self, part_related_by_, styles_part_
    ):
        part_related_by_.return_value = styles_part_
        document_part = DocumentPart(None, None, None, None)

        styles_part = document_part._styles_part

        part_related_by_.assert_called_once_with(document_part, RT.STYLES)
        assert styles_part is styles_part_

    def and_it_creates_a_default_styles_part_if_not_present(
        self, package_, part_related_by_, StylesPart_, styles_part_, relate_to_
    ):
        part_related_by_.side_effect = KeyError
        StylesPart_.default.return_value = styles_part_
        document_part = DocumentPart(None, None, None, package_)

        styles_part = document_part._styles_part

        StylesPart_.default.assert_called_once_with(package_)
        relate_to_.assert_called_once_with(document_part, styles_part_, RT.STYLES)
        assert styles_part is styles_part_

    # fixtures -------------------------------------------------------

    @pytest.fixture
    def core_props_fixture(self, package_, core_properties_):
        document_part = DocumentPart(None, None, None, package_)
        package_.core_properties = core_properties_
        return document_part, core_properties_

    @pytest.fixture
    def inline_shapes_fixture(self, request, InlineShapes_):
        document_elm = (a_document().with_nsdecls().with_child(a_body())).element
        body_elm = document_elm[0]
        document = DocumentPart(None, None, document_elm, None)
        return document, InlineShapes_, body_elm

    @pytest.fixture
    def save_fixture(self, package_):
        document_part = DocumentPart(None, None, None, package_)
        file_ = "foobar.docx"
        return document_part, file_

    @pytest.fixture
    def settings_fixture(self, _settings_part_prop_, settings_part_, settings_):
        document_part = DocumentPart(None, None, None, None)
        _settings_part_prop_.return_value = settings_part_
        settings_part_.settings = settings_
        return document_part, settings_

    @pytest.fixture
    def styles_fixture(self, _styles_part_prop_, styles_part_, styles_):
        document_part = DocumentPart(None, None, None, None)
        _styles_part_prop_.return_value = styles_part_
        styles_part_.styles = styles_
        return document_part, styles_

    # fixture components ---------------------------------------------

    @pytest.fixture
    def core_properties_(self, request):
        return instance_mock(request, CoreProperties)

    @pytest.fixture
    def drop_rel_(self, request):
        return method_mock(request, DocumentPart, "drop_rel", autospec=True)

    @pytest.fixture
    def FooterPart_(self, request):
        return class_mock(request, "docx.parts.document.FooterPart")

    @pytest.fixture
    def footer_part_(self, request):
        return instance_mock(request, FooterPart)

    @pytest.fixture
    def HeaderPart_(self, request):
        return class_mock(request, "docx.parts.document.HeaderPart")

    @pytest.fixture
    def header_part_(self, request):
        return instance_mock(request, HeaderPart)

    @pytest.fixture
    def InlineShapes_(self, request):
        return class_mock(request, "docx.parts.document.InlineShapes")

    @pytest.fixture
    def NumberingPart_(self, request):
        return class_mock(request, "docx.parts.document.NumberingPart")

    @pytest.fixture
    def numbering_part_(self, request):
        return instance_mock(request, NumberingPart)

    @pytest.fixture
    def package_(self, request):
        return instance_mock(request, Package)

    @pytest.fixture
    def part_related_by_(self, request):
        return method_mock(request, DocumentPart, "part_related_by")

    @pytest.fixture
    def relate_to_(self, request):
        return method_mock(request, DocumentPart, "relate_to")

    @pytest.fixture
    def related_parts_(self, request):
        return instance_mock(request, dict)

    @pytest.fixture
    def related_parts_prop_(self, request):
        return property_mock(request, DocumentPart, "related_parts")

    @pytest.fixture
    def SettingsPart_(self, request):
        return class_mock(request, "docx.parts.document.SettingsPart")

    @pytest.fixture
    def settings_(self, request):
        return instance_mock(request, Settings)

    @pytest.fixture
    def settings_part_(self, request):
        return instance_mock(request, SettingsPart)

    @pytest.fixture
    def _settings_part_prop_(self, request):
        return property_mock(request, DocumentPart, "_settings_part")

    @pytest.fixture
    def style_(self, request):
        return instance_mock(request, BaseStyle)

    @pytest.fixture
    def styles_(self, request):
        return instance_mock(request, Styles)

    @pytest.fixture
    def StylesPart_(self, request):
        return class_mock(request, "docx.parts.document.StylesPart")

    @pytest.fixture
    def styles_part_(self, request):
        return instance_mock(request, StylesPart)

    @pytest.fixture
    def styles_prop_(self, request):
        return property_mock(request, DocumentPart, "styles")

    @pytest.fixture
    def _styles_part_prop_(self, request):
        return property_mock(request, DocumentPart, "_styles_part")
