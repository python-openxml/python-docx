# encoding: utf-8

"""
Test suite for the docx.table module
"""

from __future__ import absolute_import, print_function, unicode_literals

import pytest

from docx.table import _Column, _Row, _RowCollection, Table

from .oxml.unitdata.table import a_gridCol, a_tbl, a_tblGrid, a_tc, a_tr
from .oxml.unitdata.text import a_p


class DescribeTable(object):

    def it_provides_access_to_the_table_rows(self, row_access_fixture):
        table = row_access_fixture
        rows = table.rows
        assert isinstance(rows, _RowCollection)

    def it_can_add_a_column(self, add_column_fixture):
        table, expected_xml = add_column_fixture
        col = table.add_column()
        assert table._tbl.xml == expected_xml
        assert isinstance(col, _Column)

    def it_can_add_a_row(self, add_row_fixture):
        table, expected_xml = add_row_fixture
        row = table.add_row()
        assert table._tbl.xml == expected_xml
        assert isinstance(row, _Row)

    # fixtures -------------------------------------------------------

    @pytest.fixture
    def add_column_fixture(self):
        tbl = _tbl_bldr(2, 1).element
        table = Table(tbl)
        expected_xml = _tbl_bldr(2, 2).xml()
        return table, expected_xml

    @pytest.fixture
    def add_row_fixture(self):
        tbl = _tbl_bldr(rows=1, cols=2).element
        table = Table(tbl)
        expected_xml = _tbl_bldr(rows=2, cols=2).xml()
        return table, expected_xml

    @pytest.fixture
    def row_access_fixture(self):
        tbl = _tbl_bldr(rows=2, cols=2).element
        table = Table(tbl)
        return table


# fixtures -----------------------------------------------------------

def _tbl_bldr(rows, cols):
    tblGrid_bldr = a_tblGrid()
    for i in range(cols):
        tblGrid_bldr.with_child(a_gridCol())
    tbl_bldr = a_tbl().with_nsdecls().with_child(tblGrid_bldr)
    for i in range(rows):
        tr_bldr = _tr_bldr(cols)
        tbl_bldr.with_child(tr_bldr)
    return tbl_bldr


def _tc_bldr():
    return a_tc().with_child(a_p())


def _tr_bldr(cols):
    tr_bldr = a_tr()
    for i in range(cols):
        tc_bldr = _tc_bldr()
        tr_bldr.with_child(tc_bldr)
    return tr_bldr
