# encoding: utf-8

"""
Test data builders for DrawingML XML elements
"""

from ...unitdata import BaseBuilder


class CT_BlipBuilder(BaseBuilder):
    __tag__ = 'a:blip'
    __nspfxs__ = ('a',)
    __attrs__ = ('r:embed', 'r:link', 'cstate')


class CT_BlipFillPropertiesBuilder(BaseBuilder):
    __tag__ = 'pic:blipFill'
    __nspfxs__ = ('pic',)
    __attrs__ = ()


class CT_DrawingBuilder(BaseBuilder):
    __tag__ = 'w:drawing'
    __nspfxs__ = ('w',)
    __attrs__ = ()


class CT_GraphicalObjectBuilder(BaseBuilder):
    __tag__ = 'a:graphic'
    __nspfxs__ = ('a',)
    __attrs__ = ()


class CT_GraphicalObjectDataBuilder(BaseBuilder):
    __tag__ = 'a:graphicData'
    __nspfxs__ = ('a',)
    __attrs__ = ('uri',)


class CT_GraphicalObjectFrameLockingBuilder(BaseBuilder):
    __tag__ = 'a:graphicFrameLocks'
    __nspfxs__ = ('a',)
    __attrs__ = ('noChangeAspect',)


class CT_InlineBuilder(BaseBuilder):
    __tag__ = 'wp:inline'
    __nspfxs__ = ('wp',)
    __attrs__ = ('distT', 'distB', 'distL', 'distR')


class CT_NonVisualDrawingPropsBuilder(BaseBuilder):
    __nspfxs__ = ('wp',)
    __attrs__ = ('id', 'name', 'descr', 'hidden', 'title')

    def __init__(self, tag):
        self.__tag__ = tag
        super(CT_NonVisualDrawingPropsBuilder, self).__init__()


class CT_NonVisualGraphicFramePropertiesBuilder(BaseBuilder):
    __tag__ = 'wp:cNvGraphicFramePr'
    __nspfxs__ = ('wp',)
    __attrs__ = ()


class CT_NonVisualPicturePropertiesBuilder(BaseBuilder):
    __tag__ = 'pic:cNvPicPr'
    __nspfxs__ = ('pic',)
    __attrs__ = ('preferRelativeResize')


class CT_PictureBuilder(BaseBuilder):
    __tag__ = 'pic:pic'
    __nspfxs__ = ('pic',)
    __attrs__ = ()


class CT_PictureNonVisualBuilder(BaseBuilder):
    __tag__ = 'pic:nvPicPr'
    __nspfxs__ = ('pic',)
    __attrs__ = ()


class CT_Point2DBuilder(BaseBuilder):
    __tag__ = 'a:off'
    __nspfxs__ = ('a',)
    __attrs__ = ('x', 'y')


class CT_PositiveSize2DBuilder(BaseBuilder):
    __nspfxs__ = ()
    __attrs__ = ('cx', 'cy')

    def __init__(self, tag):
        self.__tag__ = tag
        super(CT_PositiveSize2DBuilder, self).__init__()


class CT_PresetGeometry2DBuilder(BaseBuilder):
    __tag__ = 'a:prstGeom'
    __nspfxs__ = ('a',)
    __attrs__ = ('prst',)


class CT_RelativeRectBuilder(BaseBuilder):
    __tag__ = 'a:fillRect'
    __nspfxs__ = ('a',)
    __attrs__ = ('l', 't', 'r', 'b')


class CT_ShapePropertiesBuilder(BaseBuilder):
    __tag__ = 'pic:spPr'
    __nspfxs__ = ('pic', 'a')
    __attrs__ = ('bwMode',)


class CT_StretchInfoPropertiesBuilder(BaseBuilder):
    __tag__ = 'a:stretch'
    __nspfxs__ = ('a',)
    __attrs__ = ()


class CT_Transform2DBuilder(BaseBuilder):
    __tag__ = 'a:xfrm'
    __nspfxs__ = ('a',)
    __attrs__ = ('rot', 'flipH', 'flipV')


def a_blip():
    return CT_BlipBuilder()


def a_blipFill():
    return CT_BlipFillPropertiesBuilder()


def a_cNvGraphicFramePr():
    return CT_NonVisualGraphicFramePropertiesBuilder()


def a_cNvPicPr():
    return CT_NonVisualPicturePropertiesBuilder()


def a_cNvPr():
    return CT_NonVisualDrawingPropsBuilder('pic:cNvPr')


def a_docPr():
    return CT_NonVisualDrawingPropsBuilder('wp:docPr')


def a_drawing():
    return CT_DrawingBuilder()


def a_fillRect():
    return CT_RelativeRectBuilder()


def a_graphic():
    return CT_GraphicalObjectBuilder()


def a_graphicData():
    return CT_GraphicalObjectDataBuilder()


def a_graphicFrameLocks():
    return CT_GraphicalObjectFrameLockingBuilder()


def a_pic():
    return CT_PictureBuilder()


def a_prstGeom():
    return CT_PresetGeometry2DBuilder()


def a_stretch():
    return CT_StretchInfoPropertiesBuilder()


def an_ext():
    return CT_PositiveSize2DBuilder('a:ext')


def an_extent():
    return CT_PositiveSize2DBuilder('wp:extent')


def an_inline():
    return CT_InlineBuilder()


def an_nvPicPr():
    return CT_PictureNonVisualBuilder()


def an_off():
    return CT_Point2DBuilder()


def an_spPr():
    return CT_ShapePropertiesBuilder()


def an_xfrm():
    return CT_Transform2DBuilder()
