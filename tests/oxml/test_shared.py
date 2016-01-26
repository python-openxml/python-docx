# encoding: utf-8

"""
Test suite for the docx.oxml.shared module
"""

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)
import pytest
from ..unitutil.cxml import element, xml
from docx.oxml.text.paragraph import CT_P
from docx.oxml.text.parfmt import CT_PPr
from docx.oxml.text.run import CT_R
from docx.oxml.text.font import CT_RPr
from docx.oxml.shared import CT_Shd
from docx.oxml.table import CT_Tc, CT_TcPr, CT_Tbl, CT_TblPr


class Describe_CT_Shd(object):
    def it_is_registered(self, registration_fixture):
        shading = registration_fixture
        assert shading.val == 'nil'

    def it_raises_on_incorrect_value(self, incorrect_value_fixture):
        with pytest.raises(ValueError):
            e = incorrect_value_fixture
            e.val = 'asdf'

    # fixtures -------------------------------------------------------

    @pytest.fixture(params=[
        'w:shd{w:val=nil}',

        'w:p/w:pPr/w:shd{w:val=nil}',
        'w:r/w:rPr/w:shd{w:val=nil}',

        'w:rPr/w:shd{w:val=nil}',
        'w:pPr/w:shd{w:val=nil}',

        'w:tc/w:tcPr/w:shd{w:val=nil}',
        'w:tcPr/w:shd{w:val=nil}',

        'w:tbl/w:tblPr/w:shd{w:val=nil}',
        'w:tblPr/w:shd{w:val=nil}'
    ])
    def registration_fixture(self, request):
        cxml = request.param

        e = element(cxml)
        if isinstance(e, CT_Shd):
            shd = e
        elif isinstance(e, CT_P):
            shd = e.pPr.shd
        elif isinstance(e, CT_R):
            shd = e.rPr.shd
        elif isinstance(e, CT_Tc):
            shd = e.tcPr.shd
        elif isinstance(e, CT_Tbl):
            shd = e.tblPr.shd
        elif type(e) in (CT_PPr, CT_RPr, CT_TcPr, CT_TblPr):
            shd = e.shd
        else:
            raise NotImplementedError("Shading is not part of the object type " + str(type(e)))
        return shd

    @pytest.fixture
    def incorrect_value_fixture(self):
        e = element('w:shd{w:val=nil}')
        return e
