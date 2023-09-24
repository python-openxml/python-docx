# encoding: utf-8

"""
Test data builders for numbering part XML elements
"""

from ...unitdata import BaseBuilder


class CT_NumBuilder(BaseBuilder):
    __tag__ = "w:num"
    __nspfxs__ = ("w",)
    __attrs__ = "w:numId"


class CT_NumberingBuilder(BaseBuilder):
    __tag__ = "w:numbering"
    __nspfxs__ = ("w",)
    __attrs__ = ()


def a_num():
    return CT_NumBuilder()


def a_numbering():
    return CT_NumberingBuilder()
