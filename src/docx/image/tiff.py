from .constants import MIME_TYPE, TIFF_FLD, TIFF_TAG
from .helpers import BIG_ENDIAN, LITTLE_ENDIAN, StreamReader
from .image import BaseImageHeader


class Tiff(BaseImageHeader):
    """Image header parser for TIFF images.

    Handles both big and little endian byte ordering.
    """

    @property
    def content_type(self):
        """Return the MIME type of this TIFF image, unconditionally the string
        ``image/tiff``."""
        return MIME_TYPE.TIFF

    @property
    def default_ext(self):
        """Default filename extension, always 'tiff' for TIFF images."""
        return "tiff"

    @classmethod
    def from_stream(cls, stream):
        """Return a |Tiff| instance containing the properties of the TIFF image in
        `stream`."""
        parser = _TiffParser.parse(stream)

        px_width = parser.px_width
        px_height = parser.px_height
        horz_dpi = parser.horz_dpi
        vert_dpi = parser.vert_dpi

        return cls(px_width, px_height, horz_dpi, vert_dpi)


class _TiffParser:
    """Parses a TIFF image stream to extract the image properties found in its main
    image file directory (IFD)"""

    def __init__(self, ifd_entries):
        super(_TiffParser, self).__init__()
        self._ifd_entries = ifd_entries

    @classmethod
    def parse(cls, stream):
        """Return an instance of |_TiffParser| containing the properties parsed from the
        TIFF image in `stream`."""
        stream_rdr = cls._make_stream_reader(stream)
        ifd0_offset = stream_rdr.read_long(4)
        ifd_entries = _IfdEntries.from_stream(stream_rdr, ifd0_offset)
        return cls(ifd_entries)

    @property
    def horz_dpi(self):
        """The horizontal dots per inch value calculated from the XResolution and
        ResolutionUnit tags of the IFD; defaults to 72 if those tags are not present."""
        return self._dpi(TIFF_TAG.X_RESOLUTION)

    @property
    def vert_dpi(self):
        """The vertical dots per inch value calculated from the XResolution and
        ResolutionUnit tags of the IFD; defaults to 72 if those tags are not present."""
        return self._dpi(TIFF_TAG.Y_RESOLUTION)

    @property
    def px_height(self):
        """The number of stacked rows of pixels in the image, |None| if the IFD contains
        no ``ImageLength`` tag, the expected case when the TIFF is embeded in an Exif
        image."""
        return self._ifd_entries.get(TIFF_TAG.IMAGE_LENGTH)

    @property
    def px_width(self):
        """The number of pixels in each row in the image, |None| if the IFD contains no
        ``ImageWidth`` tag, the expected case when the TIFF is embeded in an Exif
        image."""
        return self._ifd_entries.get(TIFF_TAG.IMAGE_WIDTH)

    @classmethod
    def _detect_endian(cls, stream):
        """Return either BIG_ENDIAN or LITTLE_ENDIAN depending on the endian indicator
        found in the TIFF `stream` header, either 'MM' or 'II'."""
        stream.seek(0)
        endian_str = stream.read(2)
        return BIG_ENDIAN if endian_str == b"MM" else LITTLE_ENDIAN

    def _dpi(self, resolution_tag):
        """Return the dpi value calculated for `resolution_tag`, which can be either
        TIFF_TAG.X_RESOLUTION or TIFF_TAG.Y_RESOLUTION.

        The calculation is based on the values of both that tag and the
        TIFF_TAG.RESOLUTION_UNIT tag in this parser's |_IfdEntries| instance.
        """
        ifd_entries = self._ifd_entries

        if resolution_tag not in ifd_entries:
            return 72

        # resolution unit defaults to inches (2)
        resolution_unit = (
            ifd_entries[TIFF_TAG.RESOLUTION_UNIT]
            if TIFF_TAG.RESOLUTION_UNIT in ifd_entries
            else 2
        )

        if resolution_unit == 1:  # aspect ratio only
            return 72
        # resolution_unit == 2 for inches, 3 for centimeters
        units_per_inch = 1 if resolution_unit == 2 else 2.54
        dots_per_unit = ifd_entries[resolution_tag]
        return int(round(dots_per_unit * units_per_inch))

    @classmethod
    def _make_stream_reader(cls, stream):
        """Return a |StreamReader| instance with wrapping `stream` and having "endian-
        ness" determined by the 'MM' or 'II' indicator in the TIFF stream header."""
        endian = cls._detect_endian(stream)
        return StreamReader(stream, endian)


class _IfdEntries:
    """Image File Directory for a TIFF image, having mapping (dict) semantics allowing
    "tag" values to be retrieved by tag code."""

    def __init__(self, entries):
        super(_IfdEntries, self).__init__()
        self._entries = entries

    def __contains__(self, key):
        """Provides ``in`` operator, e.g. ``tag in ifd_entries``"""
        return self._entries.__contains__(key)

    def __getitem__(self, key):
        """Provides indexed access, e.g. ``tag_value = ifd_entries[tag_code]``"""
        return self._entries.__getitem__(key)

    @classmethod
    def from_stream(cls, stream, offset):
        """Return a new |_IfdEntries| instance parsed from `stream` starting at
        `offset`."""
        ifd_parser = _IfdParser(stream, offset)
        entries = {e.tag: e.value for e in ifd_parser.iter_entries()}
        return cls(entries)

    def get(self, tag_code, default=None):
        """Return value of IFD entry having tag matching `tag_code`, or `default` if no
        matching tag found."""
        return self._entries.get(tag_code, default)


