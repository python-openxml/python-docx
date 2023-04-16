# encoding: utf-8

"""
The :mod:`pptx.opc.appprops` module defines the AppProperties class, which
coheres around the concerns of reading and writing application document
properties to and from the app.xml part of a .pptx file.
"""

from __future__ import absolute_import, division, print_function, unicode_literals

class AppProperties(object):
    """
    Corresponds to part named ``/docProps/app.xml``, containing the app
    document properties for this document package.
    """
    def __init__(self, element):
        self._element = element

    @property
    def template(self):
        return self._element.template_text

    @template.setter
    def template(self, value):
        self._element.template_text = value
    
    @property
    def template_text(self):
        return self._element.template

    @template_text.setter
    def template_text(self, value):
        self._element.template = value