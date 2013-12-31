# encoding: utf-8

"""
Test suite for the docx.parts.document module
"""

from __future__ import absolute_import, print_function, unicode_literals

import pytest

from mock import Mock

from docx.opc.constants import CONTENT_TYPE as CT, RELATIONSHIP_TYPE as RT
from docx.opc.package import PartFactory
from docx.opc.packuri import PackURI
from docx.oxml.parts.document import CT_Body, CT_Document
from docx.oxml.text import CT_R
from docx.package import ImageParts, Package
from docx.parts.document import _Body, DocumentPart, InlineShapes
from docx.parts.image import ImagePart
from docx.shape import InlineShape
from docx.table import Table
from docx.text import Paragraph

from ..oxml.unitdata.dml import a_drawing, an_inline
from ..oxml.parts.unitdata.document import a_body, a_document
from ..oxml.unitdata.table import (
    a_gridCol, a_tbl, a_tblGrid, a_tblPr, a_tc, a_tr
)
from ..oxml.unitdata.text import a_p, a_sectPr, an_r
from ..unitutil import (
    function_mock, class_mock, initializer_mock, instance_mock, loose_mock,
    method_mock, property_mock
)


class DescribeDocumentPart(object):

    def it_is_used_by_PartFactory_to_construct_main_document_part(
            self, part_load_fixture):
        # fixture ----------------------
        document_part_load_, partname_, blob_, package_, document_part_ = (
            part_load_fixture
        )
        content_type = CT.WML_DOCUMENT_MAIN
        reltype = RT.OFFICE_DOCUMENT
        # exercise ---------------------
        part = PartFactory(partname_, content_type, reltype, blob_, package_)
        # verify -----------------------
        document_part_load_.assert_called_once_with(
            partname_, content_type, blob_, package_
        )
        assert part is document_part_

    def it_can_be_constructed_by_opc_part_factory(
            self, oxml_fromstring_, init):
        # mockery ----------------------
        partname, content_type, blob, document_elm, package = (
            Mock(name='partname'), Mock(name='content_type'),
            Mock(name='blob'), Mock(name='document_elm'),
            Mock(name='package')
        )
        oxml_fromstring_.return_value = document_elm
        # exercise ---------------------
        doc = DocumentPart.load(partname, content_type, blob, package)
        # verify -----------------------
        oxml_fromstring_.assert_called_once_with(blob)
        init.assert_called_once_with(
            partname, content_type, document_elm, package
        )
        assert isinstance(doc, DocumentPart)

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

    def it_has_a_body(self, document_body_fixture):
        document, _Body_, body_elm = document_body_fixture
        _body = document.body
        _Body_.assert_called_once_with(body_elm)
        assert _body is _Body_.return_value

    def it_can_serialize_to_xml(self, document_blob_fixture):
        document, document_elm, serialize_part_xml_ = document_blob_fixture
        blob = document.blob
        serialize_part_xml_.assert_called_once_with(document_elm)
        assert blob is serialize_part_xml_.return_value

    def it_provides_access_to_the_inline_shapes_in_the_document(
            self, inline_shapes_fixture):
        document, InlineShapes_, body_elm = inline_shapes_fixture
        inline_shapes = document.inline_shapes
        InlineShapes_.assert_called_once_with(body_elm, document)
        assert inline_shapes is InlineShapes_.return_value

    def it_knows_it_is_the_part_its_child_objects_belong_to(self, document):
        assert document.part is document

    def it_knows_the_next_available_xml_id(self, next_id_fixture):
        document, expected_id = next_id_fixture
        assert document.next_id == expected_id

    # fixtures -------------------------------------------------------

    @pytest.fixture
    def _Body_(self, request):
        return class_mock(request, 'docx.parts.document._Body')

    @pytest.fixture
    def blob_(self, request):
        return instance_mock(request, str)

    @pytest.fixture
    def content_type_(self, request):
        return instance_mock(request, str)

    @pytest.fixture
    def document(self):
        return DocumentPart(None, None, None, None)

    @pytest.fixture
    def document_blob_fixture(self, request, serialize_part_xml_):
        document_elm = instance_mock(request, CT_Document)
        document = DocumentPart(None, None, document_elm, None)
        return document, document_elm, serialize_part_xml_

    @pytest.fixture
    def document_body_fixture(self, request, _Body_):
        document_elm = (
            a_document().with_nsdecls().with_child(
                a_body())
        ).element
        body_elm = document_elm[0]
        document = DocumentPart(None, None, document_elm, None)
        return document, _Body_, body_elm

    @pytest.fixture
    def document_part_(self, request):
        return instance_mock(request, DocumentPart)

    @pytest.fixture
    def document_part_load_(self, request):
        return method_mock(request, DocumentPart, 'load')

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
    def init(self, request):
        return initializer_mock(request, DocumentPart)

    @pytest.fixture
    def InlineShapes_(self, request):
        return class_mock(request, 'docx.parts.document.InlineShapes')

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
        ((0, 0), 1), ((0, 0, 1, 3), 2),
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
    def oxml_fromstring_(self, request):
        return function_mock(request, 'docx.parts.document.oxml_fromstring')

    @pytest.fixture
    def package_(self, request):
        return instance_mock(request, Package)

    @pytest.fixture
    def part_load_fixture(
            self, document_part_load_, partname_, blob_, package_,
            document_part_):
        document_part_load_.return_value = document_part_
        return (
            document_part_load_, partname_, blob_, package_, document_part_
        )

    @pytest.fixture
    def partname_(self, request):
        return instance_mock(request, PackURI)

    @pytest.fixture
    def relate_to_(self, request, rId_):
        relate_to_ = method_mock(request, DocumentPart, 'relate_to')
        relate_to_.return_value = rId_
        return relate_to_

    @pytest.fixture
    def rId_(self, request):
        return instance_mock(request, str)

    @pytest.fixture
    def serialize_part_xml_(self, request):
        return function_mock(
            request, 'docx.parts.document.serialize_part_xml'
        )


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

    def it_can_clear_itself_of_all_content_it_holds(
            self, clear_content_fixture):
        body, expected_xml = clear_content_fixture
        _body = body.clear_content()
        assert body._body.xml == expected_xml
        assert _body is body

    def it_provides_access_to_the_paragraphs_it_contains(
            self, body_with_paragraphs):
        body = body_with_paragraphs
        paragraphs = body.paragraphs
        assert len(paragraphs) == 2
        for p in paragraphs:
            assert isinstance(p, Paragraph)

    def it_provides_access_to_the_tables_it_contains(
            self, body_with_tables):
        body = body_with_tables
        tables = body.tables
        assert len(tables) == 2
        for table in tables:
            assert isinstance(table, Table)

    # fixtures -------------------------------------------------------

    @pytest.fixture(params=[
        (0, False), (1, False), (0, True), (1, True)
    ])
    def add_paragraph_fixture(self, request):
        p_count, has_sectPr = request.param
        # body element -----------------
        body_bldr = self._body_bldr(p_count=p_count, sectPr=has_sectPr)
        body_elm = body_bldr.element
        body = _Body(body_elm)
        # expected XML -----------------
        p_count += 1
        body_bldr = self._body_bldr(p_count=p_count, sectPr=has_sectPr)
        expected_xml = body_bldr.xml()
        return body, expected_xml

    @pytest.fixture(params=[(0, False), (0, True), (1, False), (1, True)])
    def add_table_fixture(self, request):
        p_count, has_sectPr = request.param
        body_bldr = self._body_bldr(p_count=p_count, sectPr=has_sectPr)
        body = _Body(body_bldr.element)

        tbl_bldr = self._tbl_bldr()
        body_bldr = self._body_bldr(
            p_count=p_count, tbl_bldr=tbl_bldr, sectPr=has_sectPr
        )
        expected_xml = body_bldr.xml()

        return body, expected_xml

    @pytest.fixture
    def body_with_paragraphs(self):
        body_elm = (
            a_body().with_nsdecls()
                    .with_child(a_p())
                    .with_child(a_p())
                    .element
        )
        return _Body(body_elm)

    @pytest.fixture
    def body_with_tables(self):
        body_elm = (
            a_body().with_nsdecls()
                    .with_child(a_tbl())
                    .with_child(a_tbl())
                    .element
        )
        return _Body(body_elm)

    @pytest.fixture(params=[False, True])
    def clear_content_fixture(self, request):
        has_sectPr = request.param
        # body element -----------------
        body_bldr = a_body().with_nsdecls()
        body_bldr.with_child(a_p())
        if has_sectPr:
            body_bldr.with_child(a_sectPr())
        body_elm = body_bldr.element
        body = _Body(body_elm)
        # expected XML -----------------
        body_bldr = a_body().with_nsdecls()
        if has_sectPr:
            body_bldr.with_child(a_sectPr())
        expected_xml = body_bldr.xml()
        return body, expected_xml

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
        tblPr_bldr = a_tblPr()

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
        inline_shapes, inline_shape_count = inline_shapes_fixture
        assert len(inline_shapes) == inline_shape_count

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
         r_, image_part_, rId_, shape_id_, new_picture_shape_
         ) = add_picture_fixture
        # exercise ---------------------
        picture_shape = inline_shapes.add_picture(image_descriptor_)
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
        return (
            inline_shapes, image_descriptor_, document_, InlineShape_, r_,
            image_part_, rId_, shape_id_, new_picture_shape_
        )

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
    def inline_shapes_fixture(self):
        inline_shape_count = 2
        body = (
            a_body().with_nsdecls('w', 'wp').with_child(
                a_p().with_child(
                    an_r().with_child(
                        a_drawing().with_child(
                            an_inline()))).with_child(
                    an_r().with_child(
                        a_drawing().with_child(
                            an_inline())
                    )
                )
            )
        ).element
        inline_shapes = InlineShapes(body, None)
        return inline_shapes, inline_shape_count

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