class _IfdParser:
    """Service object that knows how to extract directory entries from an Image File
    Directory (IFD)"""

    def __init__(self, stream_rdr, offset):
        super(_IfdParser, self).__init__()
        self._stream_rdr = stream_rdr
        self._offset = offset

    def iter_entries(self):
        """Generate an |_IfdEntry| instance corresponding to each entry in the
        directory."""
        for idx in range(self._entry_count):
            dir_entry_offset = self._offset + 2 + (idx * 12)
            ifd_entry = _IfdEntryFactory(self._stream_rdr, dir_entry_offset)
            yield ifd_entry

    @property
    def _entry_count(self):
        """The count of directory entries, read from the top of the IFD header."""
        return self._stream_rdr.read_short(self._offset)


def _IfdEntryFactory(stream_rdr, offset):
    """Return an |_IfdEntry| subclass instance containing the value of the directory
    entry at `offset` in `stream_rdr`."""
    ifd_entry_classes = {
        TIFF_FLD.ASCII: _AsciiIfdEntry,
        TIFF_FLD.SHORT: _ShortIfdEntry,
        TIFF_FLD.LONG: _LongIfdEntry,
        TIFF_FLD.RATIONAL: _RationalIfdEntry,
    }
    field_type = stream_rdr.read_short(offset, 2)
    EntryCls = ifd_entry_classes.get(field_type, _IfdEntry)
    return EntryCls.from_stream(stream_rdr, offset)


class _IfdEntry:
    """Base class for IFD entry classes.

    Subclasses are differentiated by value type, e.g. ASCII, long int, etc.
    """

    def __init__(self, tag_code, value):
        super(_IfdEntry, self).__init__()
        self._tag_code = tag_code
        self._value = value

    @classmethod
    def from_stream(cls, stream_rdr, offset):
        """Return an |_IfdEntry| subclass instance containing the tag and value of the
        tag parsed from `stream_rdr` at `offset`.

        Note this method is common to all subclasses. Override the ``_parse_value()``
        method to provide distinctive behavior based on field type.
        """
        tag_code = stream_rdr.read_short(offset, 0)
        value_count = stream_rdr.read_long(offset, 4)
        value_offset = stream_rdr.read_long(offset, 8)
        value = cls._parse_value(stream_rdr, offset, value_count, value_offset)
        return cls(tag_code, value)

    @classmethod
    def _parse_value(cls, stream_rdr, offset, value_count, value_offset):
        """Return the value of this field parsed from `stream_rdr` at `offset`.

        Intended to be overridden by subclasses.
        """
        return "UNIMPLEMENTED FIELD TYPE"  # pragma: no cover

    @property
    def tag(self):
        """Short int code that identifies this IFD entry."""
        return self._tag_code

    @property
    def value(self):
        """Value of this tag, its type being dependent on the tag."""
        return self._value


class _AsciiIfdEntry(_IfdEntry):
    """IFD entry having the form of a NULL-terminated ASCII string."""

    @classmethod
    def _parse_value(cls, stream_rdr, offset, value_count, value_offset):
        """Return the ASCII string parsed from `stream_rdr` at `value_offset`.

        The length of the string, including a terminating '\x00' (NUL) character, is in
        `value_count`.
        """
        return stream_rdr.read_str(value_count - 1, value_offset)


class _ShortIfdEntry(_IfdEntry):
    """IFD entry expressed as a short (2-byte) integer."""

    @classmethod
    def _parse_value(cls, stream_rdr, offset, value_count, value_offset):
        """Return the short int value contained in the `value_offset` field of this
        entry.

        Only supports single values at present.
        """
        if value_count == 1:
            return stream_rdr.read_short(offset, 8)
        else:  # pragma: no cover
            return "Multi-value short integer NOT IMPLEMENTED"


class _LongIfdEntry(_IfdEntry):
    """IFD entry expressed as a long (4-byte) integer."""

    @classmethod
    def _parse_value(cls, stream_rdr, offset, value_count, value_offset):
        """Return the long int value contained in the `value_offset` field of this
        entry.

        Only supports single values at present.
        """
        if value_count == 1:
            return stream_rdr.read_long(offset, 8)
        else:  # pragma: no cover
            return "Multi-value long integer NOT IMPLEMENTED"


class _RationalIfdEntry(_IfdEntry):
    """IFD entry expressed as a numerator, denominator pair."""

    @classmethod
    def _parse_value(cls, stream_rdr, offset, value_count, value_offset):
        """Return the rational (numerator / denominator) value at `value_offset` in
        `stream_rdr` as a floating-point number.

        Only supports single values at present.
        """
        if value_count == 1:
            numerator = stream_rdr.read_long(value_offset)
            denominator = stream_rdr.read_long(value_offset, 4)
            return numerator / denominator
        else:  # pragma: no cover
            return "Multi-value Rational NOT IMPLEMENTED"
