# encoding: utf-8

"""
Objects related to parsing headers of JPEG image streams, both JFIF and Exif
sub-formats.
"""

from __future__ import absolute_import, division, print_function

from ..compat import BytesIO
from .constants import JPEG_MARKER_CODE, MIME_TYPE
from .helpers import BIG_ENDIAN, StreamReader
from .image import BaseImageHeader
from .tiff import Tiff


class Jpeg(BaseImageHeader):
    """
    Base class for JFIF and EXIF subclasses.
    """
    @property
    def content_type(self):
        """
        MIME content type for this image, unconditionally `image/jpeg` for
        JPEG images.
        """
        return MIME_TYPE.JPEG

    @property
    def default_ext(self):
        """
        Default filename extension, always 'jpg' for JPG images.
        """
        return 'jpg'


class Exif(Jpeg):
    """
    Image header parser for Exif image format
    """
    @classmethod
    def from_stream(cls, stream):
        """
        Return |Exif| instance having header properties parsed from Exif
        image in *stream*.
        """
        markers = _JfifMarkers.from_stream(stream)
        # print('\n%s' % markers)

        px_width = markers.sof.px_width
        px_height = markers.sof.px_height
        horz_dpi = markers.app1.horz_dpi
        vert_dpi = markers.app1.vert_dpi

        return cls(px_width, px_height, horz_dpi, vert_dpi)


class Jfif(Jpeg):
    """
    Image header parser for JFIF image format
    """
    @classmethod
    def from_stream(cls, stream):
        """
        Return a |Jfif| instance having header properties parsed from image
        in *stream*.
        """
        markers = _JfifMarkers.from_stream(stream)

        px_width = markers.sof.px_width
        px_height = markers.sof.px_height
        horz_dpi = markers.app0.horz_dpi
        vert_dpi = markers.app0.vert_dpi

        return cls(px_width, px_height, horz_dpi, vert_dpi)


class _JfifMarkers(object):
    """
    Sequence of markers in a JPEG file, perhaps truncated at first SOS marker
    for performance reasons.
    """
    def __init__(self, markers):
        super(_JfifMarkers, self).__init__()
        self._markers = list(markers)

    def __str__(self):  # pragma: no cover
        """
        Returns a tabular listing of the markers in this instance, which can
        be handy for debugging and perhaps other uses.
        """
        header = ' offset  seglen  mc  name\n=======  ======  ==  ====='
        tmpl = '%7d  %6d  %02X  %s'
        rows = []
        for marker in self._markers:
            rows.append(tmpl % (
                marker.offset, marker.segment_length,
                ord(marker.marker_code), marker.name
            ))
        lines = [header] + rows
        return '\n'.join(lines)

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
        for m in self._markers:
            if m.marker_code == JPEG_MARKER_CODE.APP0:
                return m
        raise KeyError('no APP0 marker in image')

    @property
    def app1(self):
        """
        First APP1 marker in image markers.
        """
        for m in self._markers:
            if m.marker_code == JPEG_MARKER_CODE.APP1:
                return m
        raise KeyError('no APP1 marker in image')

    @property
    def sof(self):
        """
        First start of frame (SOFn) marker in this sequence.
        """
        for m in self._markers:
            if m.marker_code in JPEG_MARKER_CODE.SOF_MARKER_CODES:
                return m
        raise KeyError('no start of frame (SOFn) marker in image')


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
    def __init__(self, stream):
        super(_MarkerFinder, self).__init__()
        self._stream = stream

    @classmethod
    def from_stream(cls, stream):
        """
        Return a |_MarkerFinder| instance to find JFIF markers in *stream*.
        """
        return cls(stream)

    def next(self, start):
        """
        Return a (marker_code, segment_offset) 2-tuple identifying and
        locating the first marker in *stream* occuring after offset *start*.
        The returned *segment_offset* points to the position immediately
        following the 2-byte marker code, the start of the marker segment,
        for those markers that have a segment.
        """
        position = start
        while True:
            # skip over any non-\xFF bytes
            position = self._offset_of_next_ff_byte(start=position)
            # skip over any \xFF padding bytes
            position, byte_ = self._next_non_ff_byte(start=position+1)
            # 'FF 00' sequence is not a marker, start over if found
            if byte_ == b'\x00':
                continue
            # this is a marker, gather return values and break out of scan
            marker_code, segment_offset = byte_, position+1
            break
        return marker_code, segment_offset

    def _next_non_ff_byte(self, start):
        """
        Return an offset, byte 2-tuple for the next byte in *stream* that is
        not '\xFF', starting with the byte at offset *start*. If the byte at
        offset *start* is not '\xFF', *start* and the returned *offset* will
        be the same.
        """
        self._stream.seek(start)
        byte_ = self._read_byte()
        while byte_ == b'\xFF':
            byte_ = self._read_byte()
        offset_of_non_ff_byte = self._stream.tell() - 1
        return offset_of_non_ff_byte, byte_

    def _offset_of_next_ff_byte(self, start):
        """
        Return the offset of the next '\xFF' byte in *stream* starting with
        the byte at offset *start*. Returns *start* if the byte at that
        offset is a hex 255; it does not necessarily advance in the stream.
        """
        self._stream.seek(start)
        byte_ = self._read_byte()
        while byte_ != b'\xFF':
            byte_ = self._read_byte()
        offset_of_ff_byte = self._stream.tell() - 1
        return offset_of_ff_byte

    def _read_byte(self):
        """
        Return the next byte read from stream. Raise Exception if stream is
        at end of file.
        """
        byte_ = self._stream.read(1)
        if not byte_:  # pragma: no cover
            raise Exception('unexpected end of file')
        return byte_


