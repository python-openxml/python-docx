# encoding: utf-8

"""
Test suite for docx.image.bmp module
"""

from __future__ import absolute_import, print_function

import pytest

from docx.compat import BytesIO
from docx.image.constants import MIME_TYPE
from docx.image.bmp import Bmp

from ..unitutil.mock import ANY, initializer_mock


class DescribeBmp(object):
    def it_can_construct_from_a_bmp_stream(self, Bmp__init__):
        cx, cy, horz_dpi, vert_dpi = 26, 43, 200, 96
        bytes_ = (
            b"fillerfillerfiller\x1A\x00\x00\x00\x2B\x00\x00\x00"
            b"fillerfiller\xB8\x1E\x00\x00\x00\x00\x00\x00"
        )
        stream = BytesIO(bytes_)

        bmp = Bmp.from_stream(stream)

        Bmp__init__.assert_called_once_with(ANY, cx, cy, horz_dpi, vert_dpi)
        assert isinstance(bmp, Bmp)

    def it_knows_its_content_type(self):
        bmp = Bmp(None, None, None, None)
        assert bmp.content_type == MIME_TYPE.BMP

    def it_knows_its_default_ext(self):
        bmp = Bmp(None, None, None, None)
        assert bmp.default_ext == "bmp"

    # fixtures -------------------------------------------------------

    @pytest.fixture
    def Bmp__init__(self, request):
        return initializer_mock(request, Bmp)
