# encoding: utf-8

"""
The :mod:`pptx.opc.extendedprops` module defines the ExtendedProperties class, which
coheres around the concerns of reading and writing application document
properties to and from the app.xml part of a .docx file.
"""

from __future__ import absolute_import, division, print_function, unicode_literals

import re


def _get_property_name_from_tag(tag):
    name = tag.split('}')[-1]
    snake_name = ''.join(['_' + i.lower() if i.isupper() else i for i in name]).lstrip('_')
    return snake_name


class ExtendedProperties(object):
    """
    Corresponds to part named ``/docProps/app.xml``, containing the extended
    document properties for this document package.
    """

    def __init__(self, element):
        self._element = element
        self.template = None
        self.manager = None
        self.company = None
        self.pages = None
        self.words = None
        self.characters = None
        self.presentation_format = None
        self.lines = None
        self.paragraphs = None
        self.slides = None
        self.notes = None
        self.total_time = None
        self.hidden_slides = None
        self.mm_clips = None
        self.scale_crop = None
        self.heading_pairs = None
        self.titles_of_parts = None
        self.links_up_to_date = None
        self.characters_with_space = None
        self.shared_doc = None
        self.hyperlink_base = None
        self.h_links = None
        self.hyperlinks_changed = None
        self.dig_sig = None
        self.application = None
        self.app_version = None
        self.doc_security = None
        self._property_elements = {}

        for child in self._element:
            property_name = _get_property_name_from_tag(child.tag)
            if hasattr(self, property_name):
                setattr(self, property_name, child.text)
                self._property_elements[property_name] = child

    def set_property(self, property_name, value):
        if hasattr(self, property_name):
            xml_element = self._property_elements.get(property_name)
            if xml_element is not None:
                xml_element.text = value
                setattr(self, property_name, value)
            else:
                raise AttributeError(f"XML element not found for property '{property_name}'.")
        else:
            raise AttributeError(f"Property '{property_name}' not found in ExtendedProperties.")

    # @property
    # def total_time(self):
    #     return self._element[1].text
    #
    # @total_time.setter
    # def total_time(self, value):
    #     self._element[1].text = value
    #
    # @property
    # def template(self):
    #     return self._element[0].text
    #
    # @template.setter
    # def template(self, value):
    #     self._element[0].text = value
    #
    # @property
    # def pages(self):
    #     return self._element[2].text
    #
    # @pages.setter
    # def pages(self, value):
    #     self._element[2].text = value

