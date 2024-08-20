"""Objects related to parsing headers of WEBP image streams."""

import io
from struct import unpack

from docx.image.constants import MIME_TYPE
from docx.image.helpers import BIG_ENDIAN, StreamReader
from docx.image.image import BaseImageHeader

class Webp(BaseImageHeader):
    """Image header parser for WEBP image format."""

    @classmethod
    def from_stream(cls, stream):
        """Return |Webp| instance having header properties parsed from WEBP image in
        `stream`."""
        stream.seek(0)
        stream_reader = StreamReader(stream, BIG_ENDIAN)
        
        # Skip RIFF header
        stream_reader.skip(12)
        
        # Read VP8 header
        vp8_header = stream_reader.read(4)
        
        if vp8_header == b'VP8 ':
            # Simple WebP
            stream_reader.skip(6)
            width, height = unpack('<HH', stream_reader.read(4))
        elif vp8_header == b'VP8L':
            # Lossless WebP
            stream_reader.skip(1)
            bits = stream_reader.read(4)
            width = 1 + ((bits[1] & 63) << 8 | bits[0])
            height = 1 + ((bits[3] & 15) << 10 | bits[2] << 2 | (bits[1] & 192) >> 6)
        else:
            raise ValueError('Unsupported WebP format')

        # WebP doesn't store DPI information, so we use default 72 DPI
        horz_dpi = vert_dpi = 72

        return cls(width, height, horz_dpi, vert_dpi)

    @property
    def content_type(self):
        """MIME content type for this image."""
        return MIME_TYPE.WEBP

    @property
    def default_ext(self):
        """Default filename extension, always 'webp' for WEBP images."""
        return 'webp'

class _WebpParser:
    """Parser for WebP image binary data."""

    def __init__(self, stream):
        self._stream = stream
        self._stream_rdr = StreamReader(stream, BIG_ENDIAN)
        self._width = None
        self._height = None

    @property
    def px_width(self):
        self._parse_dimensions()
        return self._width

    @property
    def px_height(self):
        self._parse_dimensions()
        return self._height

    @property
    def horz_dpi(self):
        return 72

    @property
    def vert_dpi(self):
        return 72

    def _parse_dimensions(self):
        if self._width is not None:
            return

        self._stream_rdr.seek(12)  # Skip RIFF header
        vp8_header = self._stream_rdr.read(4)

        if vp8_header == b'VP8 ':
            self._parse_simple_webp()
        elif vp8_header == b'VP8L':
            self._parse_lossless_webp()
        else:
            raise ValueError('Unsupported WebP format')

    def _parse_simple_webp(self):
        self._stream_rdr.skip(6)
        self._width, self._height = unpack('<HH', self._stream_rdr.read(4))

    def _parse_lossless_webp(self):
        self._stream_rdr.skip(1)
        bits = self._stream_rdr.read(4)
        self._width = 1 + ((bits[1] & 63) << 8 | bits[0])
        self._height = 1 + ((bits[3] & 15) << 10 | bits[2] << 2 | (bits[1] & 192) >> 6)

    @classmethod
    def parse(cls, stream):
        parser = cls(stream)
        return parser
