"""Test suite for the docx.api module."""

import pytest

from docx.api import Document as DocumentFactoryFn
from docx.document import Document as DocumentCls
from docx.opc.constants import CONTENT_TYPE as CT

from .unitutil.mock import FixtureRequest, Mock, class_mock, function_mock, instance_mock


class DescribeDocument:
    """Unit-test suite for `docx.api.Document` factory function."""

    def it_opens_a_docx_file(self, Package_: Mock, document_: Mock):
        document_part = Package_.open.return_value.main_document_part
        document_part.document = document_
        document_part.content_type = CT.WML_DOCUMENT_MAIN

        document = DocumentFactoryFn("foobar.docx")

        Package_.open.assert_called_once_with("foobar.docx")
        assert document is document_

    def it_opens_the_default_docx_if_none_specified(
        self, _default_docx_path_: Mock, Package_: Mock, document_: Mock
    ):
        _default_docx_path_.return_value = "default-document.docx"
        document_part = Package_.open.return_value.main_document_part
        document_part.document = document_
        document_part.content_type = CT.WML_DOCUMENT_MAIN

        document = DocumentFactoryFn()

        Package_.open.assert_called_once_with("default-document.docx")
        assert document is document_

    def it_raises_on_not_a_Word_file(self, Package_: Mock):
        Package_.open.return_value.main_document_part.content_type = "BOGUS"

        with pytest.raises(ValueError, match="file 'foobar.xlsx' is not a Word file,"):
            DocumentFactoryFn("foobar.xlsx")

    # -- fixtures --------------------------------------------------------------------------------

    @pytest.fixture
    def _default_docx_path_(self, request: FixtureRequest):
        return function_mock(request, "docx.api._default_docx_path")

    @pytest.fixture
    def document_(self, request: FixtureRequest):
        return instance_mock(request, DocumentCls)

    @pytest.fixture
    def Package_(self, request: FixtureRequest):
        return class_mock(request, "docx.api.Package")
