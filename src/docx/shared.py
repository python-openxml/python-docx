"""Objects shared by docx modules."""

from __future__ import annotations

import functools
from typing import TYPE_CHECKING, Any, Callable, Generic, Iterator, List, TypeVar, cast

if TYPE_CHECKING:
    from docx.oxml.xmlchemy import BaseOxmlElement
    from docx.parts.story import StoryPart


class Length(int):
    """Base class for length constructor classes Inches, Cm, Mm, Px, and Emu.

    Behaves as an int count of English Metric Units, 914,400 to the inch, 36,000 to the
    mm. Provides convenience unit conversion methods in the form of read-only
    properties. Immutable.
    """

    _EMUS_PER_INCH = 914400
    _EMUS_PER_CM = 360000
    _EMUS_PER_MM = 36000
    _EMUS_PER_PT = 12700
    _EMUS_PER_TWIP = 635

    def __new__(cls, emu):
        return int.__new__(cls, emu)

    @property
    def cm(self):
        """The equivalent length expressed in centimeters (float)."""
        return self / float(self._EMUS_PER_CM)

    @property
    def emu(self):
        """The equivalent length expressed in English Metric Units (int)."""
        return self

    @property
    def inches(self):
        """The equivalent length expressed in inches (float)."""
        return self / float(self._EMUS_PER_INCH)

    @property
    def mm(self):
        """The equivalent length expressed in millimeters (float)."""
        return self / float(self._EMUS_PER_MM)

    @property
    def pt(self):
        """Floating point length in points."""
        return self / float(self._EMUS_PER_PT)

    @property
    def twips(self):
        """The equivalent length expressed in twips (int)."""
        return int(round(self / float(self._EMUS_PER_TWIP)))


class Inches(Length):
    """Convenience constructor for length in inches, e.g. ``width = Inches(0.5)``."""

    def __new__(cls, inches):
        emu = int(inches * Length._EMUS_PER_INCH)
        return Length.__new__(cls, emu)


class Cm(Length):
    """Convenience constructor for length in centimeters, e.g. ``height = Cm(12)``."""

    def __new__(cls, cm):
        emu = int(cm * Length._EMUS_PER_CM)
        return Length.__new__(cls, emu)


class Emu(Length):
    """Convenience constructor for length in English Metric Units, e.g. ``width =
    Emu(457200)``."""

    def __new__(cls, emu):
        return Length.__new__(cls, int(emu))


class Mm(Length):
    """Convenience constructor for length in millimeters, e.g. ``width = Mm(240.5)``."""

    def __new__(cls, mm):
        emu = int(mm * Length._EMUS_PER_MM)
        return Length.__new__(cls, emu)


class Pt(Length):
    """Convenience value class for specifying a length in points."""

    def __new__(cls, points):
        emu = int(points * Length._EMUS_PER_PT)
        return Length.__new__(cls, emu)


class Twips(Length):
    """Convenience constructor for length in twips, e.g. ``width = Twips(42)``.

    A twip is a twentieth of a point, 635 EMU.
    """

    def __new__(cls, twips):
        emu = int(twips * Length._EMUS_PER_TWIP)
        return Length.__new__(cls, emu)


class RGBColor(tuple):
    """Immutable value object defining a particular RGB color."""

    def __new__(cls, r, g, b):
        msg = "RGBColor() takes three integer values 0-255"
        for val in (r, g, b):
            if not isinstance(val, int) or val < 0 or val > 255:
                raise ValueError(msg)
        return super(RGBColor, cls).__new__(cls, (r, g, b))

    def __repr__(self):
        return "RGBColor(0x%02x, 0x%02x, 0x%02x)" % self

    def __str__(self):
        """Return a hex string rgb value, like '3C2F80'."""
        return "%02X%02X%02X" % self

    @classmethod
    def from_string(cls, rgb_hex_str):
        """Return a new instance from an RGB color hex string like ``'3C2F80'``."""
        r = int(rgb_hex_str[:2], 16)
        g = int(rgb_hex_str[2:4], 16)
        b = int(rgb_hex_str[4:], 16)
        return cls(r, g, b)


T = TypeVar("T")


