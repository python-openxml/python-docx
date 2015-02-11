# encoding: utf-8

"""
Test suite for the docx.api module
"""

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

import pytest

from docx.api import Document
from docx.enum.text import WD_BREAK
from docx.opc.constants import CONTENT_TYPE as CT, RELATIONSHIP_TYPE as RT
from docx.opc.coreprops import CoreProperties
from docx.package import Package
from docx.parts.document import DocumentPart, InlineShapes
from docx.parts.numbering import NumberingPart
from docx.section import Section
from docx.shape import InlineShape
from docx.styles.styles import Styles
from docx.table import Table
from docx.text.paragraph import Paragraph
from docx.text.run import Run

from .unitutil.mock import (
    instance_mock, class_mock, method_mock, property_mock, var_mock
)


class DescribeDocument(object):

    def it_opens_a_docx_on_construction(self, init_fixture):
        docx_, open_ = init_fixture
        document = Document(docx_)
        open_.assert_called_once_with(docx_)
        assert isinstance(document, Document)

    def it_can_open_a_docx_file(self, open_fixture):
        docx_, Package_, package_, document_part_ = open_fixture
        document_part, package = Document._open(docx_)
        Package_.open.assert_called_once_with(docx_)
        assert document_part is document_part
        assert package is package_

    def it_opens_default_template_if_no_file_provided(
            self, Package_, default_docx_):
        Document._open(None)
        Package_.open.assert_called_once_with(default_docx_)

    def it_should_raise_if_not_a_Word_file(self, Package_, package_, docx_):
        package_.main_document.content_type = 'foobar'
        with pytest.raises(ValueError):
            Document._open(docx_)

    def it_can_add_a_heading(self, add_heading_fixture):
        document, text, level, style, paragraph_ = add_heading_fixture
        paragraph = document.add_heading(text, level)
        document.add_paragraph.assert_called_once_with(text, style)
        assert paragraph is paragraph_

    def it_should_raise_on_heading_level_out_of_range(self, document):
        with pytest.raises(ValueError):
            document.add_heading(level=-1)
        with pytest.raises(ValueError):
            document.add_heading(level=10)

    def it_can_add_a_paragraph(self, add_paragraph_fixture):
        document, text, style, paragraph_ = add_paragraph_fixture
        paragraph = document.add_paragraph(text, style)
        document._document_part.add_paragraph.assert_called_once_with(
            text, style
        )
        assert paragraph is paragraph_

    def it_can_add_a_page_break(self, add_page_break_fixture):
        document, document_part_, paragraph_, run_ = add_page_break_fixture
        paragraph = document.add_page_break()
        document_part_.add_paragraph.assert_called_once_with()
        paragraph_.add_run.assert_called_once_with()
        run_.add_break.assert_called_once_with(WD_BREAK.PAGE)
        assert paragraph is paragraph_

    def it_can_add_a_picture(self, add_picture_fixture):
        document, image_path_, width, height, run_, picture_ = (
            add_picture_fixture
        )
        picture = document.add_picture(image_path_, width, height)
        run_.add_picture.assert_called_once_with(image_path_, width, height)
        assert picture is picture_

    def it_can_add_a_section(self, add_section_fixture):
        document, start_type_, section_ = add_section_fixture
        section = document.add_section(start_type_)
        document._document_part.add_section.assert_called_once_with(
            start_type_
        )
        assert section is section_

    def it_can_add_a_table(self, add_table_fixture):
        document, rows, cols, style, table_ = add_table_fixture
        table = document.add_table(rows, cols, style)
        document._document_part.add_table.assert_called_once_with(rows, cols)
        assert table.style == style
        assert table == table_

    def it_provides_access_to_the_document_inline_shapes(self, document):
        body = document.inline_shapes
        assert body is document._document_part.inline_shapes

    def it_provides_access_to_the_document_paragraphs(
            self, paragraphs_fixture):
        document, paragraphs_ = paragraphs_fixture
        paragraphs = document.paragraphs
        assert paragraphs is paragraphs_

    def it_provides_access_to_the_document_sections(self, document):
        body = document.sections
        assert body is document._document_part.sections

    def it_provides_access_to_the_document_tables(self, tables_fixture):
        document, tables_ = tables_fixture
        tables = document.tables
        assert tables is tables_

    def it_can_save_the_package(self, save_fixture):
        document, package_, file_ = save_fixture
        document.save(file_)
        package_.save.assert_called_once_with(file_)

    def it_provides_access_to_its_core_properties(self, core_props_fixture):
        document, core_properties_ = core_props_fixture
        core_properties = document.core_properties
        assert core_properties is core_properties_

    def it_provides_access_to_its_styles(self, styles_fixture):
        document, styles_ = styles_fixture
        styles = document.styles
        assert styles is styles_

    def it_provides_access_to_the_numbering_part(self, num_part_get_fixture):
        document, document_part_, numbering_part_ = num_part_get_fixture
        numbering_part = document.numbering_part
        document_part_.part_related_by.assert_called_once_with(RT.NUMBERING)
        assert numbering_part is numbering_part_

    def it_creates_numbering_part_on_first_access_if_not_present(
            self, num_part_create_fixture):
        document, NumberingPart_, document_part_, numbering_part_ = (
            num_part_create_fixture
        )
        numbering_part = document.numbering_part
        NumberingPart_.new.assert_called_once_with()
        document_part_.relate_to.assert_called_once_with(
            numbering_part_, RT.NUMBERING
        )
        assert numbering_part is numbering_part_

    # fixtures -------------------------------------------------------

    @pytest.fixture(params=[
        ('',         None),
        ('',         'Heading 1'),
        ('foo\rbar', 'Body Text'),
    ])
    def add_paragraph_fixture(self, request, document, document_part_,
                              paragraph_):
        text, style = request.param
        return document, text, style, paragraph_

    @pytest.fixture(params=[
        (0, 'Title'),
        (1, 'Heading 1'),
        (2, 'Heading 2'),
        (9, 'Heading 9'),
    ])
    def add_heading_fixture(self, request, document, add_paragraph_,
                            paragraph_):
        level, style = request.param
        text = 'Spam vs. Bacon'
        return document, text, level, style, paragraph_

    @pytest.fixture
    def add_page_break_fixture(
            self, document, document_part_, paragraph_, run_):
        return document, document_part_, paragraph_, run_

    @pytest.fixture
    def add_picture_fixture(self, request, run_, picture_):
        document = Document()
        image_path_ = instance_mock(request, str, name='image_path_')
        width, height = 100, 200
        class_mock(request, 'docx.text.paragraph.Run', return_value=run_)
        run_.add_picture.return_value = picture_
        return (document, image_path_, width, height, run_, picture_)

    @pytest.fixture
    def add_section_fixture(self, document, start_type_, section_):
        return document, start_type_, section_

    @pytest.fixture
    def add_table_fixture(self, request, document, document_part_, table_):
        rows, cols = 4, 2
        style = 'Light Shading Accent 1'
        return document, rows, cols, style, table_

    @pytest.fixture
    def core_props_fixture(self, document, core_properties_):
        document._package.core_properties = core_properties_
        return document, core_properties_

    @pytest.fixture
    def init_fixture(self, docx_, open_):
        return docx_, open_

    @pytest.fixture
    def num_part_get_fixture(self, document, document_part_, numbering_part_):
        document_part_.part_related_by.return_value = numbering_part_
        return document, document_part_, numbering_part_

    @pytest.fixture
    def open_fixture(self, docx_, Package_, package_, document_part_):
        return docx_, Package_, package_, document_part_

    @pytest.fixture
    def paragraphs_fixture(self, document, paragraphs_):
        return document, paragraphs_

    @pytest.fixture
    def save_fixture(self, request, open_, package_):
        file_ = instance_mock(request, str)
        document = Document()
        return document, package_, file_

    @pytest.fixture
    def styles_fixture(self, document, styles_):
        document._document_part.styles = styles_
        return document, styles_

    @pytest.fixture
    def tables_fixture(self, document, tables_):
        return document, tables_

    # fixture components ---------------------------------------------

    @pytest.fixture
    def add_paragraph_(self, request, paragraph_):
        return method_mock(
            request, Document, 'add_paragraph', return_value=paragraph_
        )

    @pytest.fixture
    def core_properties_(self, request):
        return instance_mock(request, CoreProperties)

    @pytest.fixture
    def default_docx_(self, request):
        return var_mock(request, 'docx.api._default_docx_path')

    @pytest.fixture
    def Document_inline_shapes_(self, request, inline_shapes_):
        return property_mock(
            request, Document, 'inline_shapes', return_value=inline_shapes_
        )

    @pytest.fixture
    def document(self, open_):
        return Document()

    @pytest.fixture
    def document_part_(
            self, request, paragraph_, paragraphs_, section_, table_,
            tables_):
        document_part_ = instance_mock(
            request, DocumentPart, content_type=CT.WML_DOCUMENT_MAIN
        )
        document_part_.add_paragraph.return_value = paragraph_
        document_part_.add_section.return_value = section_
        document_part_.add_table.return_value = table_
        document_part_.paragraphs = paragraphs_
        document_part_.tables = tables_
        return document_part_

    @pytest.fixture
    def docx_(self, request):
        return instance_mock(request, str)

    @pytest.fixture
    def inline_shapes_(self, request):
        return instance_mock(request, InlineShapes)

    @pytest.fixture
    def num_part_create_fixture(
            self, document, NumberingPart_, document_part_, numbering_part_):
        document_part_.part_related_by.side_effect = KeyError
        return document, NumberingPart_, document_part_, numbering_part_

    @pytest.fixture
    def NumberingPart_(self, request, numbering_part_):
        NumberingPart_ = class_mock(request, 'docx.api.NumberingPart')
        NumberingPart_.new.return_value = numbering_part_
        return NumberingPart_

    @pytest.fixture
    def numbering_part_(self, request):
        return instance_mock(request, NumberingPart)

    @pytest.fixture
    def open_(self, request, document_part_, package_):
        return method_mock(
            request, Document, '_open',
            return_value=(document_part_, package_)
        )

    @pytest.fixture
    def Package_(self, request, package_):
        Package_ = class_mock(request, 'docx.api.Package')
        Package_.open.return_value = package_
        return Package_

    @pytest.fixture
    def package_(self, request, document_part_):
        package_ = instance_mock(request, Package)
        package_.main_document = document_part_
        return package_

    @pytest.fixture
    def paragraph_(self, request, run_):
        paragraph_ = instance_mock(request, Paragraph)
        paragraph_.add_run.return_value = run_
        return paragraph_

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
    def section_(self, request):
        return instance_mock(request, Section)

    @pytest.fixture
    def start_type_(self, request):
        return instance_mock(request, int)

    @pytest.fixture
    def styles_(self, request):
        return instance_mock(request, Styles)

    @pytest.fixture
    def table_(self, request):
        return instance_mock(request, Table, style=None)

    @pytest.fixture
    def tables_(self, request):
        return instance_mock(request, list)
