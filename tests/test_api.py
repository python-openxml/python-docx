# encoding: utf-8

"""
Test suite for the docx.api module
"""

from __future__ import absolute_import, division, print_function, unicode_literals

import pytest

import docx

from docx.api import Document
from docx.opc.constants import CONTENT_TYPE as CT

from .unitutil.mock import function_mock, instance_mock, class_mock


class DescribeDocument(object):
    def it_opens_a_docx_file(self, open_fixture):
        docx, Package_, document_ = open_fixture
        document = Document(docx)
        Package_.open.assert_called_once_with(docx)
        assert document is document_

    def it_opens_the_default_docx_if_none_specified(self, default_fixture):
        docx, Package_, document_ = default_fixture
        document = Document()
        Package_.open.assert_called_once_with(docx)
        assert document is document_

    def it_raises_on_not_a_Word_file(self, raise_fixture):
        not_a_docx = raise_fixture
        with pytest.raises(ValueError):
            Document(not_a_docx)

    # fixtures -------------------------------------------------------

    @pytest.fixture
    def default_fixture(self, _default_docx_path_, Package_, document_):
        docx = "barfoo.docx"
        _default_docx_path_.return_value = docx
        document_part = Package_.open.return_value.main_document_part
        document_part.document = document_
        document_part.content_type = CT.WML_DOCUMENT_MAIN
        return docx, Package_, document_

    @pytest.fixture
    def open_fixture(self, Package_, document_):
        docx = "foobar.docx"
        document_part = Package_.open.return_value.main_document_part
        document_part.document = document_
        document_part.content_type = CT.WML_DOCUMENT_MAIN
        return docx, Package_, document_

    @pytest.fixture
    def raise_fixture(self, Package_):
        not_a_docx = "foobar.xlsx"
        Package_.open.return_value.main_document_part.content_type = "BOGUS"
        return not_a_docx

    # fixture components ---------------------------------------------

    @pytest.fixture
    def _default_docx_path_(self, request):
        return function_mock(request, "docx.api._default_docx_path")

    @pytest.fixture
    def document_(self, request):
        return instance_mock(request, docx.document.Document)

    @pytest.fixture
    def Package_(self, request):
        return class_mock(request, "docx.api.Package")
