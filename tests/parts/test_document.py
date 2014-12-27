# encoding: utf-8

"""
Test suite for the docx.parts.document module
"""

from __future__ import absolute_import, print_function, unicode_literals

import pytest

from docx.opc.constants import RELATIONSHIP_TYPE as RT
from docx.oxml.parts.document import CT_Body, CT_Document
from docx.oxml.section import CT_SectPr
from docx.oxml.text.run import CT_R
from docx.package import ImageParts, Package
from docx.parts.document import _Body, DocumentPart, InlineShapes, Sections
from docx.parts.image import ImagePart
from docx.parts.styles import StylesPart
from docx.section import Section
from docx.shape import InlineShape
from docx.styles.style import BaseStyle
from docx.styles.styles import Styles
from docx.table import Table
from docx.text.paragraph import Paragraph
from docx.text.run import Run

from ..oxml.parts.unitdata.document import a_body, a_document
from ..oxml.unitdata.text import a_p
from ..unitutil.cxml import element, xml
from ..unitutil.mock import (
    instance_mock, class_mock, loose_mock, method_mock, property_mock
)


class DescribeDocumentPart(object):

    def it_has_a_body(self, body_fixture):
        document_part, _Body_, body_elm = body_fixture
        _body = document_part.body
        _Body_.assert_called_once_with(body_elm, document_part)
        assert _body is _Body_.return_value

    def it_provides_access_to_the_document_paragraphs(
            self, paragraphs_fixture):
        document_part, paragraphs_ = paragraphs_fixture
        paragraphs = document_part.paragraphs
        assert paragraphs is paragraphs_

    def it_provides_access_to_the_document_sections(self, sections_fixture):
        document, document_elm, Sections_ = sections_fixture
        sections = document.sections
        Sections_.assert_called_once_with(document_elm)
        assert sections is Sections_.return_value

    def it_provides_access_to_the_document_tables(self, tables_fixture):
        document_part, tables_ = tables_fixture
        tables = document_part.tables
        assert tables is tables_

    def it_provides_access_to_the_document_styles(self, styles_fixture):
        document_part, styles_ = styles_fixture
        styles = document_part.styles
        assert styles is styles_

    def it_provides_access_to_the_inline_shapes_in_the_document(
            self, inline_shapes_fixture):
        document, InlineShapes_, body_elm = inline_shapes_fixture
        inline_shapes = document.inline_shapes
        InlineShapes_.assert_called_once_with(body_elm, document)
        assert inline_shapes is InlineShapes_.return_value

    def it_can_add_a_paragraph(self, add_paragraph_fixture):
        document_part, body_, p_ = add_paragraph_fixture
        p = document_part.add_paragraph()
        body_.add_paragraph.assert_called_once_with('', None)
        assert p is p_

    def it_can_add_a_section(self, add_section_fixture):
        (document_part, start_type_, body_elm_, new_sectPr_, Section_,
         section_) = add_section_fixture
        section = document_part.add_section(start_type_)
        body_elm_.add_section_break.assert_called_once_with()
        assert new_sectPr_.start_type == start_type_
        Section_.assert_called_once_with(new_sectPr_)
        assert section is section_

    def it_can_add_a_table(self, add_table_fixture):
        document_part, rows, cols, body_, table_ = add_table_fixture
        table = document_part.add_table(rows, cols)
        body_.add_table.assert_called_once_with(rows, cols)
        assert table is table_

    def it_can_add_an_image_part_to_the_document(
            self, get_or_add_image_fixture):
        (document, image_descriptor_, image_parts_, relate_to_, image_part_,
         rId_) = get_or_add_image_fixture
        image_part, rId = document.get_or_add_image_part(image_descriptor_)
        image_parts_.get_or_add_image_part.assert_called_once_with(
            image_descriptor_
        )
        relate_to_.assert_called_once_with(image_part_, RT.IMAGE)
        assert image_part is image_part_
        assert rId == rId_

    def it_knows_the_next_available_xml_id(self, next_id_fixture):
        document, expected_id = next_id_fixture
        assert document.next_id == expected_id

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
    def add_paragraph_fixture(self, document_part_body_, body_, p_):
        document_part = DocumentPart(None, None, None, None)
        return document_part, body_, p_

    @pytest.fixture
    def add_section_fixture(
            self, document_elm_, start_type_, body_elm_, sectPr_, Section_,
            section_):
        document_part = DocumentPart(None, None, document_elm_, None)
        return (
            document_part, start_type_, body_elm_, sectPr_, Section_,
            section_
        )

    @pytest.fixture
    def add_table_fixture(self, document_part_body_, body_, table_):
        document_part = DocumentPart(None, None, None, None)
        rows, cols = 2, 4
        return document_part, rows, cols, body_, table_

    @pytest.fixture
    def body_fixture(self, _Body_):
        document_elm = (
            a_document().with_nsdecls().with_child(
                a_body())
        ).element
        body_elm = document_elm[0]
        document_part = DocumentPart(None, None, document_elm, None)
        return document_part, _Body_, body_elm

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
    def paragraphs_fixture(self, document_part_body_, body_, paragraphs_):
        document_part = DocumentPart(None, None, None, None)
        body_.paragraphs = paragraphs_
        return document_part, paragraphs_

    @pytest.fixture
    def sections_fixture(self, Sections_):
        document_elm = a_document().with_nsdecls().element
        document = DocumentPart(None, None, document_elm, None)
        return document, document_elm, Sections_

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

    @pytest.fixture
    def tables_fixture(self, document_part_body_, body_, tables_):
        document_part = DocumentPart(None, None, None, None)
        body_.tables = tables_
        return document_part, tables_

    # fixture components ---------------------------------------------

    @pytest.fixture
    def _Body_(self, request):
        return class_mock(request, 'docx.parts.document._Body')

    @pytest.fixture
    def body_(self, request, p_, table_):
        body_ = instance_mock(request, _Body)
        body_.add_paragraph.return_value = p_
        body_.add_table.return_value = table_
        return body_

    @pytest.fixture
    def body_elm_(self, request, sectPr_):
        body_elm_ = instance_mock(request, CT_Body)
        body_elm_.add_section_break.return_value = sectPr_
        return body_elm_

    @pytest.fixture
    def document_elm_(self, request, body_elm_):
        return instance_mock(request, CT_Document, body=body_elm_)

    @pytest.fixture
    def document_part_body_(self, request, body_):
        return property_mock(
            request, DocumentPart, 'body', return_value=body_
        )

    @pytest.fixture
    def get_or_add_image_fixture(
            self, request, package_, image_descriptor_, image_parts_,
            relate_to_, image_part_, rId_):
        package_.image_parts = image_parts_
        document = DocumentPart(None, None, None, package_)
        return (
            document, image_descriptor_, image_parts_, relate_to_,
            image_part_, rId_
        )

    @pytest.fixture
    def image_descriptor_(self, request):
        return instance_mock(request, str)

    @pytest.fixture
    def image_part_(self, request):
        return instance_mock(request, ImagePart)

    @pytest.fixture
    def image_parts_(self, request, image_part_):
        image_parts_ = instance_mock(request, ImageParts)
        image_parts_.get_or_add_image_part.return_value = image_part_
        return image_parts_

    @pytest.fixture
    def InlineShapes_(self, request):
        return class_mock(request, 'docx.parts.document.InlineShapes')

    @pytest.fixture
    def p_(self, request):
        return instance_mock(request, Paragraph)

    @pytest.fixture
    def package_(self, request):
        return instance_mock(request, Package)

    @pytest.fixture
    def paragraphs_(self, request):
        return instance_mock(request, list)

    @pytest.fixture
    def part_related_by_(self, request):
        return method_mock(request, DocumentPart, 'part_related_by')

    @pytest.fixture
    def relate_to_(self, request, rId_):
        relate_to_ = method_mock(request, DocumentPart, 'relate_to')
        relate_to_.return_value = rId_
        return relate_to_

    @pytest.fixture
    def rId_(self, request):
        return instance_mock(request, str)

    @pytest.fixture
    def Section_(self, request, section_):
        return class_mock(
            request, 'docx.parts.document.Section', return_value=section_
        )

    @pytest.fixture
    def section_(self, request):
        return instance_mock(request, Section)

    @pytest.fixture
    def Sections_(self, request):
        return class_mock(request, 'docx.parts.document.Sections')

    @pytest.fixture
    def sectPr_(self, request):
        return instance_mock(request, CT_SectPr)

    @pytest.fixture
    def start_type_(self, request):
        return instance_mock(request, int)

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

    @pytest.fixture
    def table_(self, request):
        return instance_mock(request, Table)

    @pytest.fixture
    def tables_(self, request):
        return instance_mock(request, list)


