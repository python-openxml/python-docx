# encoding: utf-8

"""
Simple type classes, providing validation and format translation for values
stored in XML element attributes. Naming generally corresponds to the simple
type in the associated XML schema.
"""

from __future__ import absolute_import, division, print_function, unicode_literals

from ..exceptions import InvalidXmlError
from ..shared import Emu, Pt, RGBColor, Twips


class BaseSimpleType(object):
    @classmethod
    def from_xml(cls, str_value):
        return cls.convert_from_xml(str_value)

    @classmethod
    def to_xml(cls, value):
        cls.validate(value)
        str_value = cls.convert_to_xml(value)
        return str_value

    @classmethod
    def validate_int(cls, value):
        if not isinstance(value, int):
            raise TypeError("value must be <type 'int'>, got %s" % type(value))

    @classmethod
    def validate_int_in_range(cls, value, min_inclusive, max_inclusive):
        cls.validate_int(value)
        if value < min_inclusive or value > max_inclusive:
            raise ValueError(
                "value must be in range %d to %d inclusive, got %d"
                % (min_inclusive, max_inclusive, value)
            )

    @classmethod
    def validate_string(cls, value):
        if isinstance(value, str):
            return value
        try:
            if isinstance(value, basestring):
                return value
        except NameError:  # means we're on Python 3
            pass
        raise TypeError("value must be a string, got %s" % type(value))


class BaseIntType(BaseSimpleType):
    @classmethod
    def convert_from_xml(cls, str_value):
        return int(str_value)

    @classmethod
    def convert_to_xml(cls, value):
        return str(value)

    @classmethod
    def validate(cls, value):
        cls.validate_int(value)


class BaseStringType(BaseSimpleType):
    @classmethod
    def convert_from_xml(cls, str_value):
        return str_value

    @classmethod
    def convert_to_xml(cls, value):
        return value

    @classmethod
    def validate(cls, value):
        cls.validate_string(value)


class BaseStringEnumerationType(BaseStringType):
    @classmethod
    def validate(cls, value):
        cls.validate_string(value)
        if value not in cls._members:
            raise ValueError("must be one of %s, got '%s'" % (cls._members, value))


class XsdAnyUri(BaseStringType):
    """
    There's a regular expression this is supposed to meet but so far thinking
    spending cycles on validating wouldn't be worth it for the number of
    programming errors it would catch.
    """


class XsdBoolean(BaseSimpleType):
    @classmethod
    def convert_from_xml(cls, str_value):
        if str_value not in ("1", "0", "true", "false"):
            raise InvalidXmlError(
                "value must be one of '1', '0', 'true' or 'false', got '%s'" % str_value
            )
        return str_value in ("1", "true")

    @classmethod
    def convert_to_xml(cls, value):
        return {True: "1", False: "0"}[value]

    @classmethod
    def validate(cls, value):
        if value not in (True, False):
            raise TypeError(
                "only True or False (and possibly None) may be assigned, got"
                " '%s'" % value
            )


class XsdId(BaseStringType):
    """
    String that must begin with a letter or underscore and cannot contain any
    colons. Not fully validated because not used in external API.
    """

    pass


class XsdInt(BaseIntType):
    @classmethod
    def validate(cls, value):
        cls.validate_int_in_range(value, -2147483648, 2147483647)


class XsdLong(BaseIntType):
    @classmethod
    def validate(cls, value):
        cls.validate_int_in_range(value, -9223372036854775808, 9223372036854775807)


class XsdString(BaseStringType):
    pass


class XsdStringEnumeration(BaseStringEnumerationType):
    """
    Set of enumerated xsd:string values.
    """


class XsdToken(BaseStringType):
    """
    xsd:string with whitespace collapsing, e.g. multiple spaces reduced to
    one, leading and trailing space stripped.
    """

    pass


class XsdUnsignedInt(BaseIntType):
    @classmethod
    def validate(cls, value):
        cls.validate_int_in_range(value, 0, 4294967295)


class XsdUnsignedLong(BaseIntType):
    @classmethod
    def validate(cls, value):
        cls.validate_int_in_range(value, 0, 18446744073709551615)


class ST_BrClear(XsdString):
    @classmethod
    def validate(cls, value):
        cls.validate_string(value)
        valid_values = ("none", "left", "right", "all")
        if value not in valid_values:
            raise ValueError("must be one of %s, got '%s'" % (valid_values, value))


class ST_BrType(XsdString):
    @classmethod
    def validate(cls, value):
        cls.validate_string(value)
        valid_values = ("page", "column", "textWrapping")
        if value not in valid_values:
            raise ValueError("must be one of %s, got '%s'" % (valid_values, value))


class ST_Coordinate(BaseIntType):
    @classmethod
    def convert_from_xml(cls, str_value):
        if "i" in str_value or "m" in str_value or "p" in str_value:
            return ST_UniversalMeasure.convert_from_xml(str_value)
        return Emu(int(str_value))

    @classmethod
    def validate(cls, value):
        ST_CoordinateUnqualified.validate(value)


