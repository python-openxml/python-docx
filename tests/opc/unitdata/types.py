# encoding: utf-8

"""
XML test data builders for [Content_Types].xml elements
"""

from __future__ import absolute_import, print_function, unicode_literals

from docx.opc.oxml import nsmap

from ...unitdata import BaseBuilder


class CT_DefaultBuilder(BaseBuilder):
    __tag__ = 'Default'
    __nspfxs__ = ('ct',)
    __attrs__ = ('Extension', 'ContentType')


class CT_OverrideBuilder(BaseBuilder):
    __tag__ = 'Override'
    __nspfxs__ = ('ct',)
    __attrs__ = ('PartName', 'ContentType')


class CT_TypesBuilder(BaseBuilder):
    __tag__ = 'Types'
    __nspfxs__ = ('ct',)
    __attrs__ = ()

    def with_nsdecls(self, *nspfxs):
        self._nsdecls = ' xmlns="%s"' % nsmap['ct']
        return self


def a_Default():
    return CT_DefaultBuilder()


def a_Types():
    return CT_TypesBuilder()


def an_Override():
    return CT_OverrideBuilder()
