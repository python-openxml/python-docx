# encoding: utf-8

"""
Test data builders shared by more than one other module
"""

from ...unitdata import BaseBuilder


class CT_OnOffBuilder(BaseBuilder):
    __nspfxs__ = ("w",)
    __attrs__ = "w:val"

    def __init__(self, tag):
        self.__tag__ = tag
        super(CT_OnOffBuilder, self).__init__()

    def with_val(self, value):
        self._set_xmlattr("w:val", str(value))
        return self


class CT_StringBuilder(BaseBuilder):
    __nspfxs__ = ("w",)
    __attrs__ = ()

    def __init__(self, tag):
        self.__tag__ = tag
        super(CT_StringBuilder, self).__init__()

    def with_val(self, value):
        self._set_xmlattr("w:val", str(value))
        return self
