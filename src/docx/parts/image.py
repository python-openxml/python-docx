"""The proxy class for an image part, and related objects."""

from __future__ import annotations

import hashlib

from docx.image.image import Image
from docx.opc.part import Part
from docx.shared import Emu, Inches


class ImagePart(Part):
    """An image part.

    Corresponds to the target part of a relationship with type RELATIONSHIP_TYPE.IMAGE.
    """

    def __init__(
        self, partname: str, content_type: str, blob: bytes, image: Image | None = None
    ):
        super(ImagePart, self).__init__(partname, content_type, blob)
        self._image = image

    @property
    def default_cx(self):
        """Native width of this image, calculated from its width in pixels and
        horizontal dots per inch (dpi)."""
        px_width = self.image.px_width
        horz_dpi = self.image.horz_dpi
        width_in_inches = px_width / horz_dpi
        return Inches(width_in_inches)

    @property
    def default_cy(self):
        """Native height of this image, calculated from its height in pixels and
        vertical dots per inch (dpi)."""
        px_height = self.image.px_height
        horz_dpi = self.image.horz_dpi
        height_in_emu = 914400 * px_height / horz_dpi
        return Emu(height_in_emu)

    @property
    def filename(self):
        """Filename from which this image part was originally created.

        A generic name, e.g. 'image.png', is substituted if no name is available, for
        example when the image was loaded from an unnamed stream. In that case a default
        extension is applied based on the detected MIME type of the image.
        """
        if self._image is not None:
            return self._image.filename
        return "image.%s" % self.partname.ext

    @classmethod
    def from_image(cls, image, partname):
        """Return an |ImagePart| instance newly created from `image` and assigned
        `partname`."""
        return ImagePart(partname, image.content_type, image.blob, image)

    @property
    def image(self) -> Image:
        if self._image is None:
            self._image = Image.from_blob(self.blob)
        return self._image

    @classmethod
    def load(cls, partname, content_type, blob, package):
        """Called by ``docx.opc.package.PartFactory`` to load an image part from a
        package being opened by ``Document(...)`` call."""
        return cls(partname, content_type, blob)

    @property
    def sha1(self):
        """SHA1 hash digest of the blob of this image part."""
        return hashlib.sha1(self._blob).hexdigest()
