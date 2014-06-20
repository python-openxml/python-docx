# encoding: utf-8

"""
Test data builders for section-related XML elements
"""

from ...unitdata import BaseBuilder


class CT_SectPrBuilder(BaseBuilder):
    __tag__ = 'w:sectPr'
    __nspfxs__ = ('w',)
    __attrs__ = ()


class CT_SectTypeBuilder(BaseBuilder):
    __tag__ = 'w:type'
    __nspfxs__ = ('w',)
    __attrs__ = ('w:val',)


def a_sectPr():
    return CT_SectPrBuilder()


def a_type():
    return CT_SectTypeBuilder()
