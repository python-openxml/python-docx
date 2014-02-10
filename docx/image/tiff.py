# encoding: utf-8

from __future__ import absolute_import, division, print_function

from .image import Image


class Tiff(Image):
    """
    Image header parser for TIFF images. Handles both big and little endian
    byte ordering.
    """
    @classmethod
    def from_stream(cls, stream, blob, filename):
        """
        Return a |Tiff| instance containing the properties of the TIFF image
        in *stream*.
        """
        parser = _TiffParser.parse(stream)
        px_width = parser.px_width
        px_height = parser.px_height
        horz_dpi = parser.horz_dpi
        vert_dpi = parser.vert_dpi
        return cls(blob, filename, px_width, px_height, horz_dpi, vert_dpi)


class _TiffParser(object):
    """
    Parses a TIFF image stream to extract the image properties found in its
    main image file directory (IFD)
    """
    def __init__(self, ifd):
        super(_TiffParser, self).__init__()
        self._ifd = ifd

    @classmethod
    def parse(cls, stream):
        """
        Return an instance of |_TiffParser| containing the properties parsed
        from the TIFF image in *stream*.
        """
        stream_rdr = cls._make_stream_reader(stream)
        ifd0_offset = stream_rdr.read_long(4)
        ifd_entries = _IfdEntries.from_stream(stream_rdr, ifd0_offset)
        return cls(ifd_entries)

    @property
    def horz_dpi(self):
        """
        The horizontal dots per inch value calculated from the XResolution
        and ResolutionUnit tags of the IFD; defaults to 72 if those tags are
        not present.
        """
        raise NotImplementedError

    @property
    def px_height(self):
        """
        The number of stacked rows of pixels in the image, |None| if the IFD
        contains no ``ImageLength`` tag, the expected case when the TIFF is
        embeded in an Exif image.
        """
        raise NotImplementedError

    @property
    def px_width(self):
        """
        The number of pixels in each row in the image, |None| if the IFD
        contains no ``ImageWidth`` tag, the expected case when the TIFF is
        embeded in an Exif image.
        """
        raise NotImplementedError

    @property
    def vert_dpi(self):
        """
        The vertical dots per inch value calculated from the XResolution and
        ResolutionUnit tags of the IFD; defaults to 72 if those tags are not
        present.
        """
        raise NotImplementedError

    @classmethod
    def _make_stream_reader(cls, stream):
        """
        Return a |StreamReader| instance with wrapping *stream* and having
        "endian-ness" determined by the 'MM' or 'II' indicator in the TIFF
        stream header.
        """
        raise NotImplementedError


class _IfdEntries(object):
    """
    Image File Directory for a TIFF image, having mapping (dict) semantics
    allowing "tag" values to be retrieved by tag code.
    """
    @classmethod
    def from_stream(cls, stream, offset):
        """
        Return a new |_IfdEntries| instance parsed from *stream* starting at
        *offset*.
        """
        raise NotImplementedError
