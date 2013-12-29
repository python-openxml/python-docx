# encoding: utf-8

"""
The proxy class for an image part, and related objects.
"""

from __future__ import absolute_import, print_function, unicode_literals

import hashlib
import os

from docx.opc.package import Part
from docx.shared import lazyproperty


class Image(object):
    """
    A helper object that knows how to analyze an image file.
    """
    def __init__(self, blob, filename):
        super(Image, self).__init__()
        self._blob = blob
        self._filename = filename

    @property
    def blob(self):
        """
        The bytes of the image 'file'
        """
        return self._blob

    @property
    def content_type(self):
        """
        The MIME type of the image, e.g. 'image/png'.
        """
        raise NotImplementedError

    @property
    def filename(self):
        """
        Original image file name, if loaded from disk, or a generic filename
        if loaded from an anonymous stream.
        """
        return self._filename

    @classmethod
    def load(cls, image_descriptor):
        """
        Return a new |Image| instance loaded from the image file identified
        by *image_descriptor*, a path or file-like object.
        """
        if isinstance(image_descriptor, basestring):
            path = image_descriptor
            with open(path, 'rb') as f:
                blob = f.read()
            filename = os.path.basename(path)
        else:
            stream = image_descriptor
            stream.seek(0)
            blob = stream.read()
            filename = None
        return cls(blob, filename)

    @lazyproperty
    def sha1(self):
        """
        SHA1 hash digest of the image blob
        """
        return hashlib.sha1(self._blob).hexdigest()


class ImagePart(Part):
    """
    An image part. Corresponds to the target part of a relationship with type
    RELATIONSHIP_TYPE.IMAGE.
    """
    @property
    def filename(self):
        """
        Filename from which this image part was originally created. A generic
        name, e.g. 'image.png', is substituted if no name is available, for
        example when the image was loaded from an unnamed stream. In that
        case a default extension is applied based on the detected MIME type
        of the image.
        """
        raise NotImplementedError

    @classmethod
    def from_image(cls, image, partname):
        """
        Return an |ImagePart| instance newly created from *image* and
        assigned *partname*.
        """
        return ImagePart(partname, image.content_type, image.blob, image)

    @property
    def height(self):
        """
        Native height of this image, calculated from its height in pixels and
        vertical dots per inch (dpi) when available. Default values are
        silently substituted when specific values cannot be parsed from the
        binary image byte stream.
        """
        raise NotImplementedError

    @property
    def sha1(self):
        """
        SHA1 hash digest of the blob of this image part.
        """
        raise NotImplementedError

    @property
    def width(self):
        """
        Native width of this image, calculated from its width in pixels and
        horizontal dots per inch (dpi) when available. Default values are
        silently substituted when specific values cannot be parsed from the
        binary image byte stream.
        """
        raise NotImplementedError
