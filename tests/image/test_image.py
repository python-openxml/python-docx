# encoding: utf-8

"""
Test suite for docx.image package
"""

from __future__ import absolute_import, print_function, unicode_literals

import pytest

from docx.image import Image_OLD
from docx.opc.constants import CONTENT_TYPE as CT

from ..unitutil import test_file


class DescribeImage_OLD(object):

    def it_can_construct_from_an_image_path(self):
        image_file_path = test_file('monty-truth.png')
        image = Image_OLD.from_file(image_file_path)
        assert isinstance(image, Image_OLD)
        assert image.sha1 == '79769f1e202add2e963158b532e36c2c0f76a70c'
        assert image.filename == 'monty-truth.png'

    def it_can_construct_from_an_image_stream(self):
        image_file_path = test_file('monty-truth.png')
        with open(image_file_path, 'rb') as image_file_stream:
            image = Image_OLD.from_file(image_file_stream)
        assert isinstance(image, Image_OLD)
        assert image.sha1 == '79769f1e202add2e963158b532e36c2c0f76a70c'
        assert image.filename == 'image.png'

    def it_knows_the_extension_of_a_file_based_image(self):
        image_file_path = test_file('monty-truth.png')
        image = Image_OLD.from_file(image_file_path)
        assert image.ext == '.png'

    def it_knows_the_extension_of_a_stream_based_image(self):
        image_file_path = test_file('monty-truth.png')
        with open(image_file_path, 'rb') as image_file_stream:
            image = Image_OLD.from_file(image_file_stream)
        assert image.ext == '.png'

    def it_correctly_characterizes_a_few_known_images(
            self, known_image_fixture):
        image_path, characteristics = known_image_fixture
        ext, content_type, px_width, px_height, horz_dpi, vert_dpi = (
            characteristics
        )
        with open(test_file(image_path), 'rb') as stream:
            image = Image_OLD.from_file(stream)
            assert image.ext == ext
            assert image.content_type == content_type
            assert image.px_width == px_width
            assert image.px_height == px_height
            assert image.horz_dpi == horz_dpi
            assert image.vert_dpi == vert_dpi

    # fixtures -------------------------------------------------------

    @pytest.fixture(params=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
    def known_image_fixture(self, request):
        cases = (
            ('python.bmp',       ('.bmp',  CT.BMP,   211,   71,  72,  72)),
            ('sonic.gif',        ('.gif',  CT.GIF,   290,  360,  72,  72)),
            ('python-icon.jpeg', ('.jpg',  CT.JPEG,  204,  204,  72,  72)),
            ('300-dpi.jpg',      ('.jpg',  CT.JPEG, 1504, 1936, 300, 300)),
            ('monty-truth.png',  ('.png',  CT.PNG,   150,  214,  72,  72)),
            ('150-dpi.png',      ('.png',  CT.PNG,   901, 1350, 150, 150)),
            ('300-dpi.png',      ('.png',  CT.PNG,   860,  579, 300, 300)),
            ('72-dpi.tiff',      ('.tiff', CT.TIFF,   48,   48,  72,  72)),
            ('300-dpi.TIF',      ('.tiff', CT.TIFF, 2464, 3248, 300, 300)),
            ('CVS_LOGO.WMF',     ('.wmf',  CT.X_WMF, 149,   59,  72,  72)),
        )
        image_filename, characteristics = cases[request.param]
        return image_filename, characteristics