class lazyproperty(Generic[T]):
    """Decorator like @property, but evaluated only on first access.

    Like @property, this can only be used to decorate methods having only a `self`
    parameter, and is accessed like an attribute on an instance, i.e. trailing
    parentheses are not used. Unlike @property, the decorated method is only evaluated
    on first access; the resulting value is cached and that same value returned on
    second and later access without re-evaluation of the method.

    Like @property, this class produces a *data descriptor* object, which is stored in
    the __dict__ of the *class* under the name of the decorated method ('fget'
    nominally). The cached value is stored in the __dict__ of the *instance* under that
    same name.

    Because it is a data descriptor (as opposed to a *non-data descriptor*), its
    `__get__()` method is executed on each access of the decorated attribute; the
    __dict__ item of the same name is "shadowed" by the descriptor.

    While this may represent a performance improvement over a property, its greater
    benefit may be its other characteristics. One common use is to construct
    collaborator objects, removing that "real work" from the constructor, while still
    only executing once. It also de-couples client code from any sequencing
    considerations; if it's accessed from more than one location, it's assured it will
    be ready whenever needed.

    Loosely based on: https://stackoverflow.com/a/6849299/1902513.

    A lazyproperty is read-only. There is no counterpart to the optional "setter" (or
    deleter) behavior of an @property. This is critically important to maintaining its
    immutability and idempotence guarantees. Attempting to assign to a lazyproperty
    raises AttributeError unconditionally.

    The parameter names in the methods below correspond to this usage example::

        class Obj(object)

            @lazyproperty
            def fget(self):
                return 'some result'

        obj = Obj()

    Not suitable for wrapping a function (as opposed to a method) because it is not
    callable."""

    def __init__(self, fget: Callable[..., T]) -> None:
        """*fget* is the decorated method (a "getter" function).

        A lazyproperty is read-only, so there is only an *fget* function (a regular
        @property can also have an fset and fdel function). This name was chosen for
        consistency with Python's `property` class which uses this name for the
        corresponding parameter.
        """
        # --- maintain a reference to the wrapped getter method
        self._fget = fget
        # --- and store the name of that decorated method
        self._name = fget.__name__
        # --- adopt fget's __name__, __doc__, and other attributes
        functools.update_wrapper(self, fget)  # pyright: ignore

    def __get__(self, obj: Any, type: Any = None) -> T:
        """Called on each access of 'fget' attribute on class or instance.

        *self* is this instance of a lazyproperty descriptor "wrapping" the property
        method it decorates (`fget`, nominally).

        *obj* is the "host" object instance when the attribute is accessed from an
        object instance, e.g. `obj = Obj(); obj.fget`. *obj* is None when accessed on
        the class, e.g. `Obj.fget`.

        *type* is the class hosting the decorated getter method (`fget`) on both class
        and instance attribute access.
        """
        # --- when accessed on class, e.g. Obj.fget, just return this descriptor
        # --- instance (patched above to look like fget).
        if obj is None:
            return self  # type: ignore

        # --- when accessed on instance, start by checking instance __dict__ for
        # --- item with key matching the wrapped function's name
        value = obj.__dict__.get(self._name)
        if value is None:
            # --- on first access, the __dict__ item will be absent. Evaluate fget()
            # --- and store that value in the (otherwise unused) host-object
            # --- __dict__ value of same name ('fget' nominally)
            value = self._fget(obj)
            obj.__dict__[self._name] = value
        return cast(T, value)

    def __set__(self, obj: Any, value: Any) -> None:
        """Raises unconditionally, to preserve read-only behavior.

        This decorator is intended to implement immutable (and idempotent) object
        attributes. For that reason, assignment to this property must be explicitly
        prevented.

        If this __set__ method was not present, this descriptor would become a
        *non-data descriptor*. That would be nice because the cached value would be
        accessed directly once set (__dict__ attrs have precedence over non-data
        descriptors on instance attribute lookup). The problem is, there would be
        nothing to stop assignment to the cached value, which would overwrite the result
        of `fget()` and break both the immutability and idempotence guarantees of this
        decorator.

        The performance with this __set__() method in place was roughly 0.4 usec per
        access when measured on a 2.8GHz development machine; so quite snappy and
        probably not a rich target for optimization efforts.
        """
        raise AttributeError("can't set attribute")


def write_only_property(f):
    """@write_only_property decorator.

    Creates a property (descriptor attribute) that accepts assignment, but not getattr
    (use in an expression).
    """
    docstring = f.__doc__

    return property(fset=f, doc=docstring)


class ElementProxy:
    """Base class for lxml element proxy classes.

    An element proxy class is one whose primary responsibilities are fulfilled by
    manipulating the attributes and child elements of an XML element. They are the most
    common type of class in python-docx other than custom element (oxml) classes.
    """

    def __init__(self, element: BaseOxmlElement, parent: Any | None = None):
        self._element = element
        self._parent = parent

    def __eq__(self, other):
        """Return |True| if this proxy object refers to the same oxml element as does
        `other`.

        ElementProxy objects are value objects and should maintain no mutable local
        state. Equality for proxy objects is defined as referring to the same XML
        element, whether or not they are the same proxy object instance.
        """
        if not isinstance(other, ElementProxy):
            return False
        return self._element is other._element

    def __ne__(self, other):
        if not isinstance(other, ElementProxy):
            return True
        return self._element is not other._element

    @property
    def element(self):
        """The lxml element proxied by this object."""
        return self._element

    @property
    def part(self):
        """The package part containing this object."""
        return self._parent.part


class Parented:
    """Provides common services for document elements that occur below a part but may
    occasionally require an ancestor object to provide a service, such as add or drop a
    relationship.

    Provides ``self._parent`` attribute to subclasses.
    """

    def __init__(self, parent):
        self._parent = parent

    @property
    def part(self):
        """The package part containing this object."""
        return self._parent.part


class StoryChild:
    """A document element within a story part.

    Story parts include DocumentPart and Header/FooterPart and can contain block items
    (paragraphs and tables). Items from the block-item subtree occasionally require an
    ancestor object to provide access to part-level or package-level items like styles
    or images or to add or drop a relationship.

    Provides `self._parent` attribute to subclasses.
    """

    def __init__(self, parent: StoryChild):
        self._parent = parent

    @property
    def part(self) -> StoryPart:
        """The package part containing this object."""
        return self._parent.part


class TextAccumulator:
    """Accepts `str` fragments and joins them together, in order, on `.pop().

    Handy when text in a stream is broken up arbitrarily and you want to join it back
    together within certain bounds. The optional `separator` argument determines how
    the text fragments are punctuated, defaulting to the empty string.
    """

    def __init__(self, separator: str = ""):
        self._separator = separator
        self._texts: List[str] = []

    def push(self, text: str) -> None:
        """Add a text fragment to the accumulator."""
        self._texts.append(text)

    def pop(self) -> Iterator[str]:
        """Generate sero-or-one str from those accumulated.

        Using `yield from accum.pop()` in a generator setting avoids producing an empty
        string when no text is in the accumulator.
        """
        if not self._texts:
            return
        text = self._separator.join(self._texts)
        self._texts.clear()
        yield text