class Describe_Body(object):

    def it_can_add_a_paragraph(self, add_paragraph_fixture):
        body, expected_xml = add_paragraph_fixture
        p = body.add_paragraph()
        assert body._body.xml == expected_xml
        assert isinstance(p, Paragraph)

    def it_can_add_a_table(self, add_table_fixture):
        body, rows, cols, expected_xml = add_table_fixture
        table = body.add_table(rows, cols)
        assert body._element.xml == expected_xml
        assert isinstance(table, Table)

    def it_can_clear_itself_of_all_content_it_holds(self, clear_fixture):
        body, expected_xml = clear_fixture
        _body = body.clear_content()
        assert body._body.xml == expected_xml
        assert _body is body

    def it_provides_access_to_the_paragraphs_it_contains(
            self, paragraphs_fixture):
        body = paragraphs_fixture
        paragraphs = body.paragraphs
        assert len(paragraphs) == 2
        for p in paragraphs:
            assert isinstance(p, Paragraph)

    def it_provides_access_to_the_tables_it_contains(self, tables_fixture):
        body = tables_fixture
        tables = body.tables
        assert len(tables) == 2
        for table in tables:
            assert isinstance(table, Table)

    # fixtures -------------------------------------------------------

    @pytest.fixture(params=[
        ('w:body',                 'w:body/w:p'),
        ('w:body/w:p',             'w:body/(w:p, w:p)'),
        ('w:body/w:sectPr',        'w:body/(w:p, w:sectPr)'),
        ('w:body/(w:p, w:sectPr)', 'w:body/(w:p, w:p, w:sectPr)'),
    ])
    def add_paragraph_fixture(self, request):
        before_cxml, after_cxml = request.param
        body = _Body(element(before_cxml), None)
        expected_xml = xml(after_cxml)
        return body, expected_xml

    @pytest.fixture(params=[
        ('w:body', 0, 0, 'w:body/w:tbl/(w:tblPr/w:tblW{w:type=auto,w:w=0},w:'
         'tblGrid)'),
        ('w:body', 1, 0, 'w:body/w:tbl/(w:tblPr/w:tblW{w:type=auto,w:w=0},w:'
         'tblGrid,w:tr)'),
        ('w:body', 0, 1, 'w:body/w:tbl/(w:tblPr/w:tblW{w:type=auto,w:w=0},w:'
         'tblGrid/w:gridCol)'),
        ('w:body', 1, 1, 'w:body/w:tbl/(w:tblPr/w:tblW{w:type=auto,w:w=0},w:'
         'tblGrid/w:gridCol,w:tr/w:tc/w:p)'),
    ])
    def add_table_fixture(self, request):
        body_cxml, rows, cols, after_cxml = request.param
        body = _Body(element(body_cxml), None)
        expected_xml = xml(after_cxml)
        return body, rows, cols, expected_xml

    @pytest.fixture(params=[
        ('w:body',                 'w:body'),
        ('w:body/w:p',             'w:body'),
        ('w:body/w:sectPr',        'w:body/w:sectPr'),
        ('w:body/(w:p, w:sectPr)', 'w:body/w:sectPr'),
    ])
    def clear_fixture(self, request):
        before_cxml, after_cxml = request.param
        body = _Body(element(before_cxml), None)
        expected_xml = xml(after_cxml)
        return body, expected_xml

    @pytest.fixture
    def paragraphs_fixture(self):
        return _Body(element('w:body/(w:p, w:p)'), None)

    @pytest.fixture
    def tables_fixture(self):
        return _Body(element('w:body/(w:tbl, w:tbl)'), None)


