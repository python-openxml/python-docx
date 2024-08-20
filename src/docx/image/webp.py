"""Objects related to parsing headers of WEBP image streams.

Docs: https://developers.google.com/speed/webp/docs/riff_container

VP8:

 0                   1                   2                   3
 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|      'R'      |      'I'      |      'F'      |      'F'      |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                           File Size                           |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|      'W'      |      'E'      |      'B'      |      'P'      |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                      ChunkHeader('VP8 ')                      |
|                                                               |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
:                           VP8 data                            :
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

1. Data begins with string RIFF
2. Little-endian 32-bit file size
3. String WEBP
4. String VP8 (with space)
5. Little-endian 32-bit chunk size
6. 3-byte frame tag for interframes, or 10-byte frame tag for keyframes
7. Compressed data partitions containing:
   - Frame header
   - Macroblock prediction data
   - DCT/WHT coefficient data
The frame dimensions are encoded in the frame header within the first compressed data partition, 
not in a fixed position like VP8L.

VP8L:

 0                   1                   2                   3
 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|      'R'      |      'I'      |      'F'      |      'F'      |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                           File Size                           |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|      'W'      |      'E'      |      'B'      |      'P'      |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                      ChunkHeader('VP8L')                      |
|                                                               |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
:                           VP8L data                           :
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

1. Data begins with the string RIFF 
2. A little endian 32 bit value 
3. String WEBP 
4. String VP8L 
5. A little endian 32 bit value 
6. 1 byte signature 0x2f And then the first 28 bits contains the width and the height

VP8X:

 0                   1                   2                   3
 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|      'R'      |      'I'      |      'F'      |      'F'      |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                           File Size                           |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|      'W'      |      'E'      |      'B'      |      'P'      |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                      ChunkHeader('VP8X')                      |
|                                                               |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|Rsv|I|L|E|X|A|R|                   Reserved                    |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|          Canvas Width Minus One               |             ...
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
...  Canvas Height Minus One    |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+


1. Data begins with string RIFF
2. Little-endian 32-bit file size
3. String WEBP
4. String VP8X
5. Little-endian 32-bit chunk size
6. Reeserved (Rsv): 2 bits (MUST be 0. Readers MUST ignore this field.)
7. ICC profile (I): 1 bit (Set if the file contains an 'ICCP' Chunk.)
8. Alpha (L): 1 bit (Set if any of the frames of the image contain transparency information ("alpha").)
9. Exif metadata (E): 1 bit (Set if the file contains Exif metadata.)
10. XMP metadata (X): 1 bit (Set if the file contains XMP metadata.)
11. Animation (A): 1 bit (Set if this is an animated image. Data in 'ANIM' and 'ANMF' Chunks should be used to control the animation.)
12. Reserved (R): 1 bit (MUST be 0. Readers MUST ignore this field.)
13. Reserved: 24 bits (MUST be 0. Readers MUST ignore this field.)
14. Canvas Width Minus One: 24 bits (1-based width of the canvas in pixels. The actual canvas width is 1 + Canvas Width Minus One.)
15. Canvas Height Minus One: 24 bits (1-based height of the canvas in pixels. The actual canvas height is 1 + Canvas Height Minus One.)
16. The product of Canvas Width and Canvas Height MUST be at most 2^32 - 1.
"""

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
        if stream.read(4) != b'RIFF':
            raise ValueError("Not a valid WebP file")
        
        _ = stream.read(4)  # File size, we can skip this
        
        if stream.read(4) != b'WEBP':
            raise ValueError("Not a valid WebP file")
        
        chunk_header = stream.read(4)
        
        if chunk_header == b'VP8L':
            width, height = cls._parse_lossless(stream)
        elif chunk_header == b'VP8X':
            width, height = cls._parse_extended(stream)
        elif chunk_header == b'VP8 ':
            width, height = cls._parse_simple(stream)
        else:
            raise ValueError("Unsupported WebP format")
        
        return cls(width, height, 72, 72)
    
    @staticmethod
    def _parse_lossless(stream):
        _ = unpack('<I', stream.read(4))[0]  # Chunk size, we can skip this
        
        signature = stream.read(1)[0]
        if signature != 0x2f:
            raise ValueError("Invalid lossless WebP signature")
        
        data = stream.read(4)
        bits = int.from_bytes(data, 'little')
        
        w = (bits & 0x3FFF) + 1
        h = ((bits >> 14) & 0x3FFF) + 1
        
        return w, h

    @staticmethod
    def _parse_extended(stream):
        _ = unpack('<I', stream.read(4))[0]  # Chunk size, we can skip this
        
        _ = stream.read(4)  # Skip flags
        
        width_minus_one = int.from_bytes(stream.read(3), 'little')
        height_minus_one = int.from_bytes(stream.read(3), 'little')
        
        w = width_minus_one + 1
        h = height_minus_one + 1
        
        return w, h

    @staticmethod
    def _parse_simple(stream):
        stream.seek(9, 1)  # Skip 9 bytes
        
        bits = stream.read(2)
        w = ((bits[1] & 0x3F) << 8) | bits[0]
        h = (bits[1] & 0xC0) | stream.read(1)[0]
        
        return w, h

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
        elif vp8_header == b'VP8X':
            self._parse_extended_webp()
        else:
            raise ValueError('Unsupported WebP format')

    def _parse_simple_webp(self):
        self._stream_rdr.skip(3)  # Skip frame tag for interframes
        frame_tag = self._stream_rdr.read(1)
        if frame_tag[0] & 0x1:  # Check if it's a keyframe
            self._stream_rdr.skip(6)  # Skip rest of keyframe tag
        else:
            self._stream_rdr.seek(-3, 1)  # Go back to start of frame tag
        
        # Read first two bytes of frame header
        bits = self._stream_rdr.read(2)
        self._width = ((bits[1] & 0x3F) << 8) | bits[0]
        self._height = (bits[1] & 0xC0) | self._stream_rdr.read(1)[0]

    def _parse_lossless_webp(self):
        self._stream_rdr.skip(1)
        bits = self._stream_rdr.read(4)
        self._width = 1 + ((bits[1] & 63) << 8 | bits[0])
        self._height = 1 + ((bits[3] & 15) << 10 | bits[2] << 2 | (bits[1] & 192) >> 6)

    def _parse_extended_webp(self):
        self._stream_rdr.skip(8)  # Skip chunk size and flags
        width_minus_one = int.from_bytes(self._stream_rdr.read(3), 'little')
        height_minus_one = int.from_bytes(self._stream_rdr.read(3), 'little')
        self._width = width_minus_one + 1
        self._height = height_minus_one + 1

    @classmethod
    def parse(cls, stream):
        parser = cls(stream)
        return parser
