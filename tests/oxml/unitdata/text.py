# encoding: utf-8

"""
Test data builders for text XML elements
"""

from ...unitdata import BaseBuilder
from .shared import CT_OnOffBuilder, CT_StringBuilder


class CT_BrBuilder(BaseBuilder):
    __tag__ = "w:br"
    __nspfxs__ = ("w",)
    __attrs__ = ("w:type", "w:clear")


class CT_EmptyBuilder(BaseBuilder):
    __nspfxs__ = ("w",)
    __attrs__ = ()

    def __init__(self, tag):
        self.__tag__ = tag
        super(CT_EmptyBuilder, self).__init__()


class CT_JcBuilder(BaseBuilder):
    __tag__ = "w:jc"
    __nspfxs__ = ("w",)
    __attrs__ = ("w:val",)


class CT_PBuilder(BaseBuilder):
    __tag__ = "w:p"
    __nspfxs__ = ("w",)
    __attrs__ = ()


class CT_PPrBuilder(BaseBuilder):
    __tag__ = "w:pPr"
    __nspfxs__ = ("w",)
    __attrs__ = ()


class CT_RBuilder(BaseBuilder):
    __tag__ = "w:r"
    __nspfxs__ = ("w",)
    __attrs__ = ()


class CT_RPrBuilder(BaseBuilder):
    __tag__ = "w:rPr"
    __nspfxs__ = ("w",)
    __attrs__ = ()


class CT_SectPrBuilder(BaseBuilder):
    __tag__ = "w:sectPr"
    __nspfxs__ = ("w",)
    __attrs__ = ()


class CT_TextBuilder(BaseBuilder):
    __tag__ = "w:t"
    __nspfxs__ = ("w",)
    __attrs__ = ()

    def with_space(self, value):
        self._set_xmlattr("xml:space", str(value))
        return self


class CT_UnderlineBuilder(BaseBuilder):
    __tag__ = "w:u"
    __nspfxs__ = ("w",)
    __attrs__ = ("w:val", "w:color", "w:themeColor", "w:themeTint", "w:themeShade")


def a_b():
    return CT_OnOffBuilder("w:b")


def a_bCs():
    return CT_OnOffBuilder("w:bCs")


def a_br():
    return CT_BrBuilder()


def a_caps():
    return CT_OnOffBuilder("w:caps")


def a_cr():
    return CT_EmptyBuilder("w:cr")


def a_cs():
    return CT_OnOffBuilder("w:cs")


def a_dstrike():
    return CT_OnOffBuilder("w:dstrike")


def a_jc():
    return CT_JcBuilder()


def a_noProof():
    return CT_OnOffBuilder("w:noProof")


def a_shadow():
    return CT_OnOffBuilder("w:shadow")


def a_smallCaps():
    return CT_OnOffBuilder("w:smallCaps")


def a_snapToGrid():
    return CT_OnOffBuilder("w:snapToGrid")


def a_specVanish():
    return CT_OnOffBuilder("w:specVanish")


def a_strike():
    return CT_OnOffBuilder("w:strike")


def a_tab():
    return CT_EmptyBuilder("w:tab")


def a_vanish():
    return CT_OnOffBuilder("w:vanish")


def a_webHidden():
    return CT_OnOffBuilder("w:webHidden")


def a_p():
    return CT_PBuilder()


def a_pPr():
    return CT_PPrBuilder()


def a_pStyle():
    return CT_StringBuilder("w:pStyle")


def a_sectPr():
    return CT_SectPrBuilder()


def a_t():
    return CT_TextBuilder()


def a_u():
    return CT_UnderlineBuilder()


def an_emboss():
    return CT_OnOffBuilder("w:emboss")


def an_i():
    return CT_OnOffBuilder("w:i")


def an_iCs():
    return CT_OnOffBuilder("w:iCs")


def an_imprint():
    return CT_OnOffBuilder("w:imprint")


def an_oMath():
    return CT_OnOffBuilder("w:oMath")


def an_outline():
    return CT_OnOffBuilder("w:outline")


def an_r():
    return CT_RBuilder()


def an_rPr():
    return CT_RPrBuilder()


def an_rStyle():
    return CT_StringBuilder("w:rStyle")


def an_rtl():
    return CT_OnOffBuilder("w:rtl")