class ST_CoordinateUnqualified(XsdLong):
    @classmethod
    def validate(cls, value):
        cls.validate_int_in_range(value, -27273042329600, 27273042316900)


class ST_DecimalNumber(XsdInt):
    pass


class ST_DrawingElementId(XsdUnsignedInt):
    pass


class ST_HexColor(BaseStringType):
    @classmethod
    def convert_from_xml(cls, str_value):
        if str_value == "auto":
            return ST_HexColorAuto.AUTO
        return RGBColor.from_string(str_value)

    @classmethod
    def convert_to_xml(cls, value):
        """
        Keep alpha hex numerals all uppercase just for consistency.
        """
        # expecting 3-tuple of ints in range 0-255
        return "%02X%02X%02X" % value

    @classmethod
    def validate(cls, value):
        # must be an RGBColor object ---
        if not isinstance(value, RGBColor):
            raise ValueError(
                "rgb color value must be RGBColor object, got %s %s"
                % (type(value), value)
            )


class ST_HexColorAuto(XsdStringEnumeration):
    """
    Value for `w:color/[@val="auto"] attribute setting
    """

    AUTO = "auto"

    _members = (AUTO,)


class ST_HpsMeasure(XsdUnsignedLong):
    """
    Half-point measure, e.g. 24.0 represents 12.0 points.
    """

    @classmethod
    def convert_from_xml(cls, str_value):
        if "m" in str_value or "n" in str_value or "p" in str_value:
            return ST_UniversalMeasure.convert_from_xml(str_value)
        return Pt(int(str_value) / 2.0)

    @classmethod
    def convert_to_xml(cls, value):
        emu = Emu(value)
        half_points = int(emu.pt * 2)
        return str(half_points)


class ST_Merge(XsdStringEnumeration):
    """
    Valid values for <w:xMerge val=""> attribute
    """

    CONTINUE = "continue"
    RESTART = "restart"

    _members = (CONTINUE, RESTART)


class ST_OnOff(XsdBoolean):
    @classmethod
    def convert_from_xml(cls, str_value):
        if str_value not in ("1", "0", "true", "false", "on", "off"):
            raise InvalidXmlError(
                "value must be one of '1', '0', 'true', 'false', 'on', or 'o"
                "ff', got '%s'" % str_value
            )
        return str_value in ("1", "true", "on")


class ST_PositiveCoordinate(XsdLong):
    @classmethod
    def convert_from_xml(cls, str_value):
        return Emu(int(str_value))

    @classmethod
    def validate(cls, value):
        cls.validate_int_in_range(value, 0, 27273042316900)


class ST_RelationshipId(XsdString):
    pass


class ST_SignedTwipsMeasure(XsdInt):
    @classmethod
    def convert_from_xml(cls, str_value):
        if "i" in str_value or "m" in str_value or "p" in str_value:
            return ST_UniversalMeasure.convert_from_xml(str_value)
        return Twips(int(str_value))

    @classmethod
    def convert_to_xml(cls, value):
        emu = Emu(value)
        twips = emu.twips
        return str(twips)


class ST_String(XsdString):
    pass


class ST_TblLayoutType(XsdString):
    @classmethod
    def validate(cls, value):
        cls.validate_string(value)
        valid_values = ("fixed", "autofit")
        if value not in valid_values:
            raise ValueError("must be one of %s, got '%s'" % (valid_values, value))


class ST_TblWidth(XsdString):
    @classmethod
    def validate(cls, value):
        cls.validate_string(value)
        valid_values = ("auto", "dxa", "nil", "pct")
        if value not in valid_values:
            raise ValueError("must be one of %s, got '%s'" % (valid_values, value))


class ST_TwipsMeasure(XsdUnsignedLong):
    @classmethod
    def convert_from_xml(cls, str_value):
        if "i" in str_value or "m" in str_value or "p" in str_value:
            return ST_UniversalMeasure.convert_from_xml(str_value)
        return Twips(int(str_value))

    @classmethod
    def convert_to_xml(cls, value):
        emu = Emu(value)
        twips = emu.twips
        return str(twips)


class ST_UniversalMeasure(BaseSimpleType):
    @classmethod
    def convert_from_xml(cls, str_value):
        float_part, units_part = str_value[:-2], str_value[-2:]
        quantity = float(float_part)
        multiplier = {
            "mm": 36000,
            "cm": 360000,
            "in": 914400,
            "pt": 12700,
            "pc": 152400,
            "pi": 152400,
        }[units_part]
        emu_value = Emu(int(round(quantity * multiplier)))
        return emu_value


class ST_VerticalAlignRun(XsdStringEnumeration):
    """
    Valid values for `w:vertAlign/@val`.
    """

    BASELINE = "baseline"
    SUPERSCRIPT = "superscript"
    SUBSCRIPT = "subscript"

    _members = (BASELINE, SUPERSCRIPT, SUBSCRIPT)
