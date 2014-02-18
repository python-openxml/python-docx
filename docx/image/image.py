# encoding: utf-8

"""
Provides objects that can characterize image streams as to content type and
size, as a required step in including them in a document.
"""

from __future__ import absolute_import, division, print_function

import hashlib
import os

from ..compat import BytesIO, is_string
from ..shared import lazyproperty
from .exceptions import UnrecognizedImageError


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
    def from_blob(cls, blob):
        """
        Return a new |Image| subclass instance parsed from the image binary
        contained in *blob*.
        """
        stream = BytesIO(blob)
        return cls._from_stream(stream, blob)

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
    def blob(self):
        """
        The bytes of the image 'file'
        """
        return self._blob

    @property
    def content_type(self):
        """
        MIME content type for this image, e.g. ``'image/jpeg'`` for a JPEG
        image
        """
        return self._image_header.content_type

    @lazyproperty
    def ext(self):
        """
        The file extension for the image. If an actual one is available from
        a load filename it is used. Otherwise a canonical extension is
        assigned based on the content type. Does not contain the leading
        period, e.g. 'jpg', not '.jpg'.
        """
        return os.path.splitext(self._filename)[1][1:]

    @property
    def filename(self):
        """
        Original image file name, if loaded from disk, or a generic filename
        if loaded from an anonymous stream.
        """
        return self._filename

    @property
    def px_width(self):
        """
        The horizontal pixel dimension of the image
        """
        return self._image_header.px_width

    @property
    def px_height(self):
        """
        The vertical pixel dimension of the image
        """
        return self._image_header.px_height

    @property
    def horz_dpi(self):
        """
        Integer dots per inch for the width of this image. Defaults to 72
        when not present in the file, as is often the case.
        """
        return self._image_header.horz_dpi

    @property
    def vert_dpi(self):
        """
        Integer dots per inch for the height of this image. Defaults to 72
        when not present in the file, as is often the case.
        """
        return self._image_header.vert_dpi

    @lazyproperty
    def sha1(self):
        """
        SHA1 hash digest of the image blob
        """
        return hashlib.sha1(self._blob).hexdigest()

    @classmethod
    def _from_stream(cls, stream, blob, filename=None):
        """
        Return an instance of the |Image| subclass corresponding to the
        format of the image in *stream*.
        """
        image_header = _ImageHeaderFactory(stream)
        if filename is None:
            filename = 'image.%s' % image_header.default_ext
        return cls(blob, filename, image_header)


def _ImageHeaderFactory(stream):
    """
    Return a |BaseImageHeader| subclass instance that knows how to parse the
    headers of the image in *stream*.
    """
    from docx.image import SIGNATURES

    def read_32(stream):
        stream.seek(0)
        return stream.read(32)

    header = read_32(stream)
    for cls, offset, signature_bytes in SIGNATURES:
        end = offset + len(signature_bytes)
        found_bytes = header[offset:end]
        if found_bytes == signature_bytes:
            return cls.from_stream(stream)
    raise UnrecognizedImageError


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
    def content_type(self):
        """
        Abstract property definition, must be implemented by all subclasses.
        """
        msg = (
            'content_type property must be implemented by all subclasses of '
            'BaseImageHeader'
        )
        raise NotImplementedError(msg)

    @property
    def default_ext(self):
        """
        Default filename extension for images of this type. An abstract
        property definition, must be implemented by all subclasses.
        """
        msg = (
            'default_ext property must be implemented by all subclasses of '
            'BaseImageHeader'
        )
        raise NotImplementedError(msg)

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
