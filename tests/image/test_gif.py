# encoding: utf-8

"""Unit test suite for docx.image.gif module"""

from __future__ import absolute_import, print_function

import pytest

from docx.compat import BytesIO
from docx.image.constants import MIME_TYPE
from docx.image.gif import Gif

from ..unitutil.mock import ANY, initializer_mock


class DescribeGif(object):

    def it_can_construct_from_a_gif_stream(self, Gif__init__):
        cx, cy = 42, 24
        bytes_ = b'filler\x2A\x00\x18\x00'
        stream = BytesIO(bytes_)

        gif = Gif.from_stream(stream)

        Gif__init__.assert_called_once_with(ANY, cx, cy, 72, 72)
        assert isinstance(gif, Gif)

    def it_knows_its_content_type(self):
        gif = Gif(None, None, None, None)
        assert gif.content_type == MIME_TYPE.GIF

    def it_knows_its_default_ext(self):
        gif = Gif(None, None, None, None)
        assert gif.default_ext == 'gif'

    # fixture components ---------------------------------------------

    @pytest.fixture
    def Gif__init__(self, request):
        return initializer_mock(request, Gif)
