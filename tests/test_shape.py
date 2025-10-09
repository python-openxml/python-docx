# pyright: reportPrivateUsage=false

"""Test suite for the docx.shape module."""

from __future__ import annotations

from typing import cast

import pytest

from docx.document import Document
from docx.enum.shape import WD_INLINE_SHAPE
from docx.oxml.document import CT_Body
from docx.oxml.ns import nsmap
from docx.oxml.shape import CT_Inline
from docx.shape import InlineShape, InlineShapes
from docx.shared import Emu, Length

from .unitutil.cxml import element, xml
from .unitutil.mock import FixtureRequest, Mock, instance_mock


class DescribeInlineShapes:
    """Unit-test suite for `docx.shape.InlineShapes` objects."""

    def it_knows_how_many_inline_shapes_it_contains(self, body: CT_Body, document_: Mock):
        inline_shapes = InlineShapes(body, document_)
        assert len(inline_shapes) == 2

    def it_can_iterate_over_its_InlineShape_instances(self, body: CT_Body, document_: Mock):
        inline_shapes = InlineShapes(body, document_)
        assert all(isinstance(s, InlineShape) for s in inline_shapes)
        assert len(list(inline_shapes)) == 2

    def it_provides_indexed_access_to_inline_shapes(self, body: CT_Body, document_: Mock):
        inline_shapes = InlineShapes(body, document_)
        for idx in range(-2, 2):
            assert isinstance(inline_shapes[idx], InlineShape)

    def it_raises_on_indexed_access_out_of_range(self, body: CT_Body, document_: Mock):
        inline_shapes = InlineShapes(body, document_)

        with pytest.raises(IndexError, match=r"inline shape index \[-3\] out of range"):
            inline_shapes[-3]
        with pytest.raises(IndexError, match=r"inline shape index \[2\] out of range"):
            inline_shapes[2]

    def it_knows_the_part_it_belongs_to(self, body: CT_Body, document_: Mock):
        inline_shapes = InlineShapes(body, document_)
        assert inline_shapes.part is document_.part

    # -- fixtures --------------------------------------------------------------------------------

    @pytest.fixture
    def body(self) -> CT_Body:
        return cast(
            CT_Body, element("w:body/w:p/(w:r/w:drawing/wp:inline, w:r/w:drawing/wp:inline)")
        )

    @pytest.fixture
    def document_(self, request: FixtureRequest):
        return instance_mock(request, Document)


class DescribeInlineShape:
    """Unit-test suite for `docx.shape.InlineShape` objects."""

    @pytest.mark.parametrize(
        ("uri", "content_cxml", "expected_value"),
        [
            # -- embedded picture --
            (nsmap["pic"], "/pic:pic/pic:blipFill/a:blip{r:embed=rId1}", WD_INLINE_SHAPE.PICTURE),
            # -- linked picture --
            (
                nsmap["pic"],
                "/pic:pic/pic:blipFill/a:blip{r:link=rId2}",
                WD_INLINE_SHAPE.LINKED_PICTURE,
            ),
            # -- linked and embedded picture (not expected) --
            (
                nsmap["pic"],
                "/pic:pic/pic:blipFill/a:blip{r:embed=rId1,r:link=rId2}",
                WD_INLINE_SHAPE.LINKED_PICTURE,
            ),
            # -- chart --
            (nsmap["c"], "", WD_INLINE_SHAPE.CHART),
            # -- SmartArt --
            (nsmap["dgm"], "", WD_INLINE_SHAPE.SMART_ART),
            # -- something else we don't know about --
            ("foobar", "", WD_INLINE_SHAPE.NOT_IMPLEMENTED),
        ],
    )
    def it_knows_what_type_of_shape_it_is(
        self, uri: str, content_cxml: str, expected_value: WD_INLINE_SHAPE
    ):
        cxml = "wp:inline/a:graphic/a:graphicData{uri=%s}%s" % (uri, content_cxml)
        inline = cast(CT_Inline, element(cxml))
        inline_shape = InlineShape(inline)
        assert inline_shape.type == expected_value

    def it_knows_its_display_dimensions(self):
        inline = cast(CT_Inline, element("wp:inline/wp:extent{cx=333, cy=666}"))
        inline_shape = InlineShape(inline)

        width, height = inline_shape.width, inline_shape.height

        assert isinstance(width, Length)
        assert width == 333
        assert isinstance(height, Length)
        assert height == 666

    def it_can_change_its_display_dimensions(self):
        inline_shape = InlineShape(
            cast(
                CT_Inline,
                element(
                    "wp:inline/(wp:extent{cx=333,cy=666},a:graphic/a:graphicData/pic:pic/"
                    "pic:spPr/a:xfrm/a:ext{cx=333,cy=666})"
                ),
            )
        )

        inline_shape.width = Emu(444)
        inline_shape.height = Emu(888)

        assert inline_shape._inline.xml == xml(
            "wp:inline/(wp:extent{cx=444,cy=888},a:graphic/a:graphicData/pic:pic/pic:spPr/"
            "a:xfrm/a:ext{cx=444,cy=888})"
        )
