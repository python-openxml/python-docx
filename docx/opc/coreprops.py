# encoding: utf-8

"""
The :mod:`pptx.packaging` module coheres around the concerns of reading and
writing presentations to and from a .pptx file.
"""

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)


class CoreProperties(object):
    """
    Corresponds to part named ``/docProps/core.xml``, containing the core
    document properties for this document package.
    """
    def __init__(self, element):
        self._element = element
