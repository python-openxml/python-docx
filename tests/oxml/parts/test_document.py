# encoding: utf-8

"""
Test suite for the docx.oxml.parts module.
"""

from docx.oxml.parts.document import CT_Body
from docx.oxml.text import CT_P

from .unitdata.document import a_body, a_document
from ..unitdata.text import a_p, a_sectPr


class DescribeCT_Body(object):

    def it_can_add_a_p_to_itself(self):
        """
        Return a newly created |CT_P| element that has been added after any
        existing content.
        """
        cases = (
            (a_body().with_nsdecls(),
             a_body().with_nsdecls().with_child(a_p())),
            (a_body().with_nsdecls().with_child(a_sectPr()),
             a_body().with_nsdecls().with_child(a_p()).with_child(a_sectPr())),
        )
        for before_body_bldr, after_body_bldr in cases:
            body = before_body_bldr.element
            # exercise -----------------
            p = body.add_p()
            # verify -------------------
            assert body.xml == after_body_bldr.xml()
            assert isinstance(p, CT_P)

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


class DescribeCT_Document(object):

    def it_holds_a_body_element(self):
        document = a_document().with_nsdecls().with_child(a_body()).element
        assert isinstance(document.body, CT_Body)
