# encoding: utf-8

"""
Enumerations used in python-docx
"""

from __future__ import absolute_import, print_function, unicode_literals


class Enumeration(object):

    @classmethod
    def from_xml(cls, xml_val):
        return cls._xml_to_idx[xml_val]

    @classmethod
    def to_xml(cls, enum_val):
        return cls._idx_to_xml[enum_val]
