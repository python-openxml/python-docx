# encoding: utf-8

"""
Test suite for the docx.oxml.parts module.
"""

from __future__ import absolute_import, print_function, unicode_literals

import pytest

from .unitdata.document import a_body
from ..unitdata.section import a_type
from ..unitdata.text import a_p, a_pPr, a_sectPr


class DescribeCT_Body(object):

    def it_can_clear_all_the_content_it_holds(self):
        """
        Remove all content child elements from this <w:body> element.
        """
        cases = (
            (a_body().with_nsdecls(),
             a_body().with_nsdecls()),
            (a_body().with_nsdecls().with_child(a_p()),
             a_body().with_nsdecls()),
            (a_body().with_nsdecls().with_child(a_sectPr()),
             a_body().with_nsdecls().with_child(a_sectPr())),
            (a_body().with_nsdecls().with_child(a_p()).with_child(a_sectPr()),
             a_body().with_nsdecls().with_child(a_sectPr())),
        )
        for before_body_bldr, after_body_bldr in cases:
            body = before_body_bldr.element
            # exercise -----------------
            body.clear_content()
            # verify -------------------
            assert body.xml == after_body_bldr.xml()

    def it_can_add_a_section_break(self, section_break_fixture):
        body, expected_xml = section_break_fixture
        sectPr = body.add_section_break()
        assert body.xml == expected_xml
        assert sectPr is body.get_or_add_sectPr()

    # fixtures -------------------------------------------------------

    @pytest.fixture
    def section_break_fixture(self):
        body = (
            a_body().with_nsdecls().with_child(
                a_sectPr().with_child(
                    a_type().with_val('foobar')))
        ).element
        expected_xml = (
            a_body().with_nsdecls().with_child(
                a_p().with_child(
                    a_pPr().with_child(
                        a_sectPr().with_child(
                            a_type().with_val('foobar'))))).with_child(
                a_sectPr().with_child(
                    a_type().with_val('foobar')))
        ).xml()
        return body, expected_xml
