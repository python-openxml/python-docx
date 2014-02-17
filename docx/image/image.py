# encoding: utf-8

"""
Provides objects that can characterize image streams as to content type and
size, as a required step in including them in a document.
"""

from __future__ import absolute_import, division, print_function

import os

from docx.compat import BytesIO, is_string


class Image(object):
    """
    Graphical image stream such as JPEG, PNG, or GIF with properties and
    methods required by ImagePart.
    """
    def __init__(self, blob, filename, image_header):
        super(Image, self).__init__()
        self._blob = blob
        self._filename = filename
        self._image_header = image_header

    @classmethod
    def from_file(cls, image_descriptor):
        """
        Return a new |Image| subclass instance loaded from the image file
        identified by *image_descriptor*, a path or file-like object.
        """
        if is_string(image_descriptor):
            path = image_descriptor
            with open(path, 'rb') as f:
                blob = f.read()
                stream = BytesIO(blob)
            filename = os.path.basename(path)
        else:
            stream = image_descriptor
            stream.seek(0)
            blob = stream.read()
            filename = None
        return cls._from_stream(stream, blob, filename)

    @property
    def px_width(self):
        """
        The horizontal pixel dimension of the image
        """
        return self._px_width

    @property
    def px_height(self):
        """
        The vertical pixel dimension of the image
        """
        return self._px_height

    @classmethod
    def _from_stream(cls, stream, blob, filename=None):
        """
        Return an instance of the |Image| subclass corresponding to the
        format of the image in *stream*.
        """
        image_header = _ImageHeaderFactory(stream)
        return cls(blob, filename, image_header)


def _ImageHeaderFactory(stream):
    """
    Return a |BaseImageHeader| subclass instance that knows how to parse the
    headers of the image in *stream*.
    """
    raise NotImplementedError


class BaseImageHeader(object):
    """
    Base class for image header subclasses like |Jpeg| and |Tiff|.
    """
    def __init__(self, px_width, px_height, horz_dpi, vert_dpi):
        self._px_width = px_width
        self._px_height = px_height
        self._horz_dpi = horz_dpi
        self._vert_dpi = vert_dpi

    @property
    def px_width(self):
        """
        The horizontal pixel dimension of the image
        """
        return self._px_width

    @property
    def px_height(self):
        """
        The vertical pixel dimension of the image
        """
        return self._px_height

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
