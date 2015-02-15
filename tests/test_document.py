# encoding: utf-8

"""
Test suite for the docx.document module
"""

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

import pytest

from docx.document import _Body, Document
from docx.parts.document import DocumentPart
from docx.text.paragraph import Paragraph

from .unitutil.cxml import element
from .unitutil.mock import class_mock, instance_mock, property_mock


class DescribeDocument(object):

    def it_can_add_a_paragraph(self, add_paragraph_fixture):
        document, text, style, paragraph_ = add_paragraph_fixture
        paragraph = document.add_paragraph(text, style)
        document._body.add_paragraph.assert_called_once_with(text, style)
        assert paragraph is paragraph_

    def it_provides_access_to_the_document_part(self, part_fixture):
        document, part_ = part_fixture
        assert document.part is part_

    def it_provides_access_to_the_document_body(self, body_fixture):
        document, body_elm, _Body_, body_ = body_fixture
        body = document._body
        _Body_.assert_called_once_with(body_elm, document)
        assert body is body_

    # fixtures -------------------------------------------------------

    @pytest.fixture(params=[
        ('',         None),
        ('',         'Heading 1'),
        ('foo\rbar', 'Body Text'),
    ])
    def add_paragraph_fixture(self, request, body_prop_, paragraph_):
        text, style = request.param
        document = Document(None, None)
        body_prop_.return_value.add_paragraph.return_value = paragraph_
        return document, text, style, paragraph_

    @pytest.fixture
    def body_fixture(self, _Body_, body_):
        document_elm = element('w:document/w:body')
        body_elm = document_elm[0]
        document = Document(document_elm, None)
        return document, body_elm, _Body_, body_

    @pytest.fixture
    def part_fixture(self, document_part_):
        document = Document(None, document_part_)
        return document, document_part_

    # fixture components ---------------------------------------------

    @pytest.fixture
    def _Body_(self, request, body_):
        return class_mock(request, 'docx.document._Body', return_value=body_)

    @pytest.fixture
    def body_(self, request):
        return instance_mock(request, _Body)

    @pytest.fixture
    def body_prop_(self, request):
        return property_mock(request, Document, '_body')

    @pytest.fixture
    def document_part_(self, request):
        return instance_mock(request, DocumentPart)

    @pytest.fixture
    def paragraph_(self, request):
        return instance_mock(request, Paragraph)
