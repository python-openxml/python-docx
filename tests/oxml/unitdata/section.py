"""Test data builders for section-related XML elements."""

from ...unitdata import BaseBuilder


class CT_PageMarBuilder(BaseBuilder):
    __tag__ = "w:pgMar"
    __nspfxs__ = ("w",)
    __attrs__ = (
        "w:top",
        "w:right",
        "w:bottom",
        "w:left",
        "w:header",
        "w:footer",
        "w:gutter",
    )


class CT_PageSzBuilder(BaseBuilder):
    __tag__ = "w:pgSz"
    __nspfxs__ = ("w",)
    __attrs__ = ("w:w", "w:h", "w:orient", "w:code")


class CT_SectPrBuilder(BaseBuilder):
    __tag__ = "w:sectPr"
    __nspfxs__ = ("w",)
    __attrs__ = ()


class CT_SectTypeBuilder(BaseBuilder):
    __tag__ = "w:type"
    __nspfxs__ = ("w",)
    __attrs__ = ("w:val",)


def a_pgMar():
    return CT_PageMarBuilder()


def a_pgSz():
    return CT_PageSzBuilder()


def a_sectPr():
    return CT_SectPrBuilder()


def a_type():
    return CT_SectTypeBuilder()
