# encoding: utf-8

"""
Test suite for docx.image.jpeg module
"""

from __future__ import absolute_import, print_function

import pytest

from docx.compat import BytesIO
from docx.image.jpeg import Jfif, _JfifMarkers

from ..unitutil import class_mock, instance_mock


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