def _MarkerFactory(marker_code, stream, offset):
    """
    Return |_Marker| or subclass instance appropriate for marker at *offset*
    in *stream* having *marker_code*.
    """
    if marker_code == JPEG_MARKER_CODE.APP0:
        marker_cls = _App0Marker
    elif marker_code == JPEG_MARKER_CODE.APP1:
        marker_cls = _App1Marker
    elif marker_code in JPEG_MARKER_CODE.SOF_MARKER_CODES:
        marker_cls = _SofMarker
    else:
        marker_cls = _Marker
    return marker_cls.from_stream(stream, marker_code, offset)


class _Marker(object):
    """
    Base class for JFIF marker classes. Represents a marker and its segment
    occuring in a JPEG byte stream.
    """
    def __init__(self, marker_code, offset, segment_length):
        super(_Marker, self).__init__()
        self._marker_code = marker_code
        self._offset = offset
        self._segment_length = segment_length

    @classmethod
    def from_stream(cls, stream, marker_code, offset):
        """
        Return a generic |_Marker| instance for the marker at *offset* in
        *stream* having *marker_code*.
        """
        if JPEG_MARKER_CODE.is_standalone(marker_code):
            segment_length = 0
        else:
            segment_length = stream.read_short(offset)
        return cls(marker_code, offset, segment_length)

    @property
    def marker_code(self):
        """
        The single-byte code that identifies the type of this marker, e.g.
        ``'\xE0'`` for start of image (SOI).
        """
        return self._marker_code

    @property
    def name(self):  # pragma: no cover
        return JPEG_MARKER_CODE.marker_names[self._marker_code]

    @property
    def offset(self):  # pragma: no cover
        return self._offset

    @property
    def segment_length(self):
        """
        The length in bytes of this marker's segment
        """
        return self._segment_length


class _App0Marker(_Marker):
    """
    Represents a JFIF APP0 marker segment.
    """
    def __init__(
            self, marker_code, offset, length, density_units, x_density,
            y_density):
        super(_App0Marker, self).__init__(marker_code, offset, length)
        self._density_units = density_units
        self._x_density = x_density
        self._y_density = y_density

    @property
    def horz_dpi(self):
        """
        Horizontal dots per inch specified in this marker, defaults to 72 if
        not specified.
        """
        return self._dpi(self._x_density)

    @property
    def vert_dpi(self):
        """
        Vertical dots per inch specified in this marker, defaults to 72 if
        not specified.
        """
        return self._dpi(self._y_density)

    def _dpi(self, density):
        """
        Return dots per inch corresponding to *density* value.
        """
        if self._density_units == 1:
            dpi = density
        elif self._density_units == 2:
            dpi = int(round(density * 2.54))
        else:
            dpi = 72
        return dpi

    @classmethod
    def from_stream(cls, stream, marker_code, offset):
        """
        Return an |_App0Marker| instance for the APP0 marker at *offset* in
        *stream*.
        """
        # field               off  type   notes
        # ------------------  ---  -----  -------------------
        # segment length       0   short
        # JFIF identifier      2   5 chr  'JFIF\x00'
        # major JPEG version   7   byte   typically 1
        # minor JPEG version   8   byte   typically 1 or 2
        # density units        9   byte   1=inches, 2=cm
        # horz dots per unit  10   short
        # vert dots per unit  12   short
        # ------------------  ---  -----  -------------------
        segment_length = stream.read_short(offset)
        density_units = stream.read_byte(offset, 9)
        x_density = stream.read_short(offset, 10)
        y_density = stream.read_short(offset, 12)
        return cls(
            marker_code, offset, segment_length, density_units, x_density,
            y_density
        )


