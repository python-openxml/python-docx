# encoding: utf-8

"""
Test suite for docx.parts.image module
"""

from __future__ import absolute_import, print_function, unicode_literals

import pytest

from docx.opc.constants import CONTENT_TYPE as CT, RELATIONSHIP_TYPE as RT
from docx.opc.package import PartFactory
from docx.opc.packuri import PackURI
from docx.package import Package
from docx.parts.image import Image, ImagePart

from ..unitutil import (
    initializer_mock, instance_mock, method_mock, test_file
)


class DescribeImage(object):

    def it_can_construct_from_an_image_path(self):
        image_file_path = test_file('monty-truth.png')
        image = Image.load(image_file_path)
        assert isinstance(image, Image)
        assert image.sha1 == '79769f1e202add2e963158b532e36c2c0f76a70c'
        assert image.filename == 'monty-truth.png'

    def it_can_construct_from_an_image_stream(self):
        image_file_path = test_file('monty-truth.png')
        with open(image_file_path, 'rb') as image_file_stream:
            image = Image.load(image_file_stream)
        assert isinstance(image, Image)
        assert image.sha1 == '79769f1e202add2e963158b532e36c2c0f76a70c'
        assert image.filename is None


class DescribeImagePart(object):

    def it_is_used_by_PartFactory_to_construct_image_part(self, load_fixture):
        # fixture ----------------------
        image_part_load_, partname_, blob_, package_, image_part_ = (
            load_fixture
        )
        content_type = CT.JPEG
        reltype = RT.IMAGE
        # exercise ---------------------
        part = PartFactory(partname_, content_type, reltype, blob_, package_)
        # verify -----------------------
        image_part_load_.assert_called_once_with(
            partname_, content_type, blob_, package_
        )
        assert part is image_part_

    def it_can_construct_from_image_instance(self, from_image_fixture):
        image_, partname_, ImagePart__init__ = from_image_fixture
        image_part = ImagePart.from_image(image_, partname_)
        ImagePart__init__.assert_called_once_with(
            partname_, image_.content_type, image_.blob, image_
        )
        assert isinstance(image_part, ImagePart)

    # fixtures -------------------------------------------------------

    @pytest.fixture
    def blob_(self, request):
        return instance_mock(request, str)

    @pytest.fixture
    def from_image_fixture(self, image_, partname_, ImagePart__init__):
        return image_, partname_, ImagePart__init__

    @pytest.fixture
    def image_(self, request):
        return instance_mock(request, Image)

    @pytest.fixture
    def ImagePart__init__(self, request):
        return initializer_mock(request, ImagePart)

    @pytest.fixture
    def image_part_(self, request):
        return instance_mock(request, ImagePart)

    @pytest.fixture
    def image_part_load_(self, request, image_part_):
        return method_mock(
            request, ImagePart, 'load', return_value=image_part_
        )

    @pytest.fixture
    def load_fixture(
            self, image_part_load_, partname_, blob_, package_, image_part_):
        return image_part_load_, partname_, blob_, package_, image_part_

    @pytest.fixture
    def package_(self, request):
        return instance_mock(request, Package)

    @pytest.fixture
    def partname_(self, request):
        return instance_mock(request, PackURI)
