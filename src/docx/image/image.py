"""Provides objects that can characterize image streams.

That characterization is as to content type and size, as a required step in including
them in a document.
"""

from __future__ import annotations

import hashlib
import io
import os
from typing import IO, Tuple

from docx.image.exceptions import UnrecognizedImageError
from docx.shared import Emu, Inches, Length, lazyproperty


class Image:
    """Graphical image stream such as JPEG, PNG, or GIF with properties and methods
    required by ImagePart."""

    def __init__(self, blob: bytes, filename: str, image_header: BaseImageHeader):
        super(Image, self).__init__()
        self._blob = blob
        self._filename = filename
        self._image_header = image_header

    @classmethod
    def from_blob(cls, blob: bytes) -> Image:
        """Return a new |Image| subclass instance parsed from the image binary contained
        in `blob`."""
        stream = io.BytesIO(blob)
        return cls._from_stream(stream, blob)

    @classmethod
    def from_file(cls, image_descriptor: str | IO[bytes]):
        """Return a new |Image| subclass instance loaded from the image file identified
        by `image_descriptor`, a path or file-like object."""
        if isinstance(image_descriptor, str):
            path = image_descriptor
            with open(path, "rb") as f:
                blob = f.read()
                stream = io.BytesIO(blob)
            filename = os.path.basename(path)
        else:
            stream = image_descriptor
            stream.seek(0)
            blob = stream.read()
            filename = None
        return cls._from_stream(stream, blob, filename)

    @property
    def blob(self):
        """The bytes of the image 'file'."""
        return self._blob

    @property
    def content_type(self) -> str:
        """MIME content type for this image, e.g. ``'image/jpeg'`` for a JPEG image."""
        return self._image_header.content_type

    @lazyproperty
    def ext(self):
        """The file extension for the image.

        If an actual one is available from a load filename it is used. Otherwise a
        canonical extension is assigned based on the content type. Does not contain the
        leading period, e.g. 'jpg', not '.jpg'.
        """
        return os.path.splitext(self._filename)[1][1:]

    @property
    def filename(self):
        """Original image file name, if loaded from disk, or a generic filename if
        loaded from an anonymous stream."""
        return self._filename

    @property
    def px_width(self) -> int:
        """The horizontal pixel dimension of the image."""
        return self._image_header.px_width

    @property
    def px_height(self) -> int:
        """The vertical pixel dimension of the image."""
        return self._image_header.px_height

    @property
    def horz_dpi(self) -> int:
        """Integer dots per inch for the width of this image.

        Defaults to 72 when not present in the file, as is often the case.
        """
        return self._image_header.horz_dpi

    @property
    def vert_dpi(self) -> int:
        """Integer dots per inch for the height of this image.

        Defaults to 72 when not present in the file, as is often the case.
        """
        return self._image_header.vert_dpi

    @property
    def width(self) -> Inches:
        """A |Length| value representing the native width of the image, calculated from
        the values of `px_width` and `horz_dpi`."""
        return Inches(self.px_width / self.horz_dpi)

    @property
    def height(self) -> Inches:
        """A |Length| value representing the native height of the image, calculated from
        the values of `px_height` and `vert_dpi`."""
        return Inches(self.px_height / self.vert_dpi)

    def scaled_dimensions(
        self, width: int | Length | None = None, height: int | Length | None = None
    ) -> Tuple[Length, Length]:
        """(cx, cy) pair representing scaled dimensions of this image.

        The native dimensions of the image are scaled by applying the following rules to
        the `width` and `height` arguments.

        * If both `width` and `height` are specified, the return value is (`width`,
        `height`); no scaling is performed.
        * If only one is specified, it is used to compute a scaling factor that is then
        applied to the unspecified dimension, preserving the aspect ratio of the image.
        * If both `width` and `height` are |None|, the native dimensions are returned.

        The native dimensions are calculated using the dots-per-inch (dpi) value
        embedded in the image, defaulting to 72 dpi if no value is specified, as is
        often the case. The returned values are both |Length| objects.
        """
        if width is None and height is None:
            return self.width, self.height

        if width is None:
            assert height is not None
            scaling_factor = float(height) / float(self.height)
            width = round(self.width * scaling_factor)

        if height is None:
            scaling_factor = float(width) / float(self.width)
            height = round(self.height * scaling_factor)

        return Emu(width), Emu(height)

    @lazyproperty
    def sha1(self):
        """SHA1 hash digest of the image blob."""
        return hashlib.sha1(self._blob).hexdigest()

    @classmethod
    def _from_stream(
        cls,
        stream: IO[bytes],
        blob: bytes,
        filename: str | None = None,
    ) -> Image:
        """Return an instance of the |Image| subclass corresponding to the format of the
        image in `stream`."""
        image_header = _ImageHeaderFactory(stream)
        if filename is None:
            filename = "image.%s" % image_header.default_ext
        return cls(blob, filename, image_header)


def _ImageHeaderFactory(stream: IO[bytes]):
    """A |BaseImageHeader| subclass instance that can parse headers of image in `stream`."""
    from docx.image import SIGNATURES

    def read_32(stream: IO[bytes]):
        stream.seek(0)
        return stream.read(32)

    header = read_32(stream)
    for cls, offset, signature_bytes in SIGNATURES:
        end = offset + len(signature_bytes)
        found_bytes = header[offset:end]
        if found_bytes == signature_bytes:
            return cls.from_stream(stream)
    raise UnrecognizedImageError


class BaseImageHeader:
    """Base class for image header subclasses like |Jpeg| and |Tiff|."""

    def __init__(self, px_width: int, px_height: int, horz_dpi: int, vert_dpi: int):
        self._px_width = px_width
        self._px_height = px_height
        self._horz_dpi = horz_dpi
        self._vert_dpi = vert_dpi

    @property
    def content_type(self) -> str:
        """Abstract property definition, must be implemented by all subclasses."""
        msg = "content_type property must be implemented by all subclasses of " "BaseImageHeader"
        raise NotImplementedError(msg)

    @property
    def default_ext(self) -> str:
        """Default filename extension for images of this type.

        An abstract property definition, must be implemented by all subclasses.
        """
        raise NotImplementedError(
            "default_ext property must be implemented by all subclasses of " "BaseImageHeader"
        )

    @property
    def px_width(self):
        """The horizontal pixel dimension of the image."""
        return self._px_width

    @property
    def px_height(self):
        """The vertical pixel dimension of the image."""
        return self._px_height

    @property
    def horz_dpi(self):
        """Integer dots per inch for the width of this image.

        Defaults to 72 when not present in the file, as is often the case.
        """
        return self._horz_dpi

    @property
    def vert_dpi(self):
        """Integer dots per inch for the height of this image.

        Defaults to 72 when not present in the file, as is often the case.
        """
        return self._vert_dpi
