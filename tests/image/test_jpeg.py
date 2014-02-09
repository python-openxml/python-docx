# encoding: utf-8

"""
Test suite for docx.image.jpeg module
"""

from __future__ import absolute_import, print_function

import pytest

from docx.compat import BytesIO
from docx.image.constants import JPEG_MARKER_CODE
from docx.image.jpeg import (
    _App0Marker, Jfif, _JfifMarkers, _Marker, _MarkerParser, _SofMarker
)

from ..unitutil import class_mock, initializer_mock, instance_mock


class DescribeJfif(object):

    def it_can_construct_from_a_jfif_stream(self, from_stream_fixture):
        # fixture ----------------------
        (stream_, blob_, filename_, _JfifMarkers_, px_width, px_height,
         horz_dpi, vert_dpi) = from_stream_fixture
        # exercise ---------------------
        jfif = Jfif.from_stream(stream_, blob_, filename_)
        # verify -----------------------
        _JfifMarkers_.from_stream.assert_called_once_with(stream_)
        assert isinstance(jfif, Jfif)
        assert jfif.px_width == px_width
        assert jfif.px_height == px_height
        assert jfif.horz_dpi == horz_dpi
        assert jfif.vert_dpi == vert_dpi

    # fixtures -------------------------------------------------------

    @pytest.fixture
    def blob_(self, request):
        return instance_mock(request, bytes)

    @pytest.fixture
    def filename_(self, request):
        return instance_mock(request, str)

    @pytest.fixture
    def from_stream_fixture(
            self, stream_, blob_, filename_, _JfifMarkers_, jfif_markers_):
        px_width, px_height = 111, 222
        horz_dpi, vert_dpi = 333, 444
        jfif_markers_.sof.px_width = px_width
        jfif_markers_.sof.px_height = px_height
        jfif_markers_.app0.horz_dpi = horz_dpi
        jfif_markers_.app0.vert_dpi = vert_dpi
        return (
            stream_, blob_, filename_, _JfifMarkers_, px_width, px_height,
            horz_dpi, vert_dpi
        )

    @pytest.fixture
    def _JfifMarkers_(self, request, jfif_markers_):
        _JfifMarkers_ = class_mock(request, 'docx.image.jpeg._JfifMarkers')
        _JfifMarkers_.from_stream.return_value = jfif_markers_
        return _JfifMarkers_

    @pytest.fixture
    def jfif_markers_(self, request):
        return instance_mock(request, _JfifMarkers)

    @pytest.fixture
    def stream_(self, request):
        return instance_mock(request, BytesIO)


class Describe_JfifMarkers(object):

    def it_can_construct_from_a_jfif_stream(self, from_stream_fixture):
        stream_, _MarkerParser_, _JfifMarkers__init_, marker_lst = (
            from_stream_fixture
        )
        jfif_markers = _JfifMarkers.from_stream(stream_)
        _MarkerParser_.from_stream.assert_called_once_with(stream_)
        _JfifMarkers__init_.assert_called_once_with(marker_lst)
        assert isinstance(jfif_markers, _JfifMarkers)

    # fixtures -------------------------------------------------------

    @pytest.fixture
    def app0_(self, request):
        return instance_mock(
            request, _App0Marker, marker_code=JPEG_MARKER_CODE.APP0
        )

    @pytest.fixture
    def eoi_(self, request):
        return instance_mock(
            request, _SofMarker, marker_code=JPEG_MARKER_CODE.EOI
        )

    @pytest.fixture
    def from_stream_fixture(
            self, stream_, _MarkerParser_, _JfifMarkers__init_, soi_, app0_,
            sof_, sos_):
        marker_lst = [soi_, app0_, sof_, sos_]
        return stream_, _MarkerParser_, _JfifMarkers__init_, marker_lst

    @pytest.fixture
    def _JfifMarkers__init_(self, request):
        return initializer_mock(request, _JfifMarkers)

    @pytest.fixture
    def marker_parser_(self, request, markers_all_):
        marker_parser_ = instance_mock(request, _MarkerParser)
        marker_parser_.iter_markers.return_value = markers_all_
        return marker_parser_

    @pytest.fixture
    def _MarkerParser_(self, request, marker_parser_):
        _MarkerParser_ = class_mock(request, 'docx.image.jpeg._MarkerParser')
        _MarkerParser_.from_stream.return_value = marker_parser_
        return _MarkerParser_

    @pytest.fixture
    def markers_all_(self, request, soi_, app0_, sof_, sos_, eoi_):
        return [soi_, app0_, sof_, sos_, eoi_]

    @pytest.fixture
    def sof_(self, request):
        return instance_mock(
            request, _SofMarker, marker_code=JPEG_MARKER_CODE.SOF0
        )

    @pytest.fixture
    def soi_(self, request):
        return instance_mock(
            request, _Marker, marker_code=JPEG_MARKER_CODE.SOI
        )

    @pytest.fixture
    def sos_(self, request):
        return instance_mock(
            request, _Marker, marker_code=JPEG_MARKER_CODE.SOS
        )

    @pytest.fixture
    def stream_(self, request):
        return instance_mock(request, BytesIO)