class DescribeInlineShapes(object):

    def it_knows_how_many_inline_shapes_it_contains(
            self, inline_shapes_fixture):
        inline_shapes, expected_count = inline_shapes_fixture
        assert len(inline_shapes) == expected_count

    def it_can_iterate_over_its_InlineShape_instances(
            self, inline_shapes_fixture):
        inline_shapes, inline_shape_count = inline_shapes_fixture
        actual_count = 0
        for inline_shape in inline_shapes:
            assert isinstance(inline_shape, InlineShape)
            actual_count += 1
        assert actual_count == inline_shape_count

    def it_provides_indexed_access_to_inline_shapes(
            self, inline_shapes_fixture):
        inline_shapes, inline_shape_count = inline_shapes_fixture
        for idx in range(-inline_shape_count, inline_shape_count):
            inline_shape = inline_shapes[idx]
            assert isinstance(inline_shape, InlineShape)

    def it_raises_on_indexed_access_out_of_range(
            self, inline_shapes_fixture):
        inline_shapes, inline_shape_count = inline_shapes_fixture
        with pytest.raises(IndexError):
            too_low = -1 - inline_shape_count
            inline_shapes[too_low]
        with pytest.raises(IndexError):
            too_high = inline_shape_count
            inline_shapes[too_high]

    def it_can_add_an_inline_picture_to_the_document(
            self, add_picture_fixture):
        # fixture ----------------------
        (inline_shapes, image_descriptor_, document_, InlineShape_,
         run, r_, image_part_, rId_, shape_id_, new_picture_shape_
         ) = add_picture_fixture
        # exercise ---------------------
        picture_shape = inline_shapes.add_picture(image_descriptor_, run)
        # verify -----------------------
        document_.get_or_add_image_part.assert_called_once_with(
            image_descriptor_
        )
        InlineShape_.new_picture.assert_called_once_with(
            r_, image_part_, rId_, shape_id_
        )
        assert picture_shape is new_picture_shape_

    def it_knows_the_part_it_belongs_to(self, inline_shapes_with_parent_):
        inline_shapes, parent_ = inline_shapes_with_parent_
        part = inline_shapes.part
        assert part is parent_.part

    # fixtures -------------------------------------------------------

    @pytest.fixture
    def add_picture_fixture(
            self, request, body_, document_, image_descriptor_, InlineShape_,
            r_, image_part_, rId_, shape_id_, new_picture_shape_):
        inline_shapes = InlineShapes(body_, None)
        property_mock(request, InlineShapes, 'part', return_value=document_)
        run = Run(r_, None)
        return (
            inline_shapes, image_descriptor_, document_, InlineShape_, run,
            r_, image_part_, rId_, shape_id_, new_picture_shape_
        )

    @pytest.fixture
    def inline_shapes_fixture(self):
        body = element(
            'w:body/w:p/(w:r/w:drawing/wp:inline, w:r/w:drawing/wp:inline)'
        )
        inline_shapes = InlineShapes(body, None)
        expected_count = 2
        return inline_shapes, expected_count

    # fixture components ---------------------------------------------

    @pytest.fixture
    def body_(self, request, r_):
        body_ = instance_mock(request, CT_Body)
        body_.add_p.return_value.add_r.return_value = r_
        return body_

    @pytest.fixture
    def document_(self, request, rId_, image_part_, shape_id_):
        document_ = instance_mock(request, DocumentPart, name='document_')
        document_.get_or_add_image_part.return_value = image_part_, rId_
        document_.next_id = shape_id_
        return document_

    @pytest.fixture
    def image_part_(self, request):
        return instance_mock(request, ImagePart)

    @pytest.fixture
    def image_descriptor_(self, request):
        return instance_mock(request, str)

    @pytest.fixture
    def InlineShape_(self, request, new_picture_shape_):
        InlineShape_ = class_mock(request, 'docx.parts.document.InlineShape')
        InlineShape_.new_picture.return_value = new_picture_shape_
        return InlineShape_

    @pytest.fixture
    def inline_shapes_with_parent_(self, request):
        parent_ = loose_mock(request, name='parent_')
        inline_shapes = InlineShapes(None, parent_)
        return inline_shapes, parent_

    @pytest.fixture
    def new_picture_shape_(self, request):
        return instance_mock(request, InlineShape)

    @pytest.fixture
    def r_(self, request):
        return instance_mock(request, CT_R)

    @pytest.fixture
    def rId_(self, request):
        return instance_mock(request, str)

    @pytest.fixture
    def shape_id_(self, request):
        return instance_mock(request, int)


class DescribeSections(object):

    def it_knows_how_many_sections_it_contains(self, len_fixture):
        sections, expected_len = len_fixture
        assert len(sections) == expected_len

    def it_can_iterate_over_its_Section_instances(self, iter_fixture):
        sections, expected_count = iter_fixture
        section_count = 0
        for section in sections:
            section_count += 1
            assert isinstance(section, Section)
        assert section_count == expected_count

    def it_can_access_its_Section_instances_by_index(self, index_fixture):
        sections, indicies = index_fixture
        assert len(sections[0:2]) == 2
        for index in indicies:
            assert isinstance(sections[index], Section)

    # fixtures -------------------------------------------------------

    @pytest.fixture
    def index_fixture(self, document_elm):
        sections = Sections(document_elm)
        return sections, [0, 1]

    @pytest.fixture
    def iter_fixture(self, document_elm):
        sections = Sections(document_elm)
        return sections, 2

    @pytest.fixture
    def len_fixture(self, document_elm):
        sections = Sections(document_elm)
        return sections, 2

    # fixture components ---------------------------------------------

    @pytest.fixture
    def document_elm(self):
        return element('w:document/w:body/(w:p/w:pPr/w:sectPr, w:sectPr)')
