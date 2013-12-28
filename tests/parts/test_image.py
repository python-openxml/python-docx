# encoding: utf-8

"""
Test suite for docx.parts.image module
"""

from __future__ import absolute_import, print_function, unicode_literals

from docx.parts.image import Image

from ..unitutil import test_file


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
