# encoding: utf-8

"""
Test suite for the docx.document module
"""

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

import pytest

from docx.document import _Body, Document

from .unitutil.cxml import element
from .unitutil.mock import class_mock, instance_mock


class DescribeDocument(object):

    def it_provides_access_to_the_document_body(self, body_fixture):
        document, body_elm, _Body_, body_ = body_fixture
        body = document._body
        _Body_.assert_called_once_with(body_elm, document)
        assert body is body_

    # fixtures -------------------------------------------------------

    @pytest.fixture
    def body_fixture(self, _Body_, body_):
        document_elm = element('w:document/w:body')
        body_elm = document_elm[0]
        document = Document(document_elm, None)
        return document, body_elm, _Body_, body_

    # fixture components ---------------------------------------------

    @pytest.fixture
    def _Body_(self, request, body_):
        return class_mock(request, 'docx.document._Body', return_value=body_)

    @pytest.fixture
    def body_(self, request):
        return instance_mock(request, _Body)
