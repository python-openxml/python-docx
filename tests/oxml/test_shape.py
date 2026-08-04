# pyright: reportPrivateUsage=false

"""Test suite for the docx.oxml.shape module."""

from __future__ import annotations

import pytest

from docx.enum.shape import EXIF_ORIENTATION
from docx.oxml.shape import CT_Inline, CT_Picture
from docx.shared import Emu


class DescribeCT_Picture:
    """Unit-test suite for `docx.oxml.shape.CT_Picture` objects."""

    @pytest.mark.parametrize(
        ("orientation", "expected_rot", "expected_flip_h", "expected_flip_v"),
        [
            (EXIF_ORIENTATION.NORMAL, None, None, None),
            (EXIF_ORIENTATION.FLIP_HORIZONTAL, None, "1", None),
            (EXIF_ORIENTATION.ROTATE_180, "10800000", None, None),
            (EXIF_ORIENTATION.FLIP_VERTICAL, None, None, "1"),
            (EXIF_ORIENTATION.TRANSPOSE, "16200000", "1", None),
            (EXIF_ORIENTATION.ROTATE_90, "5400000", None, None),
            (EXIF_ORIENTATION.TRANSVERSE, "5400000", "1", None),
            (EXIF_ORIENTATION.ROTATE_270, "16200000", None, None),
        ],
    )
    def it_can_set_exif_orientation_on_xfrm(
        self,
        orientation: EXIF_ORIENTATION,
        expected_rot: str | None,
        expected_flip_h: str | None,
        expected_flip_v: str | None,
    ):
        pic = CT_Picture.new(
            1, "image.jpg", "rId1", Emu(914400), Emu(914400), orientation=orientation
        )

        xfrm = pic.spPr.xfrm
        assert xfrm is not None
        assert xfrm.get("rot") == expected_rot
        assert xfrm.get("flipH") == expected_flip_h
        assert xfrm.get("flipV") == expected_flip_v
        assert xfrm.rot == orientation.rot
        assert xfrm.flipH is orientation.flip_h
        assert xfrm.flipV is orientation.flip_v


class DescribeCT_Inline:
    """Unit-test suite for `docx.oxml.shape.CT_Inline` picture factory."""

    def it_swaps_extent_axes_for_rotated_orientations(self):
        inline = CT_Inline.new_pic_inline(
            1, "rId1", "image.jpg", Emu(200), Emu(100), EXIF_ORIENTATION.ROTATE_90
        )

        assert inline.extent.cx == Emu(100)
        assert inline.extent.cy == Emu(200)
        pic = inline.graphic.graphicData.pic
        assert pic is not None
        assert pic.spPr.cx == Emu(200)
        assert pic.spPr.cy == Emu(100)
        assert pic.spPr.xfrm.rot == EXIF_ORIENTATION.ROTATE_90.rot


class DescribeEXIF_ORIENTATION:
    def it_knows_which_members_swap_axes(self):
        assert EXIF_ORIENTATION.NORMAL.swaps_axes is False
        assert EXIF_ORIENTATION.ROTATE_180.swaps_axes is False
        assert EXIF_ORIENTATION.ROTATE_90.swaps_axes is True
        assert EXIF_ORIENTATION.ROTATE_270.swaps_axes is True

    @pytest.mark.parametrize(
        ("value", "expected"),
        [
            (None, EXIF_ORIENTATION.NORMAL),
            (1, EXIF_ORIENTATION.NORMAL),
            (6, EXIF_ORIENTATION.ROTATE_90),
            (0, EXIF_ORIENTATION.NORMAL),
            (99, EXIF_ORIENTATION.NORMAL),
        ],
    )
    def it_can_resolve_exif_values(self, value: int | None, expected: EXIF_ORIENTATION):
        assert EXIF_ORIENTATION.from_exif_value(value) is expected
