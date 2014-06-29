# encoding: utf-8

"""
Test suite for docx.package module
"""

from __future__ import absolute_import, print_function, unicode_literals

import pytest

from docx.image.image import Image
from docx.opc.packuri import PackURI
from docx.package import ImageParts, Package
from docx.parts.image import ImagePart

from .unitutil.file import docx_path
from .unitutil.mock import class_mock, instance_mock, method_mock


class DescribePackage(object):

    def it_gathers_package_image_parts_after_unmarshalling(self):
        package = Package.open(docx_path('having-images'))
        image_parts = package.image_parts
        assert len(image_parts) == 3
        for image_part in image_parts:
            assert isinstance(image_part, ImagePart)


class DescribeImageParts(object):

    def it_can_get_a_matching_image_part(self, get_image_part_fixture):
        image_parts, image_descriptor, image_part_ = get_image_part_fixture
        image_part = image_parts.get_or_add_image_part(image_descriptor)
        assert image_part is image_part_

    def it_can_add_a_new_image_part(self, add_image_part_fixture):
        image_parts, image_descriptor, image_, image_part_ = (
            add_image_part_fixture
        )
        image_part = image_parts.get_or_add_image_part(image_descriptor)
        image_parts._add_image_part.assert_called_once_with(image_)
        assert image_part is image_part_

    def it_knows_the_next_available_image_partname(
            self, next_partname_fixture):
        image_parts, ext, expected_partname = next_partname_fixture
        assert image_parts._next_image_partname(ext) == expected_partname

    def it_can_really_add_a_new_image_part(
            self, really_add_image_part_fixture):
        image_parts, image_, ImagePart_, partname_, image_part_ = (
            really_add_image_part_fixture
        )
        image_part = image_parts._add_image_part(image_)
        ImagePart_.from_image.assert_called_once_with(image_, partname_)
        assert image_part in image_parts
        assert image_part is image_part_

    # fixtures -------------------------------------------------------

    @pytest.fixture
    def _add_image_part_(self, request, new_image_part_):
        return method_mock(
            request, ImageParts, '_add_image_part',
            return_value=new_image_part_
        )

    @pytest.fixture
    def add_image_part_fixture(
            self, Image_, _add_image_part_, image_descriptor_, image_,
            new_image_part_,):
        image_parts = ImageParts()
        return image_parts, image_descriptor_, image_, new_image_part_

    @pytest.fixture
    def get_image_part_fixture(self, Image_, image_part_, image_descriptor_):
        image_parts = ImageParts()
        image_parts.append(image_part_)
        return image_parts, image_descriptor_, image_part_

    @pytest.fixture
    def Image_(self, request, image_):
        Image_ = class_mock(request, 'docx.package.Image')
        Image_.from_file.return_value = image_
        return Image_

    @pytest.fixture
    def image_(self, request, sha1):
        image_ = instance_mock(request, Image)
        image_.sha1 = sha1
        return image_

    @pytest.fixture
    def image_descriptor_(self, request):
        return instance_mock(request, str)

    @pytest.fixture
    def ImagePart_(self, request, image_part_):
        ImagePart_ = class_mock(request, 'docx.package.ImagePart')
        ImagePart_.from_image.return_value = image_part_
        return ImagePart_

    @pytest.fixture
    def image_part_(self, request, sha1):
        image_part_ = instance_mock(request, ImagePart)
        image_part_.sha1 = sha1
        return image_part_

    def _image_part_with_partname_(self, request, n):
        partname = self._image_partname(n)
        return instance_mock(request, ImagePart, partname=partname)

    def _image_partname(self, n):
        return PackURI('/word/media/image%d.png' % n)

    @pytest.fixture
    def new_image_part_(self, request):
        return instance_mock(request, ImagePart)

    @pytest.fixture
    def _next_image_partname_(self, request):
        return method_mock(request, ImageParts, '_next_image_partname')

    @pytest.fixture(params=[((2, 3), 1), ((1, 3), 2), ((1, 2), 3)])
    def next_partname_fixture(self, request):
        existing_partname_numbers, expected_partname_number = request.param
        image_parts = ImageParts()
        for n in existing_partname_numbers:
            image_part_ = self._image_part_with_partname_(request, n)
            image_parts.append(image_part_)
        ext = 'png'
        expected_image_partname = self._image_partname(
            expected_partname_number
        )
        return image_parts, ext, expected_image_partname

    @pytest.fixture
    def partname_(self, request):
        return instance_mock(request, PackURI)

    @pytest.fixture
    def really_add_image_part_fixture(
            self, _next_image_partname_, partname_, image_, ImagePart_,
            image_part_):
        image_parts = ImageParts()
        _next_image_partname_.return_value = partname_
        return image_parts, image_, ImagePart_, partname_, image_part_

    @pytest.fixture
    def sha1(self):
        return 'F008AH'
