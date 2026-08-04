"""Enumerations related to DrawingML shapes in WordprocessingML files."""

from __future__ import annotations

import enum


class WD_INLINE_SHAPE_TYPE(enum.Enum):
    """Corresponds to WdInlineShapeType enumeration.

    http://msdn.microsoft.com/en-us/library/office/ff192587.aspx.
    """

    CHART = 12
    LINKED_PICTURE = 4
    PICTURE = 3
    SMART_ART = 15
    NOT_IMPLEMENTED = -6


WD_INLINE_SHAPE = WD_INLINE_SHAPE_TYPE


class EXIF_ORIENTATION(enum.Enum):
    """Exif/TIFF Orientation mapped to DrawingML ``a:xfrm`` attributes.
    https://exifstrip.com/guides/orientation-tag-explained
    
    Each member exposes:
    * ``.rot`` — DrawingML ``ST_Angle`` (1/60000°, clockwise)
    * ``.flip_h`` — ``a:xfrm/@flipH``
    * ``.flip_v`` — ``a:xfrm/@flipV``

    ``AUTO`` resolves to the orientation embedded in the image (or ``NORMAL``
    when absent). The enum value for concrete members is the Orientation tag
    integer (1-8).
    """

    rot: int
    flip_h: bool
    flip_v: bool

    def __new__(cls, exif_value: int, rot: int, flip_h: bool, flip_v: bool):
        self = object.__new__(cls)
        self._value_ = exif_value
        self.rot = rot
        self.flip_h = flip_h
        self.flip_v = flip_v
        return self

    def __str__(self) -> str:
        return f"{self.name} ({self.value})"

    @property
    def swaps_axes(self) -> bool:
        """True when this orientation rotates the image by 90° or 270°."""
        return self in (
            EXIF_ORIENTATION.TRANSPOSE,
            EXIF_ORIENTATION.ROTATE_90,
            EXIF_ORIENTATION.TRANSVERSE,
            EXIF_ORIENTATION.ROTATE_270,
        )

    @classmethod
    def from_exif_value(cls, value: int | None) -> EXIF_ORIENTATION:
        """Return the member for Exif Orientation `value`, or |NORMAL| if unknown."""
        if value is None:
            return cls.NORMAL
        try:
            member = cls(value)
        except ValueError:
            return cls.NORMAL
        if member is cls.AUTO:
            return cls.NORMAL
        return member

    AUTO = (0, 0, False, False)
    NORMAL = (1, 0, False, False)
    FLIP_HORIZONTAL = (2, 0, True, False)
    ROTATE_180 = (3, 10_800_000, False, False)
    FLIP_VERTICAL = (4, 0, False, True)
    TRANSPOSE = (5, 16_200_000, True, False)
    ROTATE_90 = (6, 5_400_000, False, False)
    TRANSVERSE = (7, 5_400_000, True, False)
    ROTATE_270 = (8, 16_200_000, False, False)
