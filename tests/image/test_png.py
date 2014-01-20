# encoding: utf-8

"""
Test suite for docx.image.png module
"""

from __future__ import absolute_import, print_function

import pytest

from docx.compat import BytesIO
from docx.image.helpers import StreamReader
from docx.image.png import Png

from ..unitutil import (
    initializer_mock, class_mock, instance_mock, method_mock
)


class DescribePng(object):

    def it_can_construct_from_a_png_stream(self, from_stream_fixture):
        # fixture ----------------------
        (stream_, blob_, filename_, StreamReader_, _parse_png_headers_,
         stream_rdr_, Png__init__, cx, cy, attrs, png_) = from_stream_fixture
        # exercise ---------------------
        png = Png.from_stream(stream_, blob_, filename_)
        # verify -----------------------
        StreamReader_.assert_called_once_with(stream_, '>')
        _parse_png_headers_.assert_called_once_with(stream_rdr_)
        Png__init__.assert_called_once_with(blob_, filename_, cx, cy, attrs)
        assert isinstance(png, Png)

    # fixtures -------------------------------------------------------

    @pytest.fixture
    def attrs(self):
        return dict()

    @pytest.fixture
    def blob_(self, request):
        return instance_mock(request, bytes)

    @pytest.fixture
    def filename_(self, request):
        return instance_mock(request, str)

    @pytest.fixture
    def from_stream_fixture(
            self, stream_, blob_, filename_, StreamReader_,
            _parse_png_headers_, stream_rdr_, Png__init__, attrs, png_):
        cx, cy = 42, 24
        attrs.update({'px_width': cx, 'px_height': cy})
        return (
            stream_, blob_, filename_, StreamReader_, _parse_png_headers_,
            stream_rdr_, Png__init__, cx, cy, attrs, png_
        )

    @pytest.fixture
    def Png__init__(self, request):
        return initializer_mock(request, Png)

    @pytest.fixture
    def _parse_png_headers_(self, request, attrs):
        return method_mock(
            request, Png, '_parse_png_headers', return_value=attrs
        )

    @pytest.fixture
    def png_(self, request):
        return instance_mock(request, Png)

    @pytest.fixture
    def StreamReader_(self, request, stream_rdr_):
        return class_mock(
            request, 'docx.image.png.StreamReader', return_value=stream_rdr_
        )

    @pytest.fixture
    def stream_(self, request):
        return instance_mock(request, BytesIO)

    @pytest.fixture
    def stream_rdr_(self, request):
        return instance_mock(request, StreamReader)
