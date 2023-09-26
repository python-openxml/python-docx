"""Test data builders for styles part XML elements."""

from ...unitdata import BaseBuilder


class CT_StyleBuilder(BaseBuilder):
    __tag__ = "w:style"
    __nspfxs__ = ("w",)
    __attrs__ = ("w:type", "w:styleId", "w:default", "w:customStyle")


class CT_StylesBuilder(BaseBuilder):
    __tag__ = "w:styles"
    __nspfxs__ = ("w",)
    __attrs__ = ()


def a_style():
    return CT_StyleBuilder()


def a_styles():
    return CT_StylesBuilder()
