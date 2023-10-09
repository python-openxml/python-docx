"""Enumerations used in python-docx."""


class Enumeration:
    @classmethod
    def from_xml(cls, xml_val):
        return cls._xml_to_idx[xml_val]

    @classmethod
    def to_xml(cls, enum_val):
        return cls._idx_to_xml[enum_val]
