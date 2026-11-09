# pyright: reportPrivateUsage=false

"""Unit test suite for the docx.parts.document module."""

import pytest

from docx.comments import Comments
from docx.enum.style import WD_STYLE_TYPE
from docx.opc.constants import CONTENT_TYPE as CT
from docx.opc.constants import RELATIONSHIP_TYPE as RT
from docx.opc.coreprops import CoreProperties
from docx.opc.packuri import PackURI
from docx.package import Package
from docx.parts.comments import CommentsPart
from docx.parts.document import DocumentPart
from docx.parts.hdrftr import FooterPart, HeaderPart
from docx.parts.numbering import NumberingPart
from docx.parts.settings import SettingsPart
from docx.parts.styles import StylesPart
from docx.settings import Settings
from docx.styles.style import BaseStyle
from docx.styles.styles import Styles

from ..unitutil.cxml import element
from ..unitutil.mock import (
    FixtureRequest,
    Mock,
    class_mock,
    instance_mock,
    method_mock,
    property_mock,
)


class DescribeDocumentPart:
    def it_can_add_a_footer_part(
        self, package_: Mock, FooterPart_: Mock, footer_part_: Mock, relate_to_: Mock
    ):
        FooterPart_.new.return_value = footer_part_
        relate_to_.return_value = "rId12"
        document_part = DocumentPart(
            PackURI("/word/document.xml"), CT.WML_DOCUMENT, element("w:document"), package_
        )

        footer_part, rId = document_part.add_footer_part()

        FooterPart_.new.assert_called_once_with(package_)
        relate_to_.assert_called_once_with(document_part, footer_part_, RT.FOOTER)
        assert footer_part is footer_part_
        assert rId == "rId12"

    def it_can_add_a_header_part(
        self, package_: Mock, HeaderPart_: Mock, header_part_: Mock, relate_to_: Mock
    ):
        HeaderPart_.new.return_value = header_part_
        relate_to_.return_value = "rId7"
        document_part = DocumentPart(
            PackURI("/word/document.xml"), CT.WML_DOCUMENT, element("w:document"), package_
        )

        header_part, rId = document_part.add_header_part()

        HeaderPart_.new.assert_called_once_with(package_)
        relate_to_.assert_called_once_with(document_part, header_part_, RT.HEADER)
        assert header_part is header_part_
        assert rId == "rId7"

    def it_can_drop_a_specified_header_part(self, drop_rel_: Mock, package_: Mock):
        document_part = DocumentPart(
            PackURI("/word/document.xml"), CT.WML_DOCUMENT, element("w:document"), package_
        )

        document_part.drop_header_part("rId42")

        drop_rel_.assert_called_once_with(document_part, "rId42")

    def it_provides_access_to_a_footer_part_by_rId(
        self, related_parts_prop_: Mock, related_parts_: Mock, footer_part_: Mock, package_: Mock
    ):
        related_parts_prop_.return_value = related_parts_
        related_parts_.__getitem__.return_value = footer_part_
        document_part = DocumentPart(
            PackURI("/word/document.xml"), CT.WML_DOCUMENT, element("w:document"), package_
        )

        footer_part = document_part.footer_part("rId9")

        related_parts_.__getitem__.assert_called_once_with("rId9")
        assert footer_part is footer_part_

    def it_provides_access_to_a_header_part_by_rId(
        self, related_parts_prop_: Mock, related_parts_: Mock, header_part_: Mock, package_: Mock
    ):
        related_parts_prop_.return_value = related_parts_
        related_parts_.__getitem__.return_value = header_part_
        document_part = DocumentPart(
            PackURI("/word/document.xml"), CT.WML_DOCUMENT, element("w:document"), package_
        )

        header_part = document_part.header_part("rId11")

        related_parts_.__getitem__.assert_called_once_with("rId11")
        assert header_part is header_part_

    def it_can_save_the_package_to_a_file(self, package_: Mock):
        document_part = DocumentPart(
            PackURI("/word/document.xml"), CT.WML_DOCUMENT, element("w:document"), package_
        )

        document_part.save("foobar.docx")

        package_.save.assert_called_once_with("foobar.docx")

    def it_provides_access_to_the_comments_added_to_the_document(
        self, _comments_part_prop_: Mock, comments_part_: Mock, comments_: Mock, package_: Mock
    ):
        comments_part_.comments = comments_
        _comments_part_prop_.return_value = comments_part_
        document_part = DocumentPart(
            PackURI("/word/document.xml"), CT.WML_DOCUMENT, element("w:document"), package_
        )

        assert document_part.comments is comments_

    def it_provides_access_to_the_document_settings(
        self, _settings_part_prop_: Mock, settings_part_: Mock, settings_: Mock, package_: Mock
    ):
        settings_part_.settings = settings_
        _settings_part_prop_.return_value = settings_part_
        document_part = DocumentPart(
            PackURI("/word/document.xml"), CT.WML_DOCUMENT, element("w:document"), package_
        )

        assert document_part.settings is settings_

    def it_provides_access_to_the_document_styles(
        self, _styles_part_prop_: Mock, styles_part_: Mock, styles_: Mock, package_: Mock
    ):
        styles_part_.styles = styles_
        _styles_part_prop_.return_value = styles_part_
        document_part = DocumentPart(
            PackURI("/word/document.xml"), CT.WML_DOCUMENT, element("w:document"), package_
        )

        assert document_part.styles is styles_

    def it_provides_access_to_its_core_properties(self, package_: Mock, core_properties_: Mock):
        document_part = DocumentPart(
            PackURI("/word/document.xml"), CT.WML_DOCUMENT, element("w:document"), package_
        )
        package_.core_properties = core_properties_

        assert document_part.core_properties is core_properties_

    def it_provides_access_to_the_inline_shapes_in_the_document(
        self, InlineShapes_: Mock, package_: Mock
    ):
        document_elm = element("w:document/w:body")
        body_elm = document_elm[0]
        document_part = DocumentPart(
            PackURI("/word/document.xml"), CT.WML_DOCUMENT, document_elm, package_
        )

        inline_shapes = document_part.inline_shapes

        InlineShapes_.assert_called_once_with(body_elm, document_part)
        assert inline_shapes is InlineShapes_.return_value

    def it_provides_access_to_the_numbering_part(
        self, part_related_by_: Mock, numbering_part_: Mock, package_: Mock
    ):
        part_related_by_.return_value = numbering_part_
        document_part = DocumentPart(
            PackURI("/word/document.xml"), CT.WML_DOCUMENT, element("w:document"), package_
        )

        numbering_part = document_part.numbering_part

        part_related_by_.assert_called_once_with(document_part, RT.NUMBERING)
        assert numbering_part is numbering_part_

    def and_it_creates_a_numbering_part_if_not_present(
        self,
        part_related_by_: Mock,
        relate_to_: Mock,
        NumberingPart_: Mock,
        numbering_part_: Mock,
        package_: Mock,
    ):
        part_related_by_.side_effect = KeyError
        NumberingPart_.new.return_value = numbering_part_
        document_part = DocumentPart(
            PackURI("/word/document.xml"), CT.WML_DOCUMENT, element("w:document"), package_
        )

        numbering_part = document_part.numbering_part

        NumberingPart_.new.assert_called_once_with()
        relate_to_.assert_called_once_with(document_part, numbering_part_, RT.NUMBERING)
        assert numbering_part is numbering_part_

    def it_can_get_a_style_by_id(
        self, styles_prop_: Mock, styles_: Mock, style_: Mock, package_: Mock
    ):
        styles_prop_.return_value = styles_
        styles_.get_by_id.return_value = style_
        document_part = DocumentPart(
            PackURI("/word/document.xml"), CT.WML_DOCUMENT, element("w:document"), package_
        )

        style = document_part.get_style("BodyText", WD_STYLE_TYPE.PARAGRAPH)

        styles_.get_by_id.assert_called_once_with("BodyText", WD_STYLE_TYPE.PARAGRAPH)
        assert style is style_

    def it_can_get_the_id_of_a_style(
        self, style_: Mock, styles_prop_: Mock, styles_: Mock, package_: Mock
    ):
        styles_prop_.return_value = styles_
        styles_.get_style_id.return_value = "BodyCharacter"
        document_part = DocumentPart(
            PackURI("/word/document.xml"), CT.WML_DOCUMENT, element("w:document"), package_
        )

        style_id = document_part.get_style_id(style_, WD_STYLE_TYPE.CHARACTER)

        styles_.get_style_id.assert_called_once_with(style_, WD_STYLE_TYPE.CHARACTER)
        assert style_id == "BodyCharacter"

    def it_provides_access_to_its_comments_part_to_help(
        self, package_: Mock, part_related_by_: Mock, comments_part_: Mock
    ):
        part_related_by_.return_value = comments_part_
        document_part = DocumentPart(
            PackURI("/word/document.xml"), CT.WML_DOCUMENT, element("w:document"), package_
        )

        comments_part = document_part._comments_part

        part_related_by_.assert_called_once_with(document_part, RT.COMMENTS)
        assert comments_part is comments_part_

    def and_it_creates_a_default_comments_part_if_not_present(
        self,
        package_: Mock,
        part_related_by_: Mock,
        CommentsPart_: Mock,
        comments_part_: Mock,
        relate_to_: Mock,
    ):
        part_related_by_.side_effect = KeyError
        CommentsPart_.default.return_value = comments_part_
        document_part = DocumentPart(
            PackURI("/word/document.xml"), CT.WML_DOCUMENT, element("w:document"), package_
        )

        comments_part = document_part._comments_part

        CommentsPart_.default.assert_called_once_with(package_)
        relate_to_.assert_called_once_with(document_part, comments_part_, RT.COMMENTS)
        assert comments_part is comments_part_

    def it_provides_access_to_its_settings_part_to_help(
        self, part_related_by_: Mock, settings_part_: Mock, package_: Mock
    ):
        part_related_by_.return_value = settings_part_
        document_part = DocumentPart(
            PackURI("/word/document.xml"), CT.WML_DOCUMENT, element("w:document"), package_
        )

        settings_part = document_part._settings_part

        part_related_by_.assert_called_once_with(document_part, RT.SETTINGS)
        assert settings_part is settings_part_

    def and_it_creates_a_default_settings_part_if_not_present(
        self,
        package_: Mock,
        part_related_by_: Mock,
        SettingsPart_: Mock,
        settings_part_: Mock,
        relate_to_: Mock,
    ):
        part_related_by_.side_effect = KeyError
        SettingsPart_.default.return_value = settings_part_
        document_part = DocumentPart(
            PackURI("/word/document.xml"), CT.WML_DOCUMENT, element("w:document"), package_
        )

        settings_part = document_part._settings_part

        SettingsPart_.default.assert_called_once_with(package_)
        relate_to_.assert_called_once_with(document_part, settings_part_, RT.SETTINGS)
        assert settings_part is settings_part_

    def it_provides_access_to_its_styles_part_to_help(
        self, part_related_by_: Mock, styles_part_: Mock, package_: Mock
    ):
        part_related_by_.return_value = styles_part_
        document_part = DocumentPart(
            PackURI("/word/document.xml"), CT.WML_DOCUMENT, element("w:document"), package_
        )

        styles_part = document_part._styles_part

        part_related_by_.assert_called_once_with(document_part, RT.STYLES)
        assert styles_part is styles_part_

    def and_it_creates_a_default_styles_part_if_not_present(
        self,
        package_: Mock,
        part_related_by_: Mock,
        StylesPart_: Mock,
        styles_part_: Mock,
        relate_to_: Mock,
    ):
        part_related_by_.side_effect = KeyError
        StylesPart_.default.return_value = styles_part_
        document_part = DocumentPart(
            PackURI("/word/document.xml"), CT.WML_DOCUMENT, element("w:document"), package_
        )

        styles_part = document_part._styles_part

        StylesPart_.default.assert_called_once_with(package_)
        relate_to_.assert_called_once_with(document_part, styles_part_, RT.STYLES)
        assert styles_part is styles_part_

    # -- fixtures --------------------------------------------------------------------------------

    @pytest.fixture
    def comments_(self, request: FixtureRequest) -> Mock:
        return instance_mock(request, Comments)

    @pytest.fixture
    def CommentsPart_(self, request: FixtureRequest) -> Mock:
        return class_mock(request, "docx.parts.document.CommentsPart")

    @pytest.fixture
    def comments_part_(self, request: FixtureRequest) -> Mock:
        return instance_mock(request, CommentsPart)

    @pytest.fixture
    def _comments_part_prop_(self, request: FixtureRequest) -> Mock:
        return property_mock(request, DocumentPart, "_comments_part")

    @pytest.fixture
    def core_properties_(self, request: FixtureRequest):
        return instance_mock(request, CoreProperties)

    @pytest.fixture
    def drop_rel_(self, request: FixtureRequest):
        return method_mock(request, DocumentPart, "drop_rel", autospec=True)

    @pytest.fixture
    def FooterPart_(self, request: FixtureRequest):
        return class_mock(request, "docx.parts.document.FooterPart")

    @pytest.fixture
    def footer_part_(self, request: FixtureRequest):
        return instance_mock(request, FooterPart)

    @pytest.fixture
    def HeaderPart_(self, request: FixtureRequest):
        return class_mock(request, "docx.parts.document.HeaderPart")

    @pytest.fixture
    def header_part_(self, request: FixtureRequest):
        return instance_mock(request, HeaderPart)

    @pytest.fixture
    def InlineShapes_(self, request: FixtureRequest):
        return class_mock(request, "docx.parts.document.InlineShapes")

    @pytest.fixture
    def NumberingPart_(self, request: FixtureRequest):
        return class_mock(request, "docx.parts.document.NumberingPart")

    @pytest.fixture
    def numbering_part_(self, request: FixtureRequest):
        return instance_mock(request, NumberingPart)

    @pytest.fixture
    def package_(self, request: FixtureRequest):
        return instance_mock(request, Package)

    @pytest.fixture
    def part_related_by_(self, request: FixtureRequest):
        return method_mock(request, DocumentPart, "part_related_by")

    @pytest.fixture
    def relate_to_(self, request: FixtureRequest):
        return method_mock(request, DocumentPart, "relate_to")

    @pytest.fixture
    def related_parts_(self, request: FixtureRequest):
        return instance_mock(request, dict)

    @pytest.fixture
    def related_parts_prop_(self, request: FixtureRequest):
        return property_mock(request, DocumentPart, "related_parts")

    @pytest.fixture
    def SettingsPart_(self, request: FixtureRequest):
        return class_mock(request, "docx.parts.document.SettingsPart")

    @pytest.fixture
    def settings_(self, request: FixtureRequest):
        return instance_mock(request, Settings)

    @pytest.fixture
    def settings_part_(self, request: FixtureRequest):
        return instance_mock(request, SettingsPart)

    @pytest.fixture
    def _settings_part_prop_(self, request: FixtureRequest):
        return property_mock(request, DocumentPart, "_settings_part")

    @pytest.fixture
    def style_(self, request: FixtureRequest):
        return instance_mock(request, BaseStyle)

    @pytest.fixture
    def styles_(self, request: FixtureRequest):
        return instance_mock(request, Styles)

    @pytest.fixture
    def StylesPart_(self, request: FixtureRequest):
        return class_mock(request, "docx.parts.document.StylesPart")

    @pytest.fixture
    def styles_part_(self, request: FixtureRequest):
        return instance_mock(request, StylesPart)

    @pytest.fixture
    def styles_prop_(self, request: FixtureRequest):
        return property_mock(request, DocumentPart, "styles")

    @pytest.fixture
    def _styles_part_prop_(self, request: FixtureRequest):
        return property_mock(request, DocumentPart, "_styles_part")
