# -*- coding: utf-8 -*-
#
# test_parts.py
#
# Copyright (C) 2013 Steve Canny scanny@cisco.com
#
# This module is part of python-docx and is released under the MIT License:
# http://www.opensource.org/licenses/mit-license.php

"""Test suite for the docx.parts module."""

from docx.parts import _Document

import pytest

from mock import Mock

from .unitutil import class_mock, function_mock, initializer_mock


class Describe_Document(object):

    @pytest.fixture
    def _Body_(self, request):
        return class_mock('docx.parts._Body', request)

    @pytest.fixture
    def init(self, request):
        return initializer_mock(_Document, request)

    @pytest.fixture
    def oxml_fromstring_(self, request):
        return function_mock('docx.parts.oxml_fromstring', request)

    def it_can_be_constructed_by_opc_part_factory(
            self, oxml_fromstring_, init):
        # mockery ----------------------
        partname, content_type, blob, document_elm = (
            Mock(name='partname'), Mock(name='content_type'),
            Mock(name='blob'), Mock(name='document_elm')
        )
        oxml_fromstring_.return_value = document_elm
        # exercise ---------------------
        doc = _Document.load(partname, content_type, blob)
        # verify -----------------------
        oxml_fromstring_.assert_called_once_with(blob)
        init.assert_called_once_with(partname, content_type, document_elm)
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
