# encoding: utf-8

"""
The proxy class for an image part, and related objects.
"""

from __future__ import absolute_import, print_function, unicode_literals

from docx.opc.package import Part


class Image(object):
    """
    A helper object that knows how to analyze an image file.
    """
    @classmethod
    def load(self, image_descriptor):
        """
        Return a new |Image| instance loaded from the image file identified
        by *image_descriptor*, a path or file-like object.
        """

    @property
    def sha1(self):
        """
        SHA1 hash digest of the image blob
        """
        raise NotImplementedError


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
