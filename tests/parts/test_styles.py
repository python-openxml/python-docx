# encoding: utf-8

"""
Test suite for the docx.parts.styles module
"""

from __future__ import absolute_import, print_function, unicode_literals

import pytest

from docx.opc.constants import CONTENT_TYPE as CT
from docx.opc.package import OpcPackage
from docx.oxml.styles import CT_Styles
from docx.parts.styles import StylesPart
from docx.styles.styles import Styles

from ..unitutil.mock import class_mock, instance_mock


class DescribeStylesPart(object):

    def it_provides_access_to_its_styles(self, styles_fixture):
        styles_part, Styles_, styles_ = styles_fixture
        styles = styles_part.styles
        Styles_.assert_called_once_with(styles_part.element)
        assert styles is styles_

    def it_can_construct_a_default_styles_part_to_help(self):
        package = OpcPackage()
        styles_part = StylesPart.default(package)
        assert isinstance(styles_part, StylesPart)
        assert styles_part.partname == '/word/styles.xml'
        assert styles_part.content_type == CT.WML_STYLES
        assert styles_part.package is package
        assert len(styles_part.element) == 6

    # fixtures -------------------------------------------------------

    @pytest.fixture
    def styles_fixture(self, Styles_, styles_elm_, styles_):
        styles_part = StylesPart(None, None, styles_elm_, None)
        return styles_part, Styles_, styles_

    # fixture components ---------------------------------------------

    @pytest.fixture
    def Styles_(self, request, styles_):
        return class_mock(
            request, 'docx.parts.styles.Styles', return_value=styles_
        )

    @pytest.fixture
    def styles_(self, request):
        return instance_mock(request, Styles)

    @pytest.fixture
    def styles_elm_(self, request):
        return instance_mock(request, CT_Styles)
