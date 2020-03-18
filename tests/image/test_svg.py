# encoding: utf-8

"""Unit test suite for docx.image.svg module"""

from __future__ import absolute_import, print_function

import pytest

from docx.compat import BytesIO
from docx.image.constants import MIME_TYPE
from docx.image.svg import Svg

from ..unitutil.mock import ANY, initializer_mock


class DescribeSvg(object):

    def it_can_construct_from_a_svg_stream(self, Svg__init__):
        cx, cy = 81.56884, 17.054602
        bytes_ = b"""\
<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<svg
   xmlns:dc="http://purl.org/dc/elements/1.1/"
   xmlns:cc="http://creativecommons.org/ns#"
   xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
   xmlns:svg="http://www.w3.org/2000/svg"
   xmlns="http://www.w3.org/2000/svg"
   id="svg883"
   version="1.1"
   viewBox="0 0 81.56884 17.054602"
   height="17.054602mm"
   width="81.56884mm">
  <defs
     id="defs877" />
  <metadata
     id="metadata880">
    <rdf:RDF>
      <cc:Work
         rdf:about="">
        <dc:format>image/svg+xml</dc:format>
        <dc:type
           rdf:resource="http://purl.org/dc/dcmitype/StillImage" />
        <dc:title />
      </cc:Work>
    </rdf:RDF>
  </metadata>
  <g
     transform="translate(238.27068,33.733892)"
     id="layer1">
    <text
       id="text843"
       y="-16.976948"
       x="-238.27068"
       style="font-style:normal;font-weight:normal;font-size:22.57777786px;line-height:1.25;font-family:sans-serif;letter-spacing:0px;word-spacing:0px;fill:#000000;fill-opacity:1;stroke:none;stroke-width:0.26458332"
       xml:space="preserve"><tspan
         style="stroke-width:0.26458332"
         y="-16.976948"
         x="-238.27068"
         id="tspan841">Test 2 !</tspan></text>
    <flowRoot
       transform="matrix(0.26458333,0,0,0.26458333,-238.27068,-33.392139)"
       style="font-style:normal;font-weight:normal;font-size:85.33333588px;line-height:1.25;font-family:sans-serif;letter-spacing:0px;word-spacing:0px;fill:#000000;fill-opacity:1;stroke:none"
       id="flowRoot814"
       xml:space="preserve"><flowRegion
         id="flowRegion816"><rect
           y="-63.976192"
           x="-182.85715"
           height="248.57143"
           width="880"
           id="rect818" /></flowRegion><flowPara
         id="flowPara820" /></flowRoot>  </g>
</svg>"""
        stream = BytesIO(bytes_)

        svg = Svg.from_stream(stream)

        Svg__init__.assert_called_once_with(ANY, cx, cy, 72, 72)
        assert isinstance(svg, Svg)

    def it_knows_its_content_type(self):
        svg = Svg(None, None, None, None)
        assert svg.content_type == MIME_TYPE.SVG

    def it_knows_its_default_ext(self):
        svg = Svg(None, None, None, None)
        assert svg.default_ext == 'svg'

    # fixture components ---------------------------------------------

    @pytest.fixture
    def Svg__init__(self, request):
        return initializer_mock(request, Svg)