class _App1Marker(_Marker):
    """
    Represents a JFIF APP1 (Exif) marker segment.
    """
    def __init__(self, marker_code, offset, length, horz_dpi, vert_dpi):
        super(_App1Marker, self).__init__(marker_code, offset, length)
        self._horz_dpi = horz_dpi
        self._vert_dpi = vert_dpi

    @classmethod
    def from_stream(cls, stream, marker_code, offset):
        """
        Extract the horizontal and vertical dots-per-inch value from the APP1
        header at *offset* in *stream*.
        """
        # field                 off  len  type   notes
        # --------------------  ---  ---  -----  ----------------------------
        # segment length         0    2   short
        # Exif identifier        2    6   6 chr  'Exif\x00\x00'
        # TIFF byte order        8    2   2 chr  'II'=little 'MM'=big endian
        # meaning of universe   10    2   2 chr  '*\x00' or '\x00*' depending
        # IFD0 off fr/II or MM  10   16   long   relative to ...?
        # --------------------  ---  ---  -----  ----------------------------
        segment_length = stream.read_short(offset)
        if cls._is_non_Exif_APP1_segment(stream, offset):
            return cls(marker_code, offset, segment_length, 72, 72)
        tiff = cls._tiff_from_exif_segment(stream, offset, segment_length)
        return cls(
            marker_code, offset, segment_length, tiff.horz_dpi, tiff.vert_dpi
        )

    @property
    def horz_dpi(self):
        """
        Horizontal dots per inch specified in this marker, defaults to 72 if
        not specified.
        """
        return self._horz_dpi

    @property
    def vert_dpi(self):
        """
        Vertical dots per inch specified in this marker, defaults to 72 if
        not specified.
        """
        return self._vert_dpi

    @classmethod
    def _is_non_Exif_APP1_segment(cls, stream, offset):
        """
        Return True if the APP1 segment at *offset* in *stream* is NOT an
        Exif segment, as determined by the ``'Exif\x00\x00'`` signature at
        offset 2 in the segment.
        """
        stream.seek(offset+2)
        exif_signature = stream.read(6)
        return exif_signature != b'Exif\x00\x00'

    @classmethod
    def _tiff_from_exif_segment(cls, stream, offset, segment_length):
        """
        Return a |Tiff| instance parsed from the Exif APP1 segment of
        *segment_length* at *offset* in *stream*.
        """
        # wrap full segment in its own stream and feed to Tiff()
        stream.seek(offset+8)
        segment_bytes = stream.read(segment_length-8)
        substream = BytesIO(segment_bytes)
        return Tiff.from_stream(substream)


class _SofMarker(_Marker):
    """
    Represents a JFIF start of frame (SOFx) marker segment.
    """
    def __init__(
            self, marker_code, offset, segment_length, px_width, px_height):
        super(_SofMarker, self).__init__(marker_code, offset, segment_length)
        self._px_width = px_width
        self._px_height = px_height

    @classmethod
    def from_stream(cls, stream, marker_code, offset):
        """
        Return an |_SofMarker| instance for the SOFn marker at *offset* in
        stream.
        """
        # field                 off  type   notes
        # ------------------  ---  -----  ----------------------------
        # segment length       0   short
        # Data precision       2   byte
        # Vertical lines       3   short  px_height
        # Horizontal lines     5   short  px_width
        # ------------------  ---  -----  ----------------------------
        segment_length = stream.read_short(offset)
        px_height = stream.read_short(offset, 3)
        px_width = stream.read_short(offset, 5)
        return cls(marker_code, offset, segment_length, px_width, px_height)

    @property
    def px_height(self):
        """
        Image height in pixels
        """
        return self._px_height

    @property
    def px_width(self):
        """
        Image width in pixels
        """
        return self._px_width
