# encoding: utf-8

"""
Test suite for the docx.api module
"""

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

import pytest

import docx

from docx.api import Document, DocumentNew
from docx.opc.constants import CONTENT_TYPE as CT, RELATIONSHIP_TYPE as RT
from docx.opc.coreprops import CoreProperties
from docx.package import Package
from docx.parts.document import DocumentPart, InlineShapes
from docx.parts.numbering import NumberingPart
from docx.section import Section
from docx.styles.styles import Styles
from docx.table import Table
from docx.text.run import Run

from .unitutil.mock import (
    function_mock, instance_mock, class_mock, property_mock
)


class DescribeDocument(object):

    def it_opens_a_docx_file(self, open_fixture):
        docx, Package_, document_ = open_fixture
        document = DocumentNew(docx)
        Package_.open.assert_called_once_with(docx)
        assert document is document_

    def it_opens_the_default_docx_if_none_specified(self, default_fixture):
        docx, Package_, document_ = default_fixture
        document = DocumentNew()
        Package_.open.assert_called_once_with(docx)
        assert document is document_

    def it_raises_on_not_a_Word_file(self, raise_fixture):
        not_a_docx = raise_fixture
        with pytest.raises(ValueError):
            Document(not_a_docx)

    # fixtures -------------------------------------------------------

    @pytest.fixture
    def default_fixture(self, _default_docx_path_, Package_, document_):
        docx = 'barfoo.docx'
        _default_docx_path_.return_value = docx
        document_part = Package_.open.return_value.main_document_part
        document_part.document = document_
        document_part.content_type = CT.WML_DOCUMENT_MAIN
        return docx, Package_, document_

    @pytest.fixture
    def open_fixture(self, Package_, document_):
        docx = 'foobar.docx'
        document_part = Package_.open.return_value.main_document_part
        document_part.document = document_
        document_part.content_type = CT.WML_DOCUMENT_MAIN
        return docx, Package_, document_

    @pytest.fixture
    def raise_fixture(self, Package_):
        not_a_docx = 'foobar.xlsx'
        Package_.open.return_value.main_document_part.content_type = 'BOGUS'
        return not_a_docx

    # fixture components ---------------------------------------------

    @pytest.fixture
    def _default_docx_path_(self, request):
        return function_mock(request, 'docx.api._default_docx_path')

    @pytest.fixture
    def document_(self, request):
        return instance_mock(request, docx.document.Document)

    @pytest.fixture
    def Package_(self, request):
        return class_mock(request, 'docx.api.Package')


class DescribeDocumentOld(object):

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
    def core_properties_(self, request):
        return instance_mock(request, CoreProperties)

    @pytest.fixture
    def Document_inline_shapes_(self, request, inline_shapes_):
        return property_mock(
            request, Document, 'inline_shapes', return_value=inline_shapes_
        )

    @pytest.fixture
    def document(self, open_):
        return Document()

    @pytest.fixture
    def document_obj_(self, request):
        return instance_mock(request, docx.document.Document)

    @pytest.fixture
    def document_part_(self, request, paragraphs_, table_, tables_):
        document_part_ = instance_mock(
            request, DocumentPart, content_type=CT.WML_DOCUMENT_MAIN
        )
        document_part_.add_table.return_value = table_
        document_part_.paragraphs = paragraphs_
        document_part_.tables = tables_
        return document_part_

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
    def open_(self, request, document_obj_, document_part_, package_):
        document_part_.package = package_
        document_obj_._part = document_part_
        return function_mock(
            request, 'docx.api.DocumentNew',
            return_value=document_obj_
        )

    @pytest.fixture
    def Package_(self, request, package_):
        Package_ = class_mock(request, 'docx.api.Package')
        Package_.open.return_value = package_
        return Package_

    @pytest.fixture
    def package_(self, request, document_part_):
        package_ = instance_mock(request, Package)
        package_.main_document_part = document_part_
        return package_

    @pytest.fixture
    def paragraphs_(self, request):
        return instance_mock(request, list)

    @pytest.fixture
    def run_(self, request):
        return instance_mock(request, Run)

    @pytest.fixture
    def section_(self, request):
        return instance_mock(request, Section)

    @pytest.fixture
    def styles_(self, request):
        return instance_mock(request, Styles)

    @pytest.fixture
    def table_(self, request):
        return instance_mock(request, Table, style=None)

    @pytest.fixture
    def tables_(self, request):
        return instance_mock(request, list)
