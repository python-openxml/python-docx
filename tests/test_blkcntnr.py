# encoding: utf-8

"""
Test suite for the docx.blkcntnr (block item container) module
"""

from __future__ import absolute_import, print_function, unicode_literals

import pytest

from docx.blkcntnr import BlockItemContainer
from docx.table import Table
from docx.text import Paragraph

from .unitutil.cxml import element, xml


class DescribeBlockItemContainer(object):

    def it_can_add_a_paragraph(self, add_paragraph_fixture):
        blkcntnr, text, style, expected_xml = add_paragraph_fixture
        paragraph = blkcntnr.add_paragraph(text, style)
        assert blkcntnr._element.xml == expected_xml
        assert isinstance(paragraph, Paragraph)

    def it_can_add_a_table(self, add_table_fixture):
        blkcntnr, rows, cols, expected_xml = add_table_fixture
        table = blkcntnr.add_table(rows, cols)
        assert blkcntnr._element.xml == expected_xml
        assert isinstance(table, Table)

    # fixtures -------------------------------------------------------

    @pytest.fixture(params=[
        ('w:body', '', None,
         'w:body/w:p'),
        ('w:body', 'foobar', None,
         'w:body/w:p/w:r/w:t"foobar"'),
        ('w:body', '', 'Heading1',
         'w:body/w:p/w:pPr/w:pStyle{w:val=Heading1}'),
        ('w:body', 'barfoo', 'BodyText',
         'w:body/w:p/(w:pPr/w:pStyle{w:val=BodyText},w:r/w:t"barfoo")'),
    ])
    def add_paragraph_fixture(self, request):
        blkcntnr_cxml, text, style, after_cxml = request.param
        blkcntnr = BlockItemContainer(element(blkcntnr_cxml), None)
        expected_xml = xml(after_cxml)
        return blkcntnr, text, style, expected_xml

    @pytest.fixture(params=[
        ('w:body', 0, 0, 'w:body/w:tbl/(w:tblPr/w:tblW{w:type=auto,w:w=0},w:'
         'tblGrid)'),
        ('w:body', 1, 0, 'w:body/w:tbl/(w:tblPr/w:tblW{w:type=auto,w:w=0},w:'
         'tblGrid,w:tr)'),
        ('w:body', 0, 1, 'w:body/w:tbl/(w:tblPr/w:tblW{w:type=auto,w:w=0},w:'
         'tblGrid/w:gridCol)'),
        ('w:body', 1, 1, 'w:body/w:tbl/(w:tblPr/w:tblW{w:type=auto,w:w=0},w:'
         'tblGrid/w:gridCol,w:tr/w:tc/w:p)'),
    ])
    def add_table_fixture(self, request):
        blkcntnr_cxml, rows, cols, after_cxml = request.param
        blkcntnr = BlockItemContainer(element(blkcntnr_cxml), None)
        expected_xml = xml(after_cxml)
        return blkcntnr, rows, cols, expected_xml
