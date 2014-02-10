# encoding: utf-8

"""
Test suite for docx.image.tiff module
"""

from __future__ import absolute_import, print_function

import pytest

from docx.compat import BytesIO
from docx.image.tiff import Tiff, _TiffParser

from ..unitutil import class_mock, initializer_mock, instance_mock


class DescribeTiff(object):

    def it_can_construct_from_a_tiff_stream(self, from_stream_fixture):
        (stream_, blob_, filename_, _TiffParser_, Tiff__init_, px_width,
         px_height, horz_dpi, vert_dpi) = from_stream_fixture
        tiff = Tiff.from_stream(stream_, blob_, filename_)
        _TiffParser_.parse.assert_called_once_with(stream_)
        Tiff__init_.assert_called_once_with(
            blob_, filename_, px_width, px_height, horz_dpi, vert_dpi
        )
        assert isinstance(tiff, Tiff)

    # fixtures -------------------------------------------------------

    @pytest.fixture
    def blob_(self, request):
        return instance_mock(request, bytes)

    @pytest.fixture
    def filename_(self, request):
        return instance_mock(request, str)

    @pytest.fixture
    def from_stream_fixture(
            self, stream_, blob_, filename_, _TiffParser_, tiff_parser_,
            Tiff__init_):
        px_width, px_height = 111, 222
        horz_dpi, vert_dpi = 333, 444
        tiff_parser_.px_width = px_width
        tiff_parser_.px_height = px_height
        tiff_parser_.horz_dpi = horz_dpi
        tiff_parser_.vert_dpi = vert_dpi
        return (
            stream_, blob_, filename_, _TiffParser_, Tiff__init_, px_width,
            px_height, horz_dpi, vert_dpi
        )

    @pytest.fixture
    def Tiff__init_(self, request):
        return initializer_mock(request, Tiff)

    @pytest.fixture
    def _TiffParser_(self, request, tiff_parser_):
        _TiffParser_ = class_mock(request, 'docx.image.tiff._TiffParser')
        _TiffParser_.parse.return_value = tiff_parser_
        return _TiffParser_

    @pytest.fixture
    def tiff_parser_(self, request):
        return instance_mock(request, _TiffParser)

    @pytest.fixture
    def stream_(self, request):
        return instance_mock(request, BytesIO)
