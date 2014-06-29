# encoding: utf-8

"""
Test suite for docx.image.gif module
"""

from __future__ import absolute_import, print_function

import pytest

from docx.compat import BytesIO
from docx.image.constants import MIME_TYPE
from docx.image.gif import Gif

from ..unitutil.mock import initializer_mock


class DescribeGif(object):

    def it_can_construct_from_a_gif_stream(self, from_stream_fixture):
        stream, Gif__init__, cx, cy = from_stream_fixture
        gif = Gif.from_stream(stream)
        Gif__init__.assert_called_once_with(cx, cy, 72, 72)
        assert isinstance(gif, Gif)

    def it_knows_its_content_type(self):
        gif = Gif(None, None, None, None)
        assert gif.content_type == MIME_TYPE.GIF

    def it_knows_its_default_ext(self):
        gif = Gif(None, None, None, None)
        assert gif.default_ext == 'gif'

    # fixtures -------------------------------------------------------

    @pytest.fixture
    def from_stream_fixture(self, Gif__init__):
        cx, cy = 42, 24
        bytes_ = b'filler\x2A\x00\x18\x00'
        stream = BytesIO(bytes_)
        return stream, Gif__init__, cx, cy

    @pytest.fixture
    def Gif__init__(self, request):
        return initializer_mock(request, Gif)
