# encoding: utf-8

"""
Constants specific the the image sub-package
"""


class MIME_TYPE(object):
    """
    Image content types.
    """
    PNG = 'image/png'


class TAG(object):
    """
    Identifiers for image attribute tags.
    """

    PX_WIDTH = 'px_width'
    PX_HEIGHT = 'px_height'
    HORZ_PX_PER_UNIT = 'horz_px_per_unit'
    VERT_PX_PER_UNIT = 'vert_px_per_unit'
    UNITS_SPECIFIER = 'units_specifier'
