# encoding: utf-8

"""Unit test suite for docx.parts.image module"""

from __future__ import absolute_import, division, print_function, unicode_literals

import pytest

from docx.image.image import Image
from docx.opc.constants import CONTENT_TYPE as CT, RELATIONSHIP_TYPE as RT
from docx.opc.packuri import PackURI
from docx.opc.part import PartFactory
from docx.package import Package
from docx.parts.image import ImagePart

from ..unitutil.file import test_file
from ..unitutil.mock import ANY, initializer_mock, instance_mock, method_mock


class DescribeImagePart(object):

    def it_is_used_by_PartFactory_to_construct_image_part(
        self, image_part_load_, partname_, blob_, package_, image_part_
    ):
        content_type = CT.JPEG
        reltype = RT.IMAGE
        image_part_load_.return_value = image_part_

        part = PartFactory(partname_, content_type, reltype, blob_, package_)

        image_part_load_.assert_called_once_with(
            partname_, content_type, blob_, package_
        )
        assert part is image_part_

    def it_can_construct_from_an_Image_instance(self, image_, partname_, _init_):
        image_part = ImagePart.from_image(image_, partname_)

        _init_.assert_called_once_with(
            ANY, partname_, image_.content_type, image_.blob, image_
        )
        assert isinstance(image_part, ImagePart)

    def it_knows_its_default_dimensions_in_EMU(self, dimensions_fixture):
        image_part, cx, cy = dimensions_fixture
        assert image_part.default_cx == cx
        assert image_part.default_cy == cy

    def it_knows_its_filename(self, filename_fixture):
        image_part, expected_filename = filename_fixture
        assert image_part.filename == expected_filename

    def it_knows_the_sha1_of_its_image(self):
        blob = b'fO0Bar'
        image_part = ImagePart(None, None, blob)
        assert image_part.sha1 == '4921e7002ddfba690a937d54bda226a7b8bdeb68'

    # fixtures -------------------------------------------------------

    @pytest.fixture
    def blob_(self, request):
        return instance_mock(request, str)

    @pytest.fixture(params=['loaded', 'new'])
    def dimensions_fixture(self, request):
        image_file_path = test_file('monty-truth.png')
        image = Image.from_file(image_file_path)
        expected_cx, expected_cy = 1905000, 2717800

        # case 1: image part is loaded by PartFactory w/no Image inst
        if request.param == 'loaded':
            partname = PackURI('/word/media/image1.png')
            content_type = CT.PNG
            image_part = ImagePart.load(
                partname, content_type, image.blob, None
            )
        # case 2: image part is newly created from image file
        elif request.param == 'new':
            image_part = ImagePart.from_image(image, None)

        return image_part, expected_cx, expected_cy

    @pytest.fixture(params=['loaded', 'new'])
    def filename_fixture(self, request, image_):
        partname = PackURI('/word/media/image666.png')
        if request.param == 'loaded':
            image_part = ImagePart(partname, None, None, None)
            expected_filename = 'image.png'
        elif request.param == 'new':
            image_.filename = 'foobar.PXG'
            image_part = ImagePart(partname, None, None, image_)
            expected_filename = image_.filename
        return image_part, expected_filename

    @pytest.fixture
    def image_(self, request):
        return instance_mock(request, Image)

    @pytest.fixture
    def _init_(self, request):
        return initializer_mock(request, ImagePart)

    @pytest.fixture
    def image_part_(self, request):
        return instance_mock(request, ImagePart)

    @pytest.fixture
    def image_part_load_(self, request):
        return method_mock(request, ImagePart, 'load', autospec=False)

    @pytest.fixture
    def package_(self, request):
        return instance_mock(request, Package)

    @pytest.fixture
    def partname_(self, request):
        return instance_mock(request, PackURI)
