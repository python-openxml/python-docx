# pyright: reportPrivateUsage=false

"""Unit test suite for docx.package module."""

from __future__ import annotations

import pytest

from docx.image.image import Image
from docx.opc.packuri import PackURI
from docx.package import ImageParts, Package
from docx.parts.image import ImagePart

from .unitutil.file import docx_path
from .unitutil.mock import (
    FixtureRequest,
    Mock,
    class_mock,
    instance_mock,
    method_mock,
    property_mock,
)


class DescribePackage:
    """Unit-test suite for `docx.package.Package`."""

    def it_can_get_or_add_an_image_part_containing_a_specified_image(
        self, image_parts_prop_: Mock, image_parts_: Mock, image_part_: Mock
    ):
        image_parts_prop_.return_value = image_parts_
        image_parts_.get_or_add_image_part.return_value = image_part_
        package = Package()

        image_part = package.get_or_add_image_part("image.png")

        image_parts_.get_or_add_image_part.assert_called_once_with("image.png")
        assert image_part is image_part_

    def it_gathers_package_image_parts_after_unmarshalling(self):
        package = Package.open(docx_path("having-images"))

        image_parts = package.image_parts

        assert len(image_parts) == 3
        assert all(isinstance(p, ImagePart) for p in image_parts)

    # fixture components ---------------------------------------------

    @pytest.fixture
    def image_part_(self, request: FixtureRequest):
        return instance_mock(request, ImagePart)

    @pytest.fixture
    def image_parts_(self, request: FixtureRequest):
        return instance_mock(request, ImageParts)

    @pytest.fixture
    def image_parts_prop_(self, request: FixtureRequest):
        return property_mock(request, Package, "image_parts")


class DescribeImageParts:
    """Unit-test suite for `docx.package.Package`."""

    def it_can_get_a_matching_image_part(
        self,
        Image_: Mock,
        image_: Mock,
        _get_by_sha1_: Mock,
        image_part_: Mock,
    ):
        Image_.from_file.return_value = image_
        image_.sha1 = "f005ba11"
        _get_by_sha1_.return_value = image_part_
        image_parts = ImageParts()

        image_part = image_parts.get_or_add_image_part("image.jpg")

        Image_.from_file.assert_called_once_with("image.jpg")
        _get_by_sha1_.assert_called_once_with(image_parts, "f005ba11")
        assert image_part is image_part_

    def but_it_adds_a_new_image_part_when_match_fails(
        self,
        Image_: Mock,
        image_: Mock,
        _get_by_sha1_: Mock,
        _add_image_part_: Mock,
        image_part_: Mock,
    ):
        Image_.from_file.return_value = image_
        image_.sha1 = "fa1afe1"
        _get_by_sha1_.return_value = None
        _add_image_part_.return_value = image_part_
        image_parts = ImageParts()

        image_part = image_parts.get_or_add_image_part("image.png")

        Image_.from_file.assert_called_once_with("image.png")
        _get_by_sha1_.assert_called_once_with(image_parts, "fa1afe1")
        _add_image_part_.assert_called_once_with(image_parts, image_)
        assert image_part is image_part_

    @pytest.mark.parametrize(
        ("existing_partname_numbers", "expected_partname_number"),
        [
            ((2, 3), 1),
            ((1, 3), 2),
            ((1, 2), 3),
        ],
    )
    def it_knows_the_next_available_image_partname(
        self,
        request: FixtureRequest,
        existing_partname_numbers: tuple[int, int],
        expected_partname_number: int,
    ):
        image_parts = ImageParts()
        for n in existing_partname_numbers:
            image_parts.append(
                instance_mock(request, ImagePart, partname=PackURI(f"/word/media/image{n}.png"))
            )

        next_partname = image_parts._next_image_partname("png")

        assert next_partname == PackURI("/word/media/image%d.png" % expected_partname_number)

    def it_can_add_a_new_image_part(
        self,
        _next_image_partname_: Mock,
        image_: Mock,
        ImagePart_: Mock,
        image_part_: Mock,
    ):
        partname = PackURI("/word/media/image7.png")
        _next_image_partname_.return_value = partname
        ImagePart_.from_image.return_value = image_part_
        image_parts = ImageParts()

        image_part = image_parts._add_image_part(image_)

        ImagePart_.from_image.assert_called_once_with(image_, partname)
        assert image_part in image_parts
        assert image_part is image_part_

    # fixtures -------------------------------------------------------

    @pytest.fixture
    def _add_image_part_(self, request: FixtureRequest):
        return method_mock(request, ImageParts, "_add_image_part")

    @pytest.fixture
    def _get_by_sha1_(self, request: FixtureRequest):
        return method_mock(request, ImageParts, "_get_by_sha1")

    @pytest.fixture
    def Image_(self, request: FixtureRequest):
        return class_mock(request, "docx.package.Image")

    @pytest.fixture
    def image_(self, request: FixtureRequest):
        return instance_mock(request, Image)

    @pytest.fixture
    def ImagePart_(self, request: FixtureRequest):
        return class_mock(request, "docx.package.ImagePart")

    @pytest.fixture
    def image_part_(self, request: FixtureRequest):
        return instance_mock(request, ImagePart)

    @pytest.fixture
    def _next_image_partname_(self, request: FixtureRequest):
        return method_mock(request, ImageParts, "_next_image_partname")
