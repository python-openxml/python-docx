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

    @classmethod
    def _from_stream(cls, stream, blob, filename=None):
        """
        Return an instance of the |Image| subclass corresponding to the
        format of the image in *stream*.
        """
        # import at execution time to avoid circular import
        from docx.image import image_cls_that_can_parse
        ImageSubclass = image_cls_that_can_parse(stream)
        return ImageSubclass.from_stream(stream, blob, filename)
