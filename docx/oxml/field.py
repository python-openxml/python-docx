# encoding: utf-8
"""
Custom element classes related to field codes (CT_Simplefield).
"""

from docx.enum.fields import WD_FIELD_TYPE
from docx.oxml.simpletypes import ST_OnOff, ST_String
from docx.oxml.xmlchemy import BaseOxmlElement, OptionalAttribute, RequiredAttribute
from docx.shared import lazyproperty


class CT_SimpleField(BaseOxmlElement):
    """
    `<w:fldSimple>` element, indicating a simple field character.
    """

    instr = RequiredAttribute("w:instr", ST_String)
    fldLock = OptionalAttribute("w:fldLock", ST_OnOff)
    dirty = OptionalAttribute("w:dirty", ST_OnOff)

    @lazyproperty
    def _fieldparts(self):
        """Split the field between its FieldType and its switches."""
        return self.instr.split(" ")

    @property
    def field(self):
        """Get the field and convert it to its enumeration counterpart."""
        field = self._fieldparts[0]
        return WD_FIELD_TYPE.from_xml(field)

    @property
    def switches(self):
        """Get the switches from the field instruction."""
        switches = self._fieldparts[1:]
        return switches
