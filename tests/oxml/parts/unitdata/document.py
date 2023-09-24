# encoding: utf-8

"""
Test data builders for parts XML.
"""

from ....unitdata import BaseBuilder


class CT_BodyBuilder(BaseBuilder):
    __tag__ = "w:body"
    __nspfxs__ = ("w",)
    __attrs__ = ()


class CT_DocumentBuilder(BaseBuilder):
    __tag__ = "w:document"
    __nspfxs__ = ("w",)
    __attrs__ = ()


def a_body():
    return CT_BodyBuilder()


def a_document():
    return CT_DocumentBuilder()
