# encoding: utf-8

"""WordprocessingML Package class and related objects"""

from __future__ import absolute_import, division, print_function, unicode_literals

from docx.image.image import Image
from docx.opc.constants import RELATIONSHIP_TYPE as RT
from docx.opc.package import OpcPackage
from docx.opc.packuri import PackURI
from docx.parts.image import ImagePart
from docx.shared import lazyproperty


class Package(OpcPackage):
    """Customizations specific to a WordprocessingML package"""

    def after_unmarshal(self):
        """Called by loading code after all parts and relationships have been loaded.

        This method affords the opportunity for any required post-processing.
        """
        self._gather_image_parts()

    def get_or_add_image_part(self, image_descriptor):
        """Return |ImagePart| containing image specified by *image_descriptor*.

        The image-part is newly created if a matching one is not already present in the
        collection.
        """
        return self.image_parts.get_or_add_image_part(image_descriptor)

    @lazyproperty
    def image_parts(self):
        """|ImageParts| collection object for this package."""
        return ImageParts()

    def _gather_image_parts(self):
        """Load the image part collection with all the image parts in package."""
        for rel in self.iter_rels():
            if rel.is_external:
                continue
            if rel.reltype != RT.IMAGE:
                continue
            if rel.target_part in self.image_parts:
                continue
            self.image_parts.append(rel.target_part)


class ImageParts(object):
    """Collection of |ImagePart| objects corresponding to images in the package"""

    def __init__(self):
        self._image_parts = []

    def __contains__(self, item):
        return self._image_parts.__contains__(item)

    def __iter__(self):
        return self._image_parts.__iter__()

    def __len__(self):
        return self._image_parts.__len__()

    def append(self, item):
        self._image_parts.append(item)

    def get_or_add_image_part(self, image_descriptor):
        """Return |ImagePart| object containing image identified by *image_descriptor*.

        The image-part is newly created if a matching one is not present in the
        collection.
        """
        image = Image.from_file(image_descriptor)
        matching_image_part = self._get_by_sha1(image.sha1)
        if matching_image_part is not None:
            return matching_image_part
        return self._add_image_part(image)

    def _add_image_part(self, image):
        """
        Return an |ImagePart| instance newly created from image and appended
        to the collection.
        """
        partname = self._next_image_partname(image.ext)
        image_part = ImagePart.from_image(image, partname)
        self.append(image_part)
        return image_part

    def _get_by_sha1(self, sha1):
        """
        Return the image part in this collection having a SHA1 hash matching
        *sha1*, or |None| if not found.
        """
        for image_part in self._image_parts:
            if image_part.sha1 == sha1:
                return image_part
        return None

    def _next_image_partname(self, ext):
        """
        The next available image partname, starting from
        ``/word/media/image1.{ext}`` where unused numbers are reused. The
        partname is unique by number, without regard to the extension. *ext*
        does not include the leading period.
        """
        def image_partname(n):
            return PackURI('/word/media/image%d.%s' % (n, ext))
        used_numbers = [image_part.partname.idx for image_part in self]
        for n in range(1, len(self)+1):
            if n not in used_numbers:
                return image_partname(n)
        return image_partname(len(self)+1)
