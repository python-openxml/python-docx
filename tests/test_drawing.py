# pyright: reportPrivateUsage=false

"""Unit test suite for the `docx.drawing` module."""

from __future__ import annotations

from typing import cast

import pytest

from docx.drawing import Drawing
from docx.image.image import Image
from docx.oxml.drawing import CT_Drawing
from docx.parts.document import DocumentPart
from docx.parts.image import ImagePart

from .unitutil.cxml import element
from .unitutil.mock import FixtureRequest, Mock, instance_mock


class DescribeDrawing:
    """Unit-test suite for `docx.drawing.Drawing` objects."""

    @pytest.mark.parametrize(
        ("cxml", "expected_value"),
        [
            ("w:drawing/wp:inline/a:graphic/a:graphicData/pic:pic", True),
            ("w:drawing/wp:anchor/a:graphic/a:graphicData/pic:pic", True),
            ("w:drawing/wp:inline/a:graphic/a:graphicData/a:grpSp", False),
            ("w:drawing/wp:anchor/a:graphic/a:graphicData/a:chart", False),
        ],
    )
    def it_knows_when_it_contains_a_Picture(
        self, cxml: str, expected_value: bool, document_part_: Mock
    ):
        drawing = Drawing(cast(CT_Drawing, element(cxml)), document_part_)
        assert drawing.has_picture == expected_value

    def it_provides_access_to_the_image_in_a_Picture_drawing(
        self, document_part_: Mock, image_part_: Mock, image_: Mock
    ):
        image_part_.image = image_
        document_part_.part.related_parts = {"rId1": image_part_}
        cxml = (
            "w:drawing/wp:inline/a:graphic/a:graphicData/pic:pic/pic:blipFill/a:blip{r:embed=rId1}"
        )
        drawing = Drawing(cast(CT_Drawing, element(cxml)), document_part_)

        image = drawing.image

        assert image is image_

    def but_it_raises_when_the_drawing_does_not_contain_a_Picture(self, document_part_: Mock):
        drawing = Drawing(
            cast(CT_Drawing, element("w:drawing/wp:inline/a:graphic/a:graphicData/a:grpSp")),
            document_part_,
        )

        with pytest.raises(ValueError, match="drawing does not contain a picture"):
            drawing.image

    # -- fixtures --------------------------------------------------------------------------------

    @pytest.fixture
    def document_part_(self, request: FixtureRequest):
        return instance_mock(request, DocumentPart)

    @pytest.fixture
    def image_(self, request: FixtureRequest):
        return instance_mock(request, Image)

    @pytest.fixture
    def image_part_(self, request: FixtureRequest):
        return instance_mock(request, ImagePart)
