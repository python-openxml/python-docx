# encoding: utf-8

"""
Test suite for docx.package module
"""

from __future__ import absolute_import, print_function, unicode_literals

from docx.package import Package

from .unitutil import docx_path


class DescribePackage(object):

    def it_gathers_package_image_parts_after_unmarshalling(self):
        package = Package.open(docx_path('having-images'))
        assert len(package.image_parts) == 3
