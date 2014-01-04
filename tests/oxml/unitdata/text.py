# encoding: utf-8

"""
Test data builders for text XML elements
"""

from ...unitdata import BaseBuilder
from .shared import CT_OnOffBuilder, CT_StringBuilder


class CT_BrBuilder(BaseBuilder):
    __tag__ = 'w:br'
    __nspfxs__ = ('w',)
    __attrs__ = ('w:type', 'w:clear')


class CT_PBuilder(BaseBuilder):
    __tag__ = 'w:p'
    __nspfxs__ = ('w',)
    __attrs__ = ()


class CT_PPrBuilder(BaseBuilder):
    __tag__ = 'w:pPr'
    __nspfxs__ = ('w',)
    __attrs__ = ()


class CT_RBuilder(BaseBuilder):
    __tag__ = 'w:r'
    __nspfxs__ = ('w',)
    __attrs__ = ()


class CT_RPrBuilder(BaseBuilder):
    __tag__ = 'w:rPr'
    __nspfxs__ = ('w',)
    __attrs__ = ()


class CT_SectPrBuilder(BaseBuilder):
    __tag__ = 'w:sectPr'
    __nspfxs__ = ('w',)
    __attrs__ = ()


class CT_TextBuilder(BaseBuilder):
    __tag__ = 'w:t'
    __nspfxs__ = ('w',)
    __attrs__ = ()


def a_b():
    return CT_OnOffBuilder('w:b')


def a_br():
    return CT_BrBuilder()


def a_p():
    return CT_PBuilder()


def a_pPr():
    return CT_PPrBuilder()


def a_pStyle():
    return CT_StringBuilder('w:pStyle')


def a_sectPr():
    return CT_SectPrBuilder()


def a_t():
    return CT_TextBuilder()


def an_r():
    return CT_RBuilder()


def an_rPr():
    return CT_RPrBuilder()
