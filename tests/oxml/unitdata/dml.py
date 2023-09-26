"""Test data builders for DrawingML XML elements."""

from ...unitdata import BaseBuilder


class CT_BlipBuilder(BaseBuilder):
    __tag__ = "a:blip"
    __nspfxs__ = ("a",)
    __attrs__ = ("r:embed", "r:link", "cstate")


class CT_BlipFillPropertiesBuilder(BaseBuilder):
    __tag__ = "pic:blipFill"
    __nspfxs__ = ("pic",)
    __attrs__ = ()


class CT_GraphicalObjectBuilder(BaseBuilder):
    __tag__ = "a:graphic"
    __nspfxs__ = ("a",)
    __attrs__ = ()


class CT_GraphicalObjectDataBuilder(BaseBuilder):
    __tag__ = "a:graphicData"
    __nspfxs__ = ("a",)
    __attrs__ = ("uri",)


class CT_InlineBuilder(BaseBuilder):
    __tag__ = "wp:inline"
    __nspfxs__ = ("wp",)
    __attrs__ = ("distT", "distB", "distL", "distR")


class CT_PictureBuilder(BaseBuilder):
    __tag__ = "pic:pic"
    __nspfxs__ = ("pic",)
    __attrs__ = ()


def a_blip():
    return CT_BlipBuilder()


def a_blipFill():
    return CT_BlipFillPropertiesBuilder()


def a_graphic():
    return CT_GraphicalObjectBuilder()


def a_graphicData():
    return CT_GraphicalObjectDataBuilder()


def a_pic():
    return CT_PictureBuilder()


def an_inline():
    return CT_InlineBuilder()
