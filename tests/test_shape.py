# encoding: utf-8

"""
Test suite for the docx.shape module
"""

from __future__ import absolute_import, print_function, unicode_literals

import pytest

from docx.enum.shape import WD_INLINE_SHAPE
from docx.oxml.ns import nsmap
from docx.shape import InlineShape, InlineShapes
from docx.shared import Length

from .oxml.unitdata.dml import (
    a_blip,
    a_blipFill,
    a_graphic,
    a_graphicData,
    a_pic,
    an_inline,
)
from .unitutil.cxml import element, xml
from .unitutil.mock import loose_mock


class DescribeInlineShapes(object):
    def it_knows_how_many_inline_shapes_it_contains(self, inline_shapes_fixture):
        inline_shapes, expected_count = inline_shapes_fixture
        assert len(inline_shapes) == expected_count

    def it_can_iterate_over_its_InlineShape_instances(self, inline_shapes_fixture):
        inline_shapes, inline_shape_count = inline_shapes_fixture
        actual_count = 0
        for inline_shape in inline_shapes:
            assert isinstance(inline_shape, InlineShape)
            actual_count += 1
        assert actual_count == inline_shape_count

    def it_provides_indexed_access_to_inline_shapes(self, inline_shapes_fixture):
        inline_shapes, inline_shape_count = inline_shapes_fixture
        for idx in range(-inline_shape_count, inline_shape_count):
            inline_shape = inline_shapes[idx]
            assert isinstance(inline_shape, InlineShape)

    def it_raises_on_indexed_access_out_of_range(self, inline_shapes_fixture):
        inline_shapes, inline_shape_count = inline_shapes_fixture
        with pytest.raises(IndexError):
            too_low = -1 - inline_shape_count
            inline_shapes[too_low]
        with pytest.raises(IndexError):
            too_high = inline_shape_count
            inline_shapes[too_high]

    def it_knows_the_part_it_belongs_to(self, inline_shapes_with_parent_):
        inline_shapes, parent_ = inline_shapes_with_parent_
        part = inline_shapes.part
        assert part is parent_.part

    # fixtures -------------------------------------------------------

    @pytest.fixture
    def inline_shapes_fixture(self):
        body = element("w:body/w:p/(w:r/w:drawing/wp:inline, w:r/w:drawing/wp:inline)")
        inline_shapes = InlineShapes(body, None)
        expected_count = 2
        return inline_shapes, expected_count

    # fixture components ---------------------------------------------

    @pytest.fixture
    def inline_shapes_with_parent_(self, request):
        parent_ = loose_mock(request, name="parent_")
        inline_shapes = InlineShapes(None, parent_)
        return inline_shapes, parent_


class DescribeInlineShape(object):
    def it_knows_what_type_of_shape_it_is(self, shape_type_fixture):
        inline_shape, inline_shape_type = shape_type_fixture
        assert inline_shape.type == inline_shape_type

    def it_knows_its_display_dimensions(self, dimensions_get_fixture):
        inline_shape, cx, cy = dimensions_get_fixture
        width = inline_shape.width
        height = inline_shape.height
        assert isinstance(width, Length)
        assert width == cx
        assert isinstance(height, Length)
        assert height == cy

    def it_can_change_its_display_dimensions(self, dimensions_set_fixture):
        inline_shape, cx, cy, expected_xml = dimensions_set_fixture
        inline_shape.width = cx
        inline_shape.height = cy
        assert inline_shape._inline.xml == expected_xml

    # fixtures -------------------------------------------------------

    @pytest.fixture
    def dimensions_get_fixture(self):
        inline_cxml, expected_cx, expected_cy = (
            "wp:inline/wp:extent{cx=333, cy=666}",
            333,
            666,
        )
        inline_shape = InlineShape(element(inline_cxml))
        return inline_shape, expected_cx, expected_cy

    @pytest.fixture
    def dimensions_set_fixture(self):
        inline_cxml, new_cx, new_cy, expected_cxml = (
            "wp:inline/(wp:extent{cx=333,cy=666},a:graphic/a:graphicData/"
            "pic:pic/pic:spPr/a:xfrm/a:ext{cx=333,cy=666})",
            444,
            888,
            "wp:inline/(wp:extent{cx=444,cy=888},a:graphic/a:graphicData/"
            "pic:pic/pic:spPr/a:xfrm/a:ext{cx=444,cy=888})",
        )
        inline_shape = InlineShape(element(inline_cxml))
        expected_xml = xml(expected_cxml)
        return inline_shape, new_cx, new_cy, expected_xml

    @pytest.fixture(
        params=[
            "embed pic",
            "link pic",
            "link+embed pic",
            "chart",
            "smart art",
            "not implemented",
        ]
    )
    def shape_type_fixture(self, request):
        if request.param == "embed pic":
            inline = self._inline_with_picture(embed=True)
            shape_type = WD_INLINE_SHAPE.PICTURE

        elif request.param == "link pic":
            inline = self._inline_with_picture(link=True)
            shape_type = WD_INLINE_SHAPE.LINKED_PICTURE

        elif request.param == "link+embed pic":
            inline = self._inline_with_picture(embed=True, link=True)
            shape_type = WD_INLINE_SHAPE.LINKED_PICTURE

        elif request.param == "chart":
            inline = self._inline_with_uri(nsmap["c"])
            shape_type = WD_INLINE_SHAPE.CHART

        elif request.param == "smart art":
            inline = self._inline_with_uri(nsmap["dgm"])
            shape_type = WD_INLINE_SHAPE.SMART_ART

        elif request.param == "not implemented":
            inline = self._inline_with_uri("foobar")
            shape_type = WD_INLINE_SHAPE.NOT_IMPLEMENTED

        return InlineShape(inline), shape_type

    # fixture components ---------------------------------------------

    def _inline_with_picture(self, embed=False, link=False):
        picture_ns = nsmap["pic"]

        blip_bldr = a_blip()
        if embed:
            blip_bldr.with_embed("rId1")
        if link:
            blip_bldr.with_link("rId2")

        inline = (
            an_inline()
            .with_nsdecls("wp", "r")
            .with_child(
                a_graphic()
                .with_nsdecls()
                .with_child(
                    a_graphicData()
                    .with_uri(picture_ns)
                    .with_child(
                        a_pic()
                        .with_nsdecls()
                        .with_child(a_blipFill().with_child(blip_bldr))
                    )
                )
            )
        ).element
        return inline

    def _inline_with_uri(self, uri):
        inline = (
            an_inline()
            .with_nsdecls("wp")
            .with_child(
                a_graphic().with_nsdecls().with_child(a_graphicData().with_uri(uri))
            )
        ).element
        return inline
