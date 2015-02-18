# encoding: utf-8

"""
Test suite for docx.dml.color module.
"""

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

from docx.enum.dml import MSO_COLOR_TYPE
from docx.dml.color import ColorFormat

from ..unitutil.cxml import element

import pytest


class DescribeColorFormat(object):

    def it_knows_its_color_type(self, type_fixture):
        color_format, expected_value = type_fixture
        assert color_format.type == expected_value

    # fixtures ---------------------------------------------

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
