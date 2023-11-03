# pyright: reportPrivateUsage=false
# pyright: reportUnknownMemberType=false

"""Unit test suite for the docx.document module."""

from __future__ import annotations

from typing import cast

import pytest

from docx.document import Document, _Body
from docx.enum.section import WD_SECTION
from docx.enum.text import WD_BREAK
from docx.opc.coreprops import CoreProperties
from docx.oxml.document import CT_Document
from docx.parts.document import DocumentPart
from docx.section import Section, Sections
from docx.settings import Settings
from docx.shape import InlineShape, InlineShapes
from docx.shared import Length
from docx.styles.styles import Styles
from docx.table import Table
from docx.text.paragraph import Paragraph
from docx.text.run import Run

from .unitutil.cxml import element, xml
from .unitutil.mock import Mock, class_mock, instance_mock, method_mock, property_mock


class DescribeDocument:
    """Unit-test suite for `docx.Document`."""

    def it_can_add_a_heading(self, add_heading_fixture, add_paragraph_, paragraph_):
        level, style = add_heading_fixture
        add_paragraph_.return_value = paragraph_
        document = Document(None, None)

        paragraph = document.add_heading("Spam vs. Bacon", level)

        add_paragraph_.assert_called_once_with(document, "Spam vs. Bacon", style)
        assert paragraph is paragraph_

    def it_raises_on_heading_level_out_of_range(self):
        document = Document(None, None)
        with pytest.raises(ValueError, match="level must be in range 0-9, got -1"):
            document.add_heading(level=-1)
        with pytest.raises(ValueError, match="level must be in range 0-9, got 10"):
            document.add_heading(level=10)

    def it_can_add_a_page_break(self, add_paragraph_, paragraph_, run_):
        add_paragraph_.return_value = paragraph_
        paragraph_.add_run.return_value = run_
        document = Document(None, None)

        paragraph = document.add_page_break()

        add_paragraph_.assert_called_once_with(document)
        paragraph_.add_run.assert_called_once_with()
        run_.add_break.assert_called_once_with(WD_BREAK.PAGE)
        assert paragraph is paragraph_

    def it_can_add_a_paragraph(self, add_paragraph_fixture):
        document, text, style, paragraph_ = add_paragraph_fixture
        paragraph = document.add_paragraph(text, style)
        document._body.add_paragraph.assert_called_once_with(text, style)
        assert paragraph is paragraph_

    def it_can_add_a_picture(self, add_picture_fixture):
        document, path, width, height, run_, picture_ = add_picture_fixture
        picture = document.add_picture(path, width, height)
        run_.add_picture.assert_called_once_with(path, width, height)
        assert picture is picture_

    def it_can_add_a_section(
        self, add_section_fixture, Section_, section_, document_part_
    ):
        document_elm, start_type, expected_xml = add_section_fixture
        Section_.return_value = section_
        document = Document(document_elm, document_part_)

        section = document.add_section(start_type)

        assert document.element.xml == expected_xml
        sectPr = document.element.xpath("w:body/w:sectPr")[0]
        Section_.assert_called_once_with(sectPr, document_part_)
        assert section is section_

    def it_can_add_a_table(self, add_table_fixture):
        document, rows, cols, style, width, table_ = add_table_fixture
        table = document.add_table(rows, cols, style)
        document._body.add_table.assert_called_once_with(rows, cols, width)
        assert table == table_
        assert table.style == style

    def it_can_save_the_document_to_a_file(self, save_fixture):
        document, file_ = save_fixture
        document.save(file_)
        document._part.save.assert_called_once_with(file_)

    def it_provides_access_to_its_core_properties(self, core_props_fixture):
        document, core_properties_ = core_props_fixture
        core_properties = document.core_properties
        assert core_properties is core_properties_

    def it_provides_access_to_its_inline_shapes(self, inline_shapes_fixture):
        document, inline_shapes_ = inline_shapes_fixture
        assert document.inline_shapes is inline_shapes_

    def it_can_iterate_the_inner_content_of_the_document(
        self, body_prop_: Mock, body_: Mock, document_part_: Mock
    ):
        document_elm = cast(CT_Document, element("w:document"))
        body_prop_.return_value = body_
        body_.iter_inner_content.return_value = iter((1, 2, 3))
        document = Document(document_elm, document_part_)

        assert list(document.iter_inner_content()) == [1, 2, 3]

    def it_provides_access_to_its_paragraphs(self, paragraphs_fixture):
        document, paragraphs_ = paragraphs_fixture
        paragraphs = document.paragraphs
        assert paragraphs is paragraphs_

    def it_provides_access_to_its_sections(self, document_part_, Sections_, sections_):
        document_elm = element("w:document")
        Sections_.return_value = sections_
        document = Document(document_elm, document_part_)

        sections = document.sections

        Sections_.assert_called_once_with(document_elm, document_part_)
        assert sections is sections_

    def it_provides_access_to_its_settings(self, settings_fixture):
        document, settings_ = settings_fixture
        assert document.settings is settings_

    def it_provides_access_to_its_styles(self, styles_fixture):
        document, styles_ = styles_fixture
        assert document.styles is styles_

    def it_provides_access_to_its_tables(self, tables_fixture):
        document, tables_ = tables_fixture
        tables = document.tables
        assert tables is tables_

    def it_provides_access_to_the_document_part(self, part_fixture):
        document, part_ = part_fixture
        assert document.part is part_

    def it_provides_access_to_the_document_body(self, body_fixture):
        document, body_elm, _Body_, body_ = body_fixture
        body = document._body
        _Body_.assert_called_once_with(body_elm, document)
        assert body is body_

    def it_determines_block_width_to_help(self, block_width_fixture):
        document, expected_value = block_width_fixture
        width = document._block_width
        assert isinstance(width, Length)
        assert width == expected_value

    # fixtures -------------------------------------------------------

    @pytest.fixture(
        params=[
            (0, "Title"),
            (1, "Heading 1"),
            (2, "Heading 2"),
            (9, "Heading 9"),
        ]
    )
    def add_heading_fixture(self, request):
        level, style = request.param
        return level, style

    @pytest.fixture(
        params=[
            ("", None),
            ("", "Heading 1"),
            ("foo\rbar", "Body Text"),
        ]
    )
    def add_paragraph_fixture(self, request, body_prop_, paragraph_):
        text, style = request.param
        document = Document(None, None)
        body_prop_.return_value.add_paragraph.return_value = paragraph_
        return document, text, style, paragraph_

    @pytest.fixture
    def add_picture_fixture(self, request, add_paragraph_, run_, picture_):
        document = Document(None, None)
        path, width, height = "foobar.png", 100, 200
        add_paragraph_.return_value.add_run.return_value = run_
        run_.add_picture.return_value = picture_
        return document, path, width, height, run_, picture_

    @pytest.fixture(
        params=[
            ("w:sectPr", WD_SECTION.EVEN_PAGE, "w:sectPr/w:type{w:val=evenPage}"),
            (
                "w:sectPr/w:type{w:val=evenPage}",
                WD_SECTION.ODD_PAGE,
                "w:sectPr/w:type{w:val=oddPage}",
            ),
            ("w:sectPr/w:type{w:val=oddPage}", WD_SECTION.NEW_PAGE, "w:sectPr"),
        ]
    )
    def add_section_fixture(self, request):
        sentinel, start_type, new_sentinel = request.param
        document_elm = element("w:document/w:body/(w:p,%s)" % sentinel)
        expected_xml = xml(
            "w:document/w:body/(w:p,w:p/w:pPr/%s,%s)" % (sentinel, new_sentinel)
        )
        return document_elm, start_type, expected_xml

    @pytest.fixture
    def add_table_fixture(self, _block_width_prop_, body_prop_, table_):
        document = Document(None, None)
        rows, cols, style = 4, 2, "Light Shading Accent 1"
        body_prop_.return_value.add_table.return_value = table_
        _block_width_prop_.return_value = width = 42
        return document, rows, cols, style, width, table_

    @pytest.fixture
    def block_width_fixture(self, sections_prop_, section_):
        document = Document(None, None)
        sections_prop_.return_value = [None, section_]
        section_.page_width = 6000
        section_.left_margin = 1500
        section_.right_margin = 1000
        expected_value = 3500
        return document, expected_value

    @pytest.fixture
    def body_fixture(self, _Body_, body_):
        document_elm = element("w:document/w:body")
        body_elm = document_elm[0]
        document = Document(document_elm, None)
        return document, body_elm, _Body_, body_

    @pytest.fixture
    def core_props_fixture(self, document_part_, core_properties_):
        document = Document(None, document_part_)
        document_part_.core_properties = core_properties_
        return document, core_properties_

    @pytest.fixture
    def inline_shapes_fixture(self, document_part_, inline_shapes_):
        document = Document(None, document_part_)
        document_part_.inline_shapes = inline_shapes_
        return document, inline_shapes_

    @pytest.fixture
    def paragraphs_fixture(self, body_prop_, paragraphs_):
        document = Document(None, None)
        body_prop_.return_value.paragraphs = paragraphs_
        return document, paragraphs_

    @pytest.fixture
    def part_fixture(self, document_part_):
        document = Document(None, document_part_)
        return document, document_part_

    @pytest.fixture
    def save_fixture(self, document_part_):
        document = Document(None, document_part_)
        file_ = "foobar.docx"
        return document, file_

    @pytest.fixture
    def settings_fixture(self, document_part_, settings_):
        document = Document(None, document_part_)
        document_part_.settings = settings_
        return document, settings_

    @pytest.fixture
    def styles_fixture(self, document_part_, styles_):
        document = Document(None, document_part_)
        document_part_.styles = styles_
        return document, styles_

    @pytest.fixture
    def tables_fixture(self, body_prop_, tables_):
        document = Document(None, None)
        body_prop_.return_value.tables = tables_
        return document, tables_

    # fixture components ---------------------------------------------

    @pytest.fixture
    def add_paragraph_(self, request):
        return method_mock(request, Document, "add_paragraph")

    @pytest.fixture
    def _Body_(self, request, body_):
        return class_mock(request, "docx.document._Body", return_value=body_)

    @pytest.fixture
    def body_(self, request):
        return instance_mock(request, _Body)

    @pytest.fixture
    def _block_width_prop_(self, request):
        return property_mock(request, Document, "_block_width")

    @pytest.fixture
    def body_prop_(self, request, body_):
        return property_mock(request, Document, "_body", return_value=body_)

    @pytest.fixture
    def core_properties_(self, request):
        return instance_mock(request, CoreProperties)

    @pytest.fixture
    def document_part_(self, request):
        return instance_mock(request, DocumentPart)

    @pytest.fixture
    def inline_shapes_(self, request):
        return instance_mock(request, InlineShapes)

    @pytest.fixture
    def paragraph_(self, request):
        return instance_mock(request, Paragraph)

    @pytest.fixture
    def paragraphs_(self, request):
        return instance_mock(request, list)

    @pytest.fixture
    def picture_(self, request):
        return instance_mock(request, InlineShape)

    @pytest.fixture
    def run_(self, request):
        return instance_mock(request, Run)

    @pytest.fixture
    def Section_(self, request):
        return class_mock(request, "docx.document.Section")

    @pytest.fixture
    def section_(self, request):
        return instance_mock(request, Section)

    @pytest.fixture
    def Sections_(self, request):
        return class_mock(request, "docx.document.Sections")

    @pytest.fixture
    def sections_(self, request):
        return instance_mock(request, Sections)

    @pytest.fixture
    def sections_prop_(self, request):
        return property_mock(request, Document, "sections")

    @pytest.fixture
    def settings_(self, request):
        return instance_mock(request, Settings)

    @pytest.fixture
    def styles_(self, request):
        return instance_mock(request, Styles)

    @pytest.fixture
    def table_(self, request):
        return instance_mock(request, Table, style="UNASSIGNED")

    @pytest.fixture
    def tables_(self, request):
        return instance_mock(request, list)


class Describe_Body:
    def it_can_clear_itself_of_all_content_it_holds(self, clear_fixture):
        body, expected_xml = clear_fixture
        _body = body.clear_content()
        assert body._body.xml == expected_xml
        assert _body is body

    # fixtures -------------------------------------------------------

    @pytest.fixture(
        params=[
            ("w:body", "w:body"),
            ("w:body/w:p", "w:body"),
            ("w:body/w:sectPr", "w:body/w:sectPr"),
            ("w:body/(w:p, w:sectPr)", "w:body/w:sectPr"),
        ]
    )
    def clear_fixture(self, request):
        before_cxml, after_cxml = request.param
        body = _Body(element(before_cxml), None)
        expected_xml = xml(after_cxml)
        return body, expected_xml
