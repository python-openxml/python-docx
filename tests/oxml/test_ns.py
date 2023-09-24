# encoding: utf-8

"""
Test suite for docx.oxml.ns
"""

from __future__ import absolute_import, print_function, unicode_literals

import pytest

from docx.oxml.ns import NamespacePrefixedTag


class DescribeNamespacePrefixedTag(object):
    def it_behaves_like_a_string_when_you_want_it_to(self, nsptag):
        s = "- %s -" % nsptag
        assert s == "- a:foobar -"

    def it_knows_its_clark_name(self, nsptag, clark_name):
        assert nsptag.clark_name == clark_name

    def it_can_construct_from_a_clark_name(self, clark_name, nsptag):
        _nsptag = NamespacePrefixedTag.from_clark_name(clark_name)
        assert _nsptag == nsptag

    def it_knows_its_local_part(self, nsptag, local_part):
        assert nsptag.local_part == local_part

    def it_can_compose_a_single_entry_nsmap_for_itself(self, nsptag, namespace_uri_a):
        expected_nsmap = {"a": namespace_uri_a}
        assert nsptag.nsmap == expected_nsmap

    def it_knows_its_namespace_prefix(self, nsptag):
        assert nsptag.nspfx == "a"

    def it_knows_its_namespace_uri(self, nsptag, namespace_uri_a):
        assert nsptag.nsuri == namespace_uri_a

    # fixtures -------------------------------------------------------

    @pytest.fixture
    def clark_name(self, namespace_uri_a, local_part):
        return "{%s}%s" % (namespace_uri_a, local_part)

    @pytest.fixture
    def local_part(self):
        return "foobar"

    @pytest.fixture
    def namespace_uri_a(self):
        return "http://schemas.openxmlformats.org/drawingml/2006/main"

    @pytest.fixture
    def nsptag(self, nsptag_str):
        return NamespacePrefixedTag(nsptag_str)

    @pytest.fixture
    def nsptag_str(self, local_part):
        return "a:%s" % local_part
