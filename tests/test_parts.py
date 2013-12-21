# encoding: utf-8

"""
Test suite for the docx.parts module
"""

from __future__ import absolute_import, print_function, unicode_literals

from docx.parts import _Body, _Document

import pytest

from mock import Mock

from docx.text import Paragraph

from .oxml.unitdata.parts import a_body
from .oxml.unitdata.text import a_p, a_sectPr
from .unitutil import class_mock, function_mock, initializer_mock


class Describe_Document(object):

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
        doc = _Document.load(partname, content_type, blob, package)
        # verify -----------------------
        oxml_fromstring_.assert_called_once_with(blob)
        init.assert_called_once_with(
            partname, content_type, document_elm, package
        )
        assert isinstance(doc, _Document)

    def it_has_a_body(self, init, _Body_):
        # mockery ----------------------
        doc = _Document(None, None, None)
        doc._element = Mock(name='_element')
        # exercise ---------------------
        body = doc.body
        # verify -----------------------
        _Body_.assert_called_once_with(doc._element.body)
        assert body is _Body_.return_value

    def it_can_serialize_to_xml(self, init, serialize_part_xml_):
        # mockery ----------------------
        doc = _Document(None, None, None)
        doc._element = Mock(name='_element')
        # exercise ---------------------
        doc.blob
        # verify -----------------------
        serialize_part_xml_.assert_called_once_with(doc._element)

    # fixtures -------------------------------------------------------

    @pytest.fixture
    def _Body_(self, request):
        return class_mock(request, 'docx.parts._Body')

    @pytest.fixture
    def init(self, request):
        return initializer_mock(request, _Document)

    @pytest.fixture
    def oxml_fromstring_(self, request):
        return function_mock(request, 'docx.parts.oxml_fromstring')

    @pytest.fixture
    def serialize_part_xml_(self, request):
        return function_mock(request, 'docx.parts.serialize_part_xml')


class Describe_Body(object):

    def it_can_add_a_paragraph_to_itself(self, add_paragraph_fixture):
        body, expected_xml = add_paragraph_fixture
        p = body.add_paragraph()
        assert body._body.xml == expected_xml
        assert isinstance(p, Paragraph)

    def it_can_clear_itself_of_all_content_it_holds(self):
        # mockery ----------------------
        body_elm = Mock(name='body_elm')
        body = _Body(body_elm)
        # exercise ---------------------
        retval = body.clear_content()
        # verify -----------------------
        body_elm.clear_content.assert_called_once_with()
        assert retval is body

    def it_provides_access_to_the_paragraphs_it_contains(
            self, body_with_paragraphs):
        body = body_with_paragraphs
        paragraphs = body.paragraphs
        assert len(paragraphs) == 2
        for p in paragraphs:
            assert isinstance(p, Paragraph)

    # fixtures -------------------------------------------------------

    @pytest.fixture(params=[
        (False, False), (True, False), (False, True), (True, True)
    ])
    def add_paragraph_fixture(self, request):
        has_p, has_sectPr = request.param
        # body element -----------------
        body_bldr = a_body().with_nsdecls()
        if has_p:
            body_bldr.with_child(a_p())
        if has_sectPr:
            body_bldr.with_child(a_sectPr())
        body_elm = body_bldr.element
        body = _Body(body_elm)
        # expected XML -----------------
        body_bldr = a_body().with_nsdecls()
        if has_p:
            body_bldr.with_child(a_p())
        body_bldr.with_child(a_p())
        if has_sectPr:
            body_bldr.with_child(a_sectPr())
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
