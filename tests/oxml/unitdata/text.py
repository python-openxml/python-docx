# encoding: utf-8

"""
Test data builders for text XML elements
"""

from ...unitdata import BaseBuilder


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


class CT_SectPrBuilder(BaseBuilder):
    __tag__ = 'w:sectPr'
    __nspfxs__ = ('w',)
    __attrs__ = ()


class CT_StringBuilder(BaseBuilder):
    __tag__ = 'w:pStyle'
    __nspfxs__ = ('w',)
    __attrs__ = ()

    def with_val(self, value):
        self._set_xmlattr('w:val', str(value))
        return self


class CT_TextBuilder(BaseBuilder):
    __tag__ = 'w:t'
    __nspfxs__ = ('w',)
    __attrs__ = ()


def a_p():
    return CT_PBuilder()


def a_pPr():
    return CT_PPrBuilder()


def a_pStyle():
    return CT_StringBuilder()


def a_sectPr():
    return CT_SectPrBuilder()


def a_t():
    return CT_TextBuilder()


def an_r():
    return CT_RBuilder()
