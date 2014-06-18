# encoding: utf-8

"""
Objects shared by docx modules.
"""

from __future__ import absolute_import, print_function, unicode_literals


class Length(int):
    """
    Base class for length constructor classes Inches, Cm, Mm, Px, and Emu.
    Behaves as an int count of English Metric Units, 914400 to the inch,
    36000 to the cm. Provides convenience unit conversion methods in the form
    of read-only properties. Immutable.
    """
    _EMUS_PER_INCH = 914400
    _EMUS_PER_CM = 360000
    _EMUS_PER_MM = 36000
    _EMUS_PER_PX = 12700
    _EMUS_PER_TWIP = 635

    def __new__(cls, emu):
        return int.__new__(cls, emu)

    @property
    def cm(self):
        """
        The equivalent length expressed in centimeters (float).
        """
        return self / float(self._EMUS_PER_CM)

    @property
    def emu(self):
        """
        The equivalent length expressed in English Metric Units (int).
        """
        return self

    @property
    def inches(self):
        """
        The equivalent length expressed in inches (float).
        """
        return self / float(self._EMUS_PER_INCH)

    @property
    def mm(self):
        """
        The equivalent length expressed in millimeters (float).
        """
        return self / float(self._EMUS_PER_MM)

    @property
    def px(self):
        # round can somtimes return values like x.999999 which are truncated
        # to x by int(); adding the 0.1 prevents this
        return int(round(self / float(self._EMUS_PER_PX)) + 0.1)

    @property
    def twips(self):
        """
        The equivalent length expressed in twips (int).
        """
        return int(round(self / float(self._EMUS_PER_TWIP)))


class Inches(Length):
    """
    Convenience constructor for length in inches, e.g.
    ``width = Inches(0.5)``.
    """
    def __new__(cls, inches):
        emu = int(inches * Length._EMUS_PER_INCH)
        return Length.__new__(cls, emu)


class Cm(Length):
    """
    Convenience constructor for length in centimeters, e.g.
    ``height = Cm(12)``.
    """
    def __new__(cls, cm):
        emu = int(cm * Length._EMUS_PER_CM)
        return Length.__new__(cls, emu)


class Emu(Length):
    """
    Convenience constructor for length in English Metric Units, e.g.
    ``width = Emu(457200)``.
    """
    def __new__(cls, emu):
        return Length.__new__(cls, int(emu))


class Mm(Length):
    """
    Convenience constructor for length in millimeters, e.g.
    ``width = Mm(240.5)``.
    """
    def __new__(cls, mm):
        emu = int(mm * Length._EMUS_PER_MM)
        return Length.__new__(cls, emu)


class Pt(int):
    """
    Convenience class for setting font sizes in points
    """
    _UNITS_PER_POINT = 100

    def __new__(cls, pts):
        units = int(pts * Pt._UNITS_PER_POINT)
        return int.__new__(cls, units)


class Px(Length):
    """
    Convenience constructor for length in pixels.
    """
    def __new__(cls, px):
        emu = int(px * Length._EMUS_PER_PX)
        return Length.__new__(cls, emu)


class Twips(Length):
    """
    Convenience constructor for length in twips, e.g. ``width = Twips(42)``.
    A twip is a twentieth of a point, 635 EMU.
    """
    def __new__(cls, twips):
        emu = int(twips * Length._EMUS_PER_TWIP)
        return Length.__new__(cls, emu)


def lazyproperty(f):
    """
    @lazyprop decorator. Decorated method will be called only on first access
    to calculate a cached property value. After that, the cached value is
    returned.
    """
    cache_attr_name = '_%s' % f.__name__  # like '_foobar' for prop 'foobar'
    docstring = f.__doc__

    def get_prop_value(obj):
        try:
            return getattr(obj, cache_attr_name)
        except AttributeError:
            value = f(obj)
            setattr(obj, cache_attr_name, value)
            return value

    return property(get_prop_value, doc=docstring)


def write_only_property(f):
    """
    @write_only_property decorator. Creates a property (descriptor attribute)
    that accepts assignment, but not getattr (use in an expression).
    """
    docstring = f.__doc__

    return property(fset=f, doc=docstring)


class Parented(object):
    """
    Provides common services for document elements that occur below a part
    but may occasionally require an ancestor object to provide a service,
    such as add or drop a relationship. Provides ``self._parent`` attribute
    to subclasses.
    """
    def __init__(self, parent):
        super(Parented, self).__init__()
        self._parent = parent

    @property
    def part(self):
        """
        The package part containing this object
        """
        return self._parent.part
