# encoding: utf-8

"""
Objects shared by docx modules.
"""

from __future__ import absolute_import, print_function, unicode_literals


class _BaseLength(int):
    """
    Base class for length classes Inches, Cm, Mm, Px, and Emu
    """
    _EMUS_PER_INCH = 914400
    _EMUS_PER_CM = 360000
    _EMUS_PER_MM = 36000
    _EMUS_PER_PX = 12700

    def __new__(cls, emu):
        return int.__new__(cls, emu)

    @property
    def inches(self):
        return self / float(self._EMUS_PER_INCH)

    @property
    def cm(self):
        return self / float(self._EMUS_PER_CM)

    @property
    def mm(self):
        return self / float(self._EMUS_PER_MM)

    @property
    def px(self):
        # round can somtimes return values like x.999999 which are truncated
        # to x by int(); adding the 0.1 prevents this
        return int(round(self / float(self._EMUS_PER_PX)) + 0.1)

    @property
    def emu(self):
        return self


class Inches(_BaseLength):
    """Convenience constructor for length in inches."""
    def __new__(cls, inches):
        emu = int(inches * _BaseLength._EMUS_PER_INCH)
        return _BaseLength.__new__(cls, emu)


class Cm(_BaseLength):
    """Convenience constructor for length in centimeters."""
    def __new__(cls, cm):
        emu = int(cm * _BaseLength._EMUS_PER_CM)
        return _BaseLength.__new__(cls, emu)


class Emu(_BaseLength):
    """Convenience constructor for length in english metric units."""
    def __new__(cls, emu):
        return _BaseLength.__new__(cls, int(emu))


class Mm(_BaseLength):
    """Convenience constructor for length in millimeters."""
    def __new__(cls, mm):
        emu = int(mm * _BaseLength._EMUS_PER_MM)
        return _BaseLength.__new__(cls, emu)


class Pt(int):
    """Convenience class for setting font sizes in points"""
    _UNITS_PER_POINT = 100

    def __new__(cls, pts):
        units = int(pts * Pt._UNITS_PER_POINT)
        return int.__new__(cls, units)


class Px(_BaseLength):
    """Convenience constructor for length in pixels."""
    def __new__(cls, px):
        emu = int(px * _BaseLength._EMUS_PER_PX)
        return _BaseLength.__new__(cls, emu)


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
