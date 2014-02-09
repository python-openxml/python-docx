# encoding: utf-8

"""
Objects related to parsing headers of JPEG image streams, both JFIF and Exif
sub-formats.
"""

from __future__ import absolute_import, division, print_function

from .constants import JPEG_MARKER_CODE
from .helpers import BIG_ENDIAN, StreamReader
from .image import Image


class Jpeg(Image):
    """
    Base class for JFIF and EXIF subclasses.
    """


class Exif(Jpeg):
    """
    Image header parser for Exif image format
    """


class Jfif(Jpeg):
    """
    Image header parser for JFIF image format
    """
    def __init__(self, blob, filename, cx, cy, horz_dpi, vert_dpi):
        super(Jfif, self).__init__(blob, filename, cx, cy, attrs={})
        self._horz_dpi = horz_dpi
        self._vert_dpi = vert_dpi

    @classmethod
    def from_stream(cls, stream, blob, filename):
        """
        Return a |Jfif| instance having header properties parsed from image
        in *stream*.
        """
        markers = _JfifMarkers.from_stream(stream)
        sof, app0 = markers.sof, markers.app0
        cx, cy = sof.px_width, sof.px_height
        horz_dpi, vert_dpi = app0.horz_dpi, app0.vert_dpi
        return cls(blob, filename, cx, cy, horz_dpi, vert_dpi)

    @property
    def horz_dpi(self):
        """
        Integer dots per inch for the width of this image. Defaults to 72
        when not present in the file, as is often the case.
        """
        return self._horz_dpi

    @property
    def vert_dpi(self):
        """
        Integer dots per inch for the height of this image. Defaults to 72
        when not present in the file, as is often the case.
        """
        return self._vert_dpi


class _JfifMarkers(object):
    """
    Sequence of markers in a JPEG file, perhaps truncated at first SOS marker
    for performance reasons.
    """
    def __init__(self, markers):
        super(_JfifMarkers, self).__init__()
        self._markers = list(markers)

    @classmethod
    def from_stream(cls, stream):
        """
        Return a |_JfifMarkers| instance containing a |_JfifMarker| subclass
        instance for each marker in *stream*.
        """
        marker_parser = _MarkerParser.from_stream(stream)
        markers = []
        for marker in marker_parser.iter_markers():
            markers.append(marker)
            if marker.marker_code == JPEG_MARKER_CODE.SOS:
                break
        return cls(markers)

    @property
    def app0(self):
        """
        First APP0 marker in image markers.
        """
        raise NotImplementedError

    @property
    def sof(self):
        """
        First start of frame (SOFn) marker in this sequence.
        """
        raise NotImplementedError


class _MarkerParser(object):
    """
    Service class that knows how to parse a JFIF stream and iterate over its
    markers.
    """
    def __init__(self, stream_reader):
        super(_MarkerParser, self).__init__()
        self._stream = stream_reader

    @classmethod
    def from_stream(cls, stream):
        """
        Return a |_MarkerParser| instance to parse JFIF markers from
        *stream*.
        """
        stream_reader = StreamReader(stream, BIG_ENDIAN)
        return cls(stream_reader)

    def iter_markers(self):
        """
        Generate a (marker_code, segment_offset) 2-tuple for each marker in
        the JPEG *stream*, in the order they occur in the stream.
        """
        marker_finder = _MarkerFinder.from_stream(self._stream)
        start = 0
        marker_code = None
        while marker_code != JPEG_MARKER_CODE.EOI:
            marker_code, segment_offset = marker_finder.next(start)
            marker = _MarkerFactory(
                marker_code, self._stream, segment_offset
            )
            yield marker
            start = segment_offset + marker.segment_length


class _MarkerFinder(object):
    """
    Service class that knows how to find the next JFIF marker in a stream.
    """
    @classmethod
    def from_stream(cls, stream):
        """
        Return a |_MarkerFinder| instance to find JFIF markers in *stream*.
        """
        raise NotImplementedError

    def next(self, start):
        """
        Return a (marker_code, segment_offset) 2-tuple identifying and
        locating the first marker in *stream* occuring after offset *start*.
        The returned *segment_offset* points to the position immediately
        following the 2-byte marker code, the start of the marker segment,
        for those markers that have a segment.
        """
        raise NotImplementedError


def _MarkerFactory(marker_code, stream, offset):
    """
    Return |_Marker| or subclass instance appropriate for marker at *offset*
    in *stream* having *marker_code*.
    """
    raise NotImplementedError


class _Marker(object):
    """
    Base class for JFIF marker classes. Represents a marker and its segment
    occuring in a JPEG byte stream.
    """
    @property
    def marker_code(self):
        """
        The single-byte code that identifies the type of this marker, e.g.
        ``'\xE0'`` for start of image (SOI).
        """
        raise NotImplementedError

    @property
    def segment_length(self):
        """
        The length in bytes of this marker's segment
        """
        raise NotImplementedError


class _App0Marker(_Marker):
    """
    Represents a JFIF APP0 marker segment.
    """


class _SofMarker(_Marker):
    """
    Represents a JFIF start of frame (SOFx) marker segment.
    """
