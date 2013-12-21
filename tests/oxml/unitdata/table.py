# encoding: utf-8

"""
Test data builders for text XML elements
"""

from ...unitdata import BaseBuilder


class CT_TblBuilder(BaseBuilder):
    __tag__ = 'w:tbl'
    __nspfxs__ = ('w',)
    __attrs__ = ()


def a_tbl():
    return CT_TblBuilder()
