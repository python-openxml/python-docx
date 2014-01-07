# encoding: utf-8

"""
The proxy class for an image part, and related objects.
"""

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

import hashlib
import os

try:
    from PIL import Image as PIL_Image
except ImportError:
    import Image as PIL_Image

from docx.compat import BytesIO, is_string
from docx.opc.constants import CONTENT_TYPE as CT
from docx.opc.package import Part
from docx.shared import Emu, Inches, lazyproperty


class Image(object):
    """
    A helper object that knows how to analyze an image file.
    """
    def __init__(
            self, blob, filename, content_type, px_width, px_height,
            horz_dpi, vert_dpi):
        super(Image, self).__init__()
        self._blob = blob
        self._filename = filename
        self._content_type = content_type
        self._px_width = px_width
        self._px_height = px_height
        self._horz_dpi = horz_dpi
        self._vert_dpi = vert_dpi

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
        return self._content_type

    @lazyproperty
    def ext(self):
        """
        The file extension for the image. If an actual one is available from
        a load filename it is used. Otherwise a canonical extension is
        assigned based on the content type.
        """
        return os.path.splitext(self._filename)[1]

    @property
    def filename(self):
        """
        Original image file name, if loaded from disk, or a generic filename
        if loaded from an anonymous stream.
        """
        return self._filename

    @classmethod
    def from_blob(cls, blob):
        stream = BytesIO(blob)
        return cls._from_stream(stream, blob)

    @classmethod
    def from_file(cls, image_descriptor):
        """
        Return a new |Image| instance loaded from the image file identified
        by *image_descriptor*, a path or file-like object.
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
    def horz_dpi(self):
        """
        The horizontal dots per inch (dpi) of the image, defaults to 72 when
        no dpi information is stored in the image, as is often the case.
        """
        return self._horz_dpi

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

    @lazyproperty
    def sha1(self):
        """
        SHA1 hash digest of the image blob
        """
        return hashlib.sha1(self._blob).hexdigest()

    @property
    def vert_dpi(self):
        """
        The vertical dots per inch (dpi) of the image, defaults to 72 when no
        dpi information is stored in the image.
        """
        return self._vert_dpi

    @classmethod
    def _analyze_image(cls, stream):
        pil_image = cls._open_pillow_image(stream)
        content_type = cls._format_content_type(pil_image.format)
        px_width, px_height = pil_image.size
        try:
            horz_dpi, vert_dpi = pil_image.info.get('dpi')
        except:
            horz_dpi, vert_dpi = (72, 72)
        return content_type, px_width, px_height, horz_dpi, vert_dpi

    @classmethod
    def _def_mime_ext(cls, mime_type):
        """
        Return the default file extension, e.g. ``'.png'``, corresponding to
        *mime_type*. Raises |KeyError| for unsupported image types.
        """
        content_type_extensions = {
            CT.BMP: '.bmp', CT.GIF: '.gif', CT.JPEG: '.jpg', CT.PNG: '.png',
            CT.TIFF: '.tiff', CT.X_WMF: '.wmf'
        }
        return content_type_extensions[mime_type]

    @classmethod
    def _format_content_type(cls, format):
        """
        Return the content type string (MIME type for images) corresponding
        to the Pillow image format string *format*.
        """
        format_content_types = {
            'BMP': CT.BMP, 'GIF': CT.GIF, 'JPEG': CT.JPEG, 'PNG': CT.PNG,
            'TIFF': CT.TIFF, 'WMF': CT.X_WMF
        }
        return format_content_types[format]

    @classmethod
    def _from_stream(cls, stream, blob, filename=None):
        content_type, px_width, px_height, horz_dpi, vert_dpi = (
            cls._analyze_image(stream)
        )
        if filename is None:
            filename = 'image%s' % cls._def_mime_ext(content_type)
        return cls(
            blob, filename, content_type, px_width, px_height, horz_dpi,
            vert_dpi
        )

    @classmethod
    def _open_pillow_image(cls, stream):
        """
        Return a Pillow ``Image`` instance loaded from the image file-like
        object *stream*. The image is validated to confirm it is a supported
        image type.
        """
        stream.seek(0)
        pil_image = PIL_Image.open(stream)
        try:
            cls._format_content_type(pil_image.format)
        except KeyError:
            tmpl = "unsupported image format '%s'"
            raise ValueError(tmpl % (pil_image.format))
        return pil_image


class ImagePart(Part):
    """
    An image part. Corresponds to the target part of a relationship with type
    RELATIONSHIP_TYPE.IMAGE.
    """
    def __init__(self, partname, content_type, blob, image=None):
        super(ImagePart, self).__init__(partname, content_type, blob)
        self._image = image

    @property
    def default_cx(self):
        """
        Native width of this image, calculated from its width in pixels and
        horizontal dots per inch (dpi).
        """
        px_width = self.image.px_width
        horz_dpi = self.image.horz_dpi
        width_in_inches = px_width / horz_dpi
        return Inches(width_in_inches)

    @property
    def default_cy(self):
        """
        Native height of this image, calculated from its height in pixels and
        vertical dots per inch (dpi).
        """
        px_height = self.image.px_height
        horz_dpi = self.image.horz_dpi
        height_in_emu = 914400 * px_height / horz_dpi
        return Emu(height_in_emu)

    @property
    def filename(self):
        """
        Filename from which this image part was originally created. A generic
        name, e.g. 'image.png', is substituted if no name is available, for
        example when the image was loaded from an unnamed stream. In that
        case a default extension is applied based on the detected MIME type
        of the image.
        """
        if self._image is not None:
            return self._image.filename
        return 'image%s' % self.partname.ext

    @classmethod
    def from_image(cls, image, partname):
        """
        Return an |ImagePart| instance newly created from *image* and
        assigned *partname*.
        """
        return ImagePart(partname, image.content_type, image.blob, image)

    @property
    def image(self):
        if self._image is None:
            self._image = Image.from_blob(self.blob)
        return self._image

    @classmethod
    def load(cls, partname, content_type, blob, package):
        """
        Called by ``docx.opc.package.PartFactory`` to load an image part from
        a package being opened by ``Document(...)`` call.
        """
        return cls(partname, content_type, blob)

    @property
    def sha1(self):
        """
        SHA1 hash digest of the blob of this image part.
        """
        raise NotImplementedError
