# encoding: utf-8

"""
WordprocessingML Package class and related objects
"""

from __future__ import absolute_import, print_function, unicode_literals

from docx.opc.constants import RELATIONSHIP_TYPE as RT
from docx.opc.package import OpcPackage
from docx.shared import lazyproperty


class Package(OpcPackage):
    """
    Customizations specific to a WordprocessingML package.
    """
    def after_unmarshal(self):
        """
        Called by loading code after all parts and relationships have been
        loaded, to afford the opportunity for any required post-processing.
        """
        self._gather_image_parts()

    @lazyproperty
    def image_parts(self):
        """
        Collection of all image parts in this package.
        """
        return ImageParts()

    def _gather_image_parts(self):
        """
        Load the image part collection with all the image parts in package.
        """
        for rel in self.iter_rels():
            if rel.is_external:
                continue
            if rel.reltype != RT.IMAGE:
                continue
            if rel.target_part in self.image_parts:
                continue
            self.image_parts.append(rel.target_part)


class ImageParts(object):
    """
    Collection of |ImagePart| instances containing all the image parts in the
    package.
    """
    def __init__(self):
        super(ImageParts, self).__init__()
        self._image_parts = []

    def __contains__(self, item):
        return self._image_parts.__contains__(item)

    def __len__(self):
        return self._image_parts.__len__()

    def append(self, item):
        self._image_parts.append(item)

    def get_or_add_image_part(self, image_descriptor):
        """
        Return an |ImagePart| instance containing the image identified by
        *image_descriptor*, newly created if a matching one is not present in
        the collection.
        """
