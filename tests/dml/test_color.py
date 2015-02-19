# encoding: utf-8

"""
Test suite for docx.dml.color module.
"""

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

from docx.enum.dml import MSO_COLOR_TYPE
from docx.dml.color import ColorFormat
from docx.shared import RGBColor

from ..unitutil.cxml import element

import pytest


class DescribeColorFormat(object):

    def it_knows_its_color_type(self, type_fixture):
        color_format, expected_value = type_fixture
        assert color_format.type == expected_value

    def it_knows_its_RGB_value(self, rgb_get_fixture):
        color_format, expected_value = rgb_get_fixture
        assert color_format.rgb == expected_value

    # fixtures ---------------------------------------------

    @pytest.fixture(params=[
        ('w:r',                                                  None),
        ('w:r/w:rPr',                                            None),
        ('w:r/w:rPr/w:color{w:val=auto}',                        None),
        ('w:r/w:rPr/w:color{w:val=4224FF}',                      '4224ff'),
        ('w:r/w:rPr/w:color{w:val=auto,w:themeColor=accent1}',   None),
        ('w:r/w:rPr/w:color{w:val=F00BA9,w:themeColor=accent1}', 'f00ba9'),
    ])
    def rgb_get_fixture(self, request):
        r_cxml, rgb = request.param
        color_format = ColorFormat(element(r_cxml))
        expected_value = None if rgb is None else RGBColor.from_string(rgb)
        return color_format, expected_value

    @pytest.fixture(params=[
        ('w:r',                                   None),
        ('w:r/w:rPr',                             None),
        ('w:r/w:rPr/w:color{w:val=auto}',         MSO_COLOR_TYPE.AUTO),
        ('w:r/w:rPr/w:color{w:val=4224FF}',       MSO_COLOR_TYPE.RGB),
        ('w:r/w:rPr/w:color{w:themeColor=dark1}', MSO_COLOR_TYPE.THEME),
        ('w:r/w:rPr/w:color{w:val=F00BA9,w:themeColor=accent1}',
         MSO_COLOR_TYPE.THEME),
    ])
    def type_fixture(self, request):
        r_cxml, expected_value = request.param
        color_format = ColorFormat(element(r_cxml))
        return color_format, expected_value
