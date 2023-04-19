# encoding: utf-8

"""
The :mod:`pptx.opc.extendedprops` module defines the ExtendedProperties class, which
coheres around the concerns of reading and writing application document
properties to and from the app.xml part of a .docx file.
"""

from __future__ import absolute_import, division, print_function, unicode_literals


class ExtendedProperties(object):
    """
    Corresponds to part named ``/docProps/app.xml``, containing the extended
    document properties for this document package.
    """

    def __init__(self, element):
        self._element = element

    @property
    def total_time(self):
        return self._element[1].text

    @total_time.setter
    def total_time(self, value):
        self._element[1].text = value

    @property
    def template(self):
        return self._element[0].text

    @template.setter
    def template(self, value):
        self._element[0].text = value

    @property
    def pages(self):
        return self._element[2].text

    @pages.setter
    def pages(self, value):
        self._element[2].text = value

