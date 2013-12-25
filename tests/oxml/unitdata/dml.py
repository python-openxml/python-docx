# encoding: utf-8

"""
Test data builders for text XML elements
"""

from ...unitdata import BaseBuilder


class CT_DrawingBuilder(BaseBuilder):
    __tag__ = 'w:drawing'
    __nspfxs__ = ('w',)
    __attrs__ = ()


def a_drawing():
    return CT_DrawingBuilder()


class CT_InlineBuilder(BaseBuilder):
    __tag__ = 'wp:inline'
    __nspfxs__ = ('wp',)
    __attrs__ = ('distT', 'distB', 'distL', 'distR')


def an_inline():
    return CT_InlineBuilder()
