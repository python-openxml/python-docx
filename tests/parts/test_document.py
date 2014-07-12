# encoding: utf-8

"""
Test suite for the docx.parts.document module
"""

from __future__ import absolute_import, print_function, unicode_literals

import pytest

from docx.opc.constants import RELATIONSHIP_TYPE as RT
from docx.oxml.parts.document import CT_Body, CT_Document
from docx.oxml.section import CT_SectPr
from docx.oxml.text import CT_R
from docx.package import ImageParts, Package
from docx.parts.document import _Body, DocumentPart, InlineShapes, Sections
from docx.parts.image import ImagePart
from docx.section import Section
from docx.shape import InlineShape
from docx.table import Table
from docx.text import Paragraph, Run

from ..oxml.parts.unitdata.document import a_body, a_document
from ..oxml.unitdata.table import (
    a_gridCol, a_tbl, a_tblGrid, a_tblPr, a_tblW, a_tc, a_tr
)
from ..oxml.unitdata.text import a_p, a_sectPr
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

    def it_provides_access_to_the_inline_shapes_in_the_document(
            self, inline_shapes_fixture):
        document, InlineShapes_, body_elm = inline_shapes_fixture
        inline_shapes = document.inline_shapes
        InlineShapes_.assert_called_once_with(body_elm, document)
        assert inline_shapes is InlineShapes_.return_value

    def it_can_add_a_paragraph(self, add_paragraph_fixture):
        document_part, body_, p_ = add_paragraph_fixture
        p = document_part.add_paragraph()
        body_.add_paragraph.assert_called_once_with()
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
    def body_fixture(self, request, _Body_):
        document_elm = (
            a_document().with_nsdecls().with_child(
                a_body())
        ).element
        body_elm = document_elm[0]
        document_part = DocumentPart(None, None, document_elm, None)
        return document_part, _Body_, body_elm

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
    def sections_fixture(self, request, Sections_):
        document_elm = a_document().with_nsdecls().element
        document = DocumentPart(None, None, document_elm, None)
        return document, document_elm, Sections_

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
        body, expected_xml = add_table_fixture
        table = body.add_table(rows=1, cols=1)
        assert body._body.xml == expected_xml
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

    @pytest.fixture(params=[(0, False), (0, True), (1, False), (1, True)])
    def add_table_fixture(self, request):
        p_count, has_sectPr = request.param
        body_bldr = self._body_bldr(p_count=p_count, sectPr=has_sectPr)
        body = _Body(body_bldr.element, None)

        tbl_bldr = self._tbl_bldr()
        body_bldr = self._body_bldr(
            p_count=p_count, tbl_bldr=tbl_bldr, sectPr=has_sectPr
        )
        expected_xml = body_bldr.xml()

        return body, expected_xml

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

    # fixture components ---------------------------------------------

    def _body_bldr(self, p_count=0, tbl_bldr=None, sectPr=False):
        body_bldr = a_body().with_nsdecls()
        for i in range(p_count):
            body_bldr.with_child(a_p())
        if tbl_bldr is not None:
            body_bldr.with_child(tbl_bldr)
        if sectPr:
            body_bldr.with_child(a_sectPr())
        return body_bldr

    def _tbl_bldr(self, rows=1, cols=1):
        tblPr_bldr = (
            a_tblPr().with_child(
                a_tblW().with_type("auto").with_w(0))
        )

        tblGrid_bldr = a_tblGrid()
        for i in range(cols):
            tblGrid_bldr.with_child(a_gridCol())

        tbl_bldr = a_tbl()
        tbl_bldr.with_child(tblPr_bldr)
        tbl_bldr.with_child(tblGrid_bldr)
        for i in range(rows):
            tr_bldr = self._tr_bldr(cols)
            tbl_bldr.with_child(tr_bldr)

        return tbl_bldr

    def _tc_bldr(self):
        return a_tc().with_child(a_p())

    def _tr_bldr(self, cols):
        tr_bldr = a_tr()
        for i in range(cols):
            tc_bldr = self._tc_bldr()
            tr_bldr.with_child(tc_bldr)
        return tr_bldr


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
