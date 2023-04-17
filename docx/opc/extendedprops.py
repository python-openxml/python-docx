# encoding: utf-8

"""
The :mod:`pptx.opc.appprops` module defines the AppProperties class, which
coheres around the concerns of reading and writing application document
properties to and from the app.xml part of a .pptx file.
"""

from __future__ import absolute_import, division, print_function, unicode_literals


# Getting error 'AttributeError("'lxml.etree._Element' object has no attribute 'template_text'")'
class ExtendedProperties(object):
    """
    Corresponds to part named ``/docProps/app.xml``, containing the app
    document properties for this document package.
    """
    def __init__(self, element):
        self._element = element[1]

    @property
    def total_time(self):
        return self._element.text

    @total_time.setter
    def total_time(self, value):
        self._element.text = value
