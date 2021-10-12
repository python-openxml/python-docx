"""FieldType-related proxy types."""

from __future__ import absolute_import, division, print_function, unicode_literals

from docx.shared import ElementProxy


class Field(ElementProxy):
    """
    A individual (non-evaluated) field code.
    """

    __slots__ = ("_field",)

    def __init__(self, element):
        super(Field, self).__init__(element, None)
        self._field = element

    @property
    def instruction(self):
        """Return field instruction as found in element."""
        return self._field.instr

    @property
    def field(self):
        """Return fieldtype."""
        return self._field.field

    @property
    def switches(self):
        """Return applied field switches."""
        return self._field.switches
