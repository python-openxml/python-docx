# encoding: utf-8

"""
Test suite for the docx.header module
"""

from __future__ import (
    absolute_import, print_function, unicode_literals, division
)

import pytest

from docx.enum.header import WD_HEADER_FOOTER
from docx.header import Header

from .unitutil.cxml import element


class Describe_BaseHeaderFooter(object):

    def it_knows_whether_it_is_linked_to_previous(self, is_linked_fixture):
        header, expected_value = is_linked_fixture
        assert header.is_linked_to_previous is expected_value

    # fixtures -------------------------------------------------------

    @pytest.fixture(params=[
        ('w:sectPr',                                   True),
        ('w:sectPr/w:headerReference{w:type=default}', False),
        ('w:sectPr/w:headerReference{w:type=even}',    True),
    ])
    def is_linked_fixture(self, request):
        sectPr_cxml, expected_value = request.param
        header = Header(element(sectPr_cxml), None, WD_HEADER_FOOTER.PRIMARY)
        return header, expected_value
