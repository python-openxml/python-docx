# encoding: utf-8

"""
WordprocessingML Package class and related objects
"""

from __future__ import absolute_import, print_function, unicode_literals

from docx.opc.package import OpcPackage


class Package(OpcPackage):
    """
    Customizations specific to a WordprocessingML package.
    """
    @property
    def image_parts(self):
        """
        Collection of all image parts in this package.
        """


class ImageParts(object):
    """
    Collection of |ImagePart| instances containing all the image parts in the
    package.
    """
    def get_or_add_image_part(self, image_descriptor):
        """
        Return an |ImagePart| instance containing the image identified by
        *image_descriptor*, newly created if a matching one is not present in
        the collection.
        """
