# encoding: utf-8

"""
Objects related to parsing headers of JPEG image streams, both JFIF and Exif
sub-formats.
"""

from __future__ import absolute_import, division, print_function

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
    @classmethod
    def from_stream(cls, stream):
        """
        Return a |_JfifMarkers| instance containing a |_JfifMarker| instance
        for each marker in *stream*.
        """
        raise NotImplementedError

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
