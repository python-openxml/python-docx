# encoding: utf-8

"""
The proxy class for an image part, and related objects.
"""

from __future__ import absolute_import, print_function, unicode_literals

from docx.opc.package import Part


class ImagePart(Part):
    """
    An image part. Corresponds to the target part of a relationship with type
    RELATIONSHIP_TYPE.IMAGE.
    """
