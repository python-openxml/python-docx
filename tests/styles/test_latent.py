# encoding: utf-8

"""
Unit test suite for the docx.styles.latent module
"""

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

import pytest

from docx.styles.latent import LatentStyles

from ..unitutil.cxml import element


class DescribeLatentStyles(object):

    def it_knows_how_many_latent_styles_it_contains(self, len_fixture):
        latent_styles, expected_value = len_fixture
        assert len(latent_styles) == expected_value

    # fixture --------------------------------------------------------

    @pytest.fixture(params=[
        ('w:latentStyles',                                  0),
        ('w:latentStyles/w:lsdException',                   1),
        ('w:latentStyles/(w:lsdException,w:lsdException)',  2),
    ])
    def len_fixture(self, request):
        latentStyles_cxml, count = request.param
        latent_styles = LatentStyles(element(latentStyles_cxml))
        return latent_styles, count
