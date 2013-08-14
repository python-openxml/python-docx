# -*- coding: utf-8 -*-
#
# test_api.py
#
# Copyright (C) 2013 Steve Canny scanny@cisco.com
#
# This module is part of python-docx and is released under the MIT License:
# http://www.opensource.org/licenses/mit-license.php

"""Test suite for the docx.api module."""

import pytest

from mock import Mock, PropertyMock

from docx.api import Document, _Document

from .unitutil import class_mock, var_mock


class DescribeDocument(object):

    @pytest.fixture
    def _Document_(self, request):
        return class_mock('docx.api._Document', request)

    @pytest.fixture
    def default_docx(self, request):
        return var_mock('docx.api._default_docx_path', request)

    @pytest.fixture
    def OpcPackage_(self, OpcPackage_mockery):
        return OpcPackage_mockery[0]

    @pytest.fixture
    def OpcPackage_mockery(self, request):
        OpcPackage_ = class_mock('docx.api.OpcPackage', request)
        pkg = OpcPackage_.open.return_value
        main_document = PropertyMock(name='main_document')
        type(pkg).main_document = main_document
        document_part = main_document.return_value
        return (OpcPackage_, pkg, main_document, document_part)

    def it_opens_a_docx_file_on_construction(self, OpcPackage_mockery,
                                             _Document_):
        # mockery ----------------------
        docx = Mock(name='docx')
        OpcPackage_, pkg, main_document, document_part = OpcPackage_mockery
        # exercise ---------------------
        doc = Document(docx)
        # verify -----------------------
        OpcPackage_.open.assert_called_once_with(docx)
        main_document.assert_called_once_with()
        _Document_.assert_called_once_with(pkg, document_part)
        assert isinstance(doc, _Document)

    def it_uses_default_if_no_file_provided(self, OpcPackage_, _Document_,
                                            default_docx):
        Document()
        OpcPackage_.open.assert_called_once_with(default_docx)
