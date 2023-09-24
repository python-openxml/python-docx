# encoding: utf-8

"""
Test suite for the docx.opc.packuri module
"""

import pytest

from docx.opc.packuri import PackURI


class DescribePackURI(object):
    def cases(self, expected_values):
        """
        Return list of tuples zipped from uri_str cases and
        *expected_values*. Raise if lengths don't match.
        """
        uri_str_cases = [
            "/",
            "/ppt/presentation.xml",
            "/ppt/slides/slide1.xml",
        ]
        if len(expected_values) != len(uri_str_cases):
            msg = "len(expected_values) differs from len(uri_str_cases)"
            raise AssertionError(msg)
        pack_uris = [PackURI(uri_str) for uri_str in uri_str_cases]
        return zip(pack_uris, expected_values)

    def it_can_construct_from_relative_ref(self):
        baseURI = "/ppt/slides"
        relative_ref = "../slideLayouts/slideLayout1.xml"
        pack_uri = PackURI.from_rel_ref(baseURI, relative_ref)
        assert pack_uri == "/ppt/slideLayouts/slideLayout1.xml"

    def it_should_raise_on_construct_with_bad_pack_uri_str(self):
        with pytest.raises(ValueError):
            PackURI("foobar")

    def it_can_calculate_baseURI(self):
        expected_values = ("/", "/ppt", "/ppt/slides")
        for pack_uri, expected_baseURI in self.cases(expected_values):
            assert pack_uri.baseURI == expected_baseURI

    def it_can_calculate_extension(self):
        expected_values = ("", "xml", "xml")
        for pack_uri, expected_ext in self.cases(expected_values):
            assert pack_uri.ext == expected_ext

    def it_can_calculate_filename(self):
        expected_values = ("", "presentation.xml", "slide1.xml")
        for pack_uri, expected_filename in self.cases(expected_values):
            assert pack_uri.filename == expected_filename

    def it_knows_the_filename_index(self):
        expected_values = (None, None, 1)
        for pack_uri, expected_idx in self.cases(expected_values):
            assert pack_uri.idx == expected_idx

    def it_can_calculate_membername(self):
        expected_values = (
            "",
            "ppt/presentation.xml",
            "ppt/slides/slide1.xml",
        )
        for pack_uri, expected_membername in self.cases(expected_values):
            assert pack_uri.membername == expected_membername

    def it_can_calculate_relative_ref_value(self):
        cases = (
            ("/", "/ppt/presentation.xml", "ppt/presentation.xml"),
            (
                "/ppt",
                "/ppt/slideMasters/slideMaster1.xml",
                "slideMasters/slideMaster1.xml",
            ),
            (
                "/ppt/slides",
                "/ppt/slideLayouts/slideLayout1.xml",
                "../slideLayouts/slideLayout1.xml",
            ),
        )
        for baseURI, uri_str, expected_relative_ref in cases:
            pack_uri = PackURI(uri_str)
            assert pack_uri.relative_ref(baseURI) == expected_relative_ref

    def it_can_calculate_rels_uri(self):
        expected_values = (
            "/_rels/.rels",
            "/ppt/_rels/presentation.xml.rels",
            "/ppt/slides/_rels/slide1.xml.rels",
        )
        for pack_uri, expected_rels_uri in self.cases(expected_values):
            assert pack_uri.rels_uri == expected_rels_uri
