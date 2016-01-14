# encoding: utf-8

"""
Test suite for the docx.oxml.styles module.
"""

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)
import pytest

from docx.mixins.PrMixin import PrMixin
from docx.oxml import CT_R, CT_P, CT_Tc
from docx.shared import RGBColor
from docx.mixins.ShdMixin import ShdMixin
from docx.table import _Cell
from docx.text.paragraph import Paragraph
from docx.text.run import Run
from .unitutil.cxml import element, xml
from .unitutil.mock import class_mock, instance_mock
from docx.shading import Shd
from docx.dml.color import ColorFormat
from docx.shared import ElementProxy


class Describe_ShdMixin(object):
    class Test_Doc_Shd(ShdMixin, ElementProxy):
        pass

    def it_knows_its_shd_val(self, shd_val_get_fixture):
        obj, expected_value = shd_val_get_fixture
        assert obj.shd_val == expected_value

    def it_can_change_its_shd_val(self, shd_val_set_fixture):
        obj, expected_val = shd_val_set_fixture
        assert obj.shd_val == expected_val

    def it_knows_its_shd_color(self, shd_color_get_fixture):
        obj, expected_value = shd_color_get_fixture
        assert obj.shd_color == expected_value

    def it_can_change_its_shd_color(self, shd_color_set_fixture):
        obj, expected_val = shd_color_set_fixture
        assert str(obj.shd_color) == expected_val

    def it_knows_its_shd_fill(self, shd_fill_get_fixture):
        obj, expected_value = shd_fill_get_fixture
        assert obj.shd_fill == expected_value

    def it_can_change_its_shd_fill(self, shd_fill_set_fixture):
        obj, expected_val = shd_fill_set_fixture
        assert str(obj.shd_fill) == expected_val

    def it_knows_its_shd_themeColor(self, shd_themeColor_get_fixture):
        obj, expected_value = shd_themeColor_get_fixture
        assert obj.shd_themeColor == expected_value

    def it_can_change_its_shd_themeColor(self, shd_themeColor_set_fixture):
        obj, expected_val = shd_themeColor_set_fixture
        assert str(obj.shd_themeColor) == expected_val

    def it_knows_its_shd_themeFill(self, shd_themeFill_get_fixture):
        obj, expected_value = shd_themeFill_get_fixture
        assert obj.shd_themeFill == expected_value

    def it_can_change_its_shd_themeFill(self, shd_themeFill_set_fixture):
        obj, expected_val = shd_themeFill_set_fixture
        assert str(obj.shd_themeFill) == expected_val

    def it_knows_its_shd_themeFillShade(self, shd_themeFillShade_get_fixture):
        obj, expected_value = shd_themeFillShade_get_fixture
        assert obj.shd_themeFillShade == expected_value

    def it_can_change_its_shd_themeFillShade(self, shd_themeFillShade_set_fixture):
        obj, expected_val = shd_themeFillShade_set_fixture
        assert str(obj.shd_themeFillShade) == expected_val

    def it_knows_its_shd_themeFillTint(self, shd_themeFillTint_get_fixture):
        obj, expected_value = shd_themeFillTint_get_fixture
        assert obj.shd_themeFillTint == expected_value

    def it_can_change_its_shd_themeFillTint(self, shd_themeFillTint_set_fixture):
        obj, expected_val = shd_themeFillTint_set_fixture
        assert str(obj.shd_themeFillTint) == expected_val

    def it_knows_its_shd_themeShade(self, shd_themeShade_get_fixture):
        obj, expected_value = shd_themeShade_get_fixture
        assert obj.shd_themeShade == expected_value

    def it_can_change_its_shd_themeShade(self, shd_themeShade_set_fixture):
        obj, expected_val = shd_themeShade_set_fixture
        assert str(obj.shd_themeShade) == expected_val

    def it_knows_its_shd_themeTint(self, shd_themeTint_get_fixture):
        obj, expected_value = shd_themeTint_get_fixture
        assert obj.shd_themeTint == expected_value

    def it_can_change_its_shd_themeTint(self, shd_themeTint_set_fixture):
        obj, expected_val = shd_themeTint_set_fixture
        assert str(obj.shd_themeTint) == expected_val

    def it_should_raise_on_unsupported_object_get(self):
        with pytest.raises(AttributeError):
            doc = Describe_ShdMixin.Test_Doc_Shd(element('w:document'), None)
            doc.shd_val

    def it_should_raise_on_unsupported_object_set(self):
        with pytest.raises(AttributeError):
            doc = Describe_ShdMixin.Test_Doc_Shd(element('w:document'), None)
            doc.shd_val = 'nil'

    # fixtures -----------------------------------------------------------

    @pytest.fixture(params=[
        ('w:r', None),
        ('w:r/w:rPr', None),
        ('w:r/w:rPr/w:shd{w:val=clear}', 'clear'),
        ('w:r/w:rPr/w:shd{w:val=clear,w:fill=C3D69B}', 'clear'),

        ('w:p', None),
        ('w:p/w:pPr', None),
        ('w:p/w:pPr/w:shd{w:val=clear}', 'clear'),
        ('w:p/w:pPr/w:shd{w:val=clear,w:fill=C3D69B}', 'clear'),

        ('w:tc', None),
        ('w:tc/w:tcPr', None),
        ('w:tc/w:tcPr/w:shd{w:val=clear}', 'clear'),
        ('w:tc/w:tcPr/w:shd{w:val=clear,w:fill=C3D69B}', 'clear'),
    ])
    def shd_val_get_fixture(self, request):
        cxml, expected_value = request.param
        e = element(cxml)
        if isinstance(e, CT_R):
            obj = Run(e, None)
        elif isinstance(e, CT_P):
            obj = Paragraph(e, None)
        elif isinstance(e, CT_Tc):
            obj = _Cell(e, None)
        else:
            obj = None
        return obj, expected_value

    @pytest.fixture(params=[
        ('w:r', 'clear', 'clear'),
        ('w:r/w:rPr', 'diagCross', 'diagCross'),
        ('w:r/w:rPr/w:shd{w:val=diagCross}', 'diagStripe', 'diagStripe'),
        ('w:r/w:rPr/w:shd{w:val=horzCross,w:fill=C3D69B}', 'horzStripe', 'horzStripe'),

        ('w:p', 'clear', 'clear'),
        ('w:p/w:pPr', 'diagCross', 'diagCross'),
        ('w:p/w:pPr/w:shd{w:val=diagCross}', 'diagStripe', 'diagStripe'),
        ('w:p/w:pPr/w:shd{w:val=horzCross,w:fill=C3D69B}', 'horzStripe', 'horzStripe'),

        ('w:tc', 'clear', 'clear'),
        ('w:tc/w:rPr', 'diagCross', 'diagCross'),
        ('w:tc/w:tcPr/w:shd{w:val=diagCross}', 'diagStripe', 'diagStripe'),
        ('w:tc/w:tcPr/w:shd{w:val=horzCross,w:fill=C3D69B}', 'horzStripe', 'horzStripe'),
    ])
    def shd_val_set_fixture(self, request):
        cxml, value, expected_value = request.param
        e = element(cxml)
        if isinstance(e, CT_R):
            obj = Run(e, None)
        elif isinstance(e, CT_P):
            obj = Paragraph(e, None)
        elif isinstance(e, CT_Tc):
            obj = _Cell(e, None)
        else:
            obj = None

        obj.shd_val = value
        return obj, expected_value

    @pytest.fixture(params=[
        ('w:r', None),
        ('w:r/w:rPr', None),
        ('w:r/w:rPr/w:shd', None),
        ('w:r/w:rPr/w:shd{w:val=nil,w:color=auto}', 'auto'),
        ('w:r/w:rPr/w:shd{w:val=nil,w:color=FA0123}', RGBColor.from_string('FA0123')),
        ('w:r/w:rPr/w:shd{w:val=nil,w:color=FF0012,w:fill=C3D69B}', RGBColor.from_string('FF0012')),

        ('w:p', None),
        ('w:p/w:rPr', None),
        ('w:p/w:pPr/w:shd', None),
        ('w:p/w:pPr/w:shd{w:val=nil,w:color=auto}', 'auto'),

        ('w:tc', None),
        ('w:tc/w:tcPr', None),
        ('w:tc/w:tcPr/w:shd', None),
        ('w:tc/w:tcPr/w:shd{w:val=nil,w:color=auto}', 'auto'),
    ])
    def shd_color_get_fixture(self, request):
        cxml, expected_value = request.param
        e = element(cxml)
        if isinstance(e, CT_R):
            obj = Run(e, None)
        elif isinstance(e, CT_P):
            obj = Paragraph(e, None)
        elif isinstance(e, CT_Tc):
            obj = _Cell(e, None)
        else:
            obj = None
        return obj, expected_value

    @pytest.fixture(params=[
        ('w:r', RGBColor.from_string('AB9019'), 'AB9019'),
        ('w:r/w:rPr', RGBColor.from_string('F0C0D0'), 'F0C0D0'),
        ('w:r/w:rPr/w:shd{w:color=FFFFFF}', 'auto', 'auto'),
        ('w:r/w:rPr/w:shd{w:color=FFFFFF}', RGBColor.from_string('ADF123'), 'ADF123'),

        ('w:p', RGBColor.from_string('AB9019'), 'AB9019'),
        ('w:p/w:pPr', RGBColor.from_string('F0C0D0'), 'F0C0D0'),
        ('w:p/w:pPr/w:shd{w:color=FFFFFF}', 'auto', 'auto'),
        ('w:p/w:pPr/w:shd{w:color=FFFFFF}', RGBColor.from_string('ADF123'), 'ADF123'),

        ('w:tc', RGBColor.from_string('AB9019'), 'AB9019'),
        ('w:tc/w:tcPr', RGBColor.from_string('F0C0D0'), 'F0C0D0'),
        ('w:tc/w:tcPr/w:shd{w:color=FFFFFF}', 'auto', 'auto'),
        ('w:tc/w:tcPr/w:shd{w:color=FFFFFF}', RGBColor.from_string('ADF123'), 'ADF123'),
    ])
    def shd_color_set_fixture(self, request):
        cxml, value, expected_value = request.param
        e = element(cxml)
        if isinstance(e, CT_R):
            obj = Run(e, None)
        elif isinstance(e, CT_P):
            obj = Paragraph(e, None)
        elif isinstance(e, CT_Tc):
            obj = _Cell(e, None)
        else:
            obj = None

        obj.shd_color = value
        return obj, expected_value

    @pytest.fixture(params=[
        ('w:r', None),
        ('w:r/w:rPr', None),
        ('w:r/w:rPr/w:shd{w:val=nil,w:fill=auto}', 'auto'),
        ('w:r/w:rPr/w:shd{w:val=nil,w:fill=FA0123}', RGBColor.from_string('FA0123')),

        ('w:p', None),
        ('w:p/w:rPr', None),
        ('w:p/w:pPr/w:shd{w:val=nil,w:fill=auto}', 'auto'),

        ('w:tc', None),
        ('w:tc/w:tcPr', None),
        ('w:tc/w:tcPr/w:shd{w:val=nil,w:fill=auto}', 'auto'),
    ])
    def shd_fill_get_fixture(self, request):
        cxml, expected_value = request.param
        e = element(cxml)
        if isinstance(e, CT_R):
            obj = Run(e, None)
        elif isinstance(e, CT_P):
            obj = Paragraph(e, None)
        elif isinstance(e, CT_Tc):
            obj = _Cell(e, None)
        else:
            obj = None
        return obj, expected_value

    @pytest.fixture(params=[
        ('w:r', RGBColor.from_string('AB9019'), 'AB9019'),
        ('w:r/w:rPr', RGBColor.from_string('F0C0D0'), 'F0C0D0'),
        ('w:r/w:rPr/w:shd{w:fill=FFFFFF}', 'auto', 'auto'),
        ('w:r/w:rPr/w:shd{w:fill=FFFFFF}', RGBColor.from_string('ADF123'), 'ADF123'),

        ('w:p', RGBColor.from_string('AB9019'), 'AB9019'),
        ('w:p/w:pPr', RGBColor.from_string('F0C0D0'), 'F0C0D0'),
        ('w:p/w:pPr/w:shd{w:fill=FFFFFF}', 'auto', 'auto'),
        ('w:p/w:pPr/w:shd{w:fill=FFFFFF}', RGBColor.from_string('ADF123'), 'ADF123'),

        ('w:tc', RGBColor.from_string('AB9019'), 'AB9019'),
        ('w:tc/w:tcPr', RGBColor.from_string('F0C0D0'), 'F0C0D0'),
        ('w:tc/w:tcPr/w:shd{w:fill=FFFFFF}', 'auto', 'auto'),
        ('w:tc/w:tcPr/w:shd{w:fill=FFFFFF}', RGBColor.from_string('ADF123'), 'ADF123'),
    ])
    def shd_fill_set_fixture(self, request):
        cxml, value, expected_value = request.param
        e = element(cxml)
        if isinstance(e, CT_R):
            obj = Run(e, None)
        elif isinstance(e, CT_P):
            obj = Paragraph(e, None)
        elif isinstance(e, CT_Tc):
            obj = _Cell(e, None)
        else:
            obj = None

        obj.shd_fill = value
        return obj, expected_value

    @pytest.fixture(params=[
        ('w:r', None),
        ('w:r/w:rPr', None),
        ('w:r/w:rPr/w:shd{w:val=nil,w:themeColor=dark1}', 'dark1'),
        ('w:r/w:rPr/w:shd{w:val=nil,w:themeColor=light1}', 'light1'),

        ('w:p', None),
        ('w:p/w:pPr', None),
        ('w:p/w:pPr/w:shd{w:val=nil,w:themeColor=accent1}', 'accent1'),
        ('w:p/w:pPr/w:shd{w:val=nil,w:themeColor=accent2}', 'accent2'),

        ('w:tc', None),
        ('w:tc/w:tcPr', None),
        ('w:tc/w:tcPr/w:shd{w:val=nil,w:themeColor=accent3}', 'accent3'),
        ('w:tc/w:tcPr/w:shd{w:val=nil,w:themeColor=accent4}', 'accent4'),
    ])
    def shd_themeColor_get_fixture(self, request):
        cxml, expected_themeColorue = request.param
        e = element(cxml)
        if isinstance(e, CT_R):
            obj = Run(e, None)
        elif isinstance(e, CT_P):
            obj = Paragraph(e, None)
        elif isinstance(e, CT_Tc):
            obj = _Cell(e, None)
        else:
            obj = None
        return obj, expected_themeColorue

    @pytest.fixture(params=[
        ('w:r', 'accent5', 'accent5'),
        ('w:r/w:rPr', 'accent6', 'accent6'),
        ('w:r/w:rPr/w:shd{w:themeColor=diagCross}', 'hyperlink', 'hyperlink'),
        ('w:r/w:rPr/w:shd{w:themeColor=horzCross,w:fill=C3D69B}', 'followedHyperlink', 'followedHyperlink'),

        ('w:p', 'none', 'none'),
        ('w:p/w:pPr', 'background1', 'background1'),
        ('w:p/w:pPr/w:shd{w:themeColor=diagCross}', 'background2', 'background2'),
        ('w:p/w:pPr/w:shd{w:themeColor=horzCross,w:fill=C3D69B}', 'text2', 'text2'),

        ('w:tc', 'light2', 'light2'),
        ('w:tc/w:rPr', 'dark2', 'dark2'),
        ('w:tc/w:tcPr/w:shd{w:themeColor=diagCross}', 'light1', 'light1'),
        ('w:tc/w:tcPr/w:shd{w:themeColor=horzCross,w:fill=C3D69B}', 'dark1', 'dark1'),
    ])
    def shd_themeColor_set_fixture(self, request):
        cxml, themeColorue, expected_themeColorue = request.param
        e = element(cxml)
        if isinstance(e, CT_R):
            obj = Run(e, None)
        elif isinstance(e, CT_P):
            obj = Paragraph(e, None)
        elif isinstance(e, CT_Tc):
            obj = _Cell(e, None)
        else:
            obj = None

        obj.shd_themeColor = themeColorue
        return obj, expected_themeColorue

    @pytest.fixture(params=[
        ('w:r', None),
        ('w:r/w:rPr', None),
        ('w:r/w:rPr/w:shd{w:val=nil,w:themeFill=dark1}', 'dark1'),
        ('w:r/w:rPr/w:shd{w:val=nil,w:themeFill=light1}', 'light1'),

        ('w:p', None),
        ('w:p/w:pPr', None),
        ('w:p/w:pPr/w:shd{w:val=nil,w:themeFill=accent1}', 'accent1'),
        ('w:p/w:pPr/w:shd{w:val=nil,w:themeFill=accent2}', 'accent2'),

        ('w:tc', None),
        ('w:tc/w:tcPr', None),
        ('w:tc/w:tcPr/w:shd{w:val=nil,w:themeFill=accent3}', 'accent3'),
        ('w:tc/w:tcPr/w:shd{w:val=nil,w:themeFill=accent4}', 'accent4'),
    ])
    def shd_themeFill_get_fixture(self, request):
        cxml, expected_themeFill = request.param
        e = element(cxml)
        if isinstance(e, CT_R):
            obj = Run(e, None)
        elif isinstance(e, CT_P):
            obj = Paragraph(e, None)
        elif isinstance(e, CT_Tc):
            obj = _Cell(e, None)
        else:
            obj = None
        return obj, expected_themeFill

    @pytest.fixture(params=[
        ('w:r', 'accent5', 'accent5'),
        ('w:r/w:rPr', 'accent6', 'accent6'),
        ('w:r/w:rPr/w:shd{w:themeFill=diagCross}', 'hyperlink', 'hyperlink'),
        ('w:r/w:rPr/w:shd{w:themeFill=horzCross,w:fill=C3D69B}', 'followedHyperlink', 'followedHyperlink'),

        ('w:p', 'none', 'none'),
        ('w:p/w:pPr', 'background1', 'background1'),
        ('w:p/w:pPr/w:shd{w:themeFill=diagCross}', 'background2', 'background2'),
        ('w:p/w:pPr/w:shd{w:themeFill=horzCross,w:fill=C3D69B}', 'text2', 'text2'),

        ('w:tc', 'light2', 'light2'),
        ('w:tc/w:rPr', 'dark2', 'dark2'),
        ('w:tc/w:tcPr/w:shd{w:themeFill=diagCross}', 'light1', 'light1'),
        ('w:tc/w:tcPr/w:shd{w:themeFill=horzCross,w:fill=C3D69B}', 'dark1', 'dark1'),
    ])
    def shd_themeFill_set_fixture(self, request):
        cxml, themeFill, expected_themeFill = request.param
        e = element(cxml)
        if isinstance(e, CT_R):
            obj = Run(e, None)
        elif isinstance(e, CT_P):
            obj = Paragraph(e, None)
        elif isinstance(e, CT_Tc):
            obj = _Cell(e, None)
        else:
            obj = None

        obj.shd_themeFill = themeFill
        return obj, expected_themeFill

    @pytest.fixture(params=[
        ('w:r', None),
        ('w:r/w:rPr', None),
        ('w:r/w:rPr/w:shd{w:val=nil,w:themeFillShade=AB}', 'AB'),
        ('w:r/w:rPr/w:shd{w:val=nil,w:themeFillShade=BF}', 'BF'),

        ('w:p', None),
        ('w:p/w:pPr', None),
        ('w:p/w:pPr/w:shd{w:val=nil,w:themeFillShade=E0}', 'E0'),
        ('w:p/w:pPr/w:shd{w:val=nil,w:themeFillShade=1F}', '1F'),

        ('w:tc', None),
        ('w:tc/w:tcPr', None),
        ('w:tc/w:tcPr/w:shd{w:val=nil,w:themeFillShade=A4}', 'A4'),
        ('w:tc/w:tcPr/w:shd{w:val=nil,w:themeFillShade=F2}', 'F2'),
    ])
    def shd_themeFillShade_get_fixture(self, request):
        cxml, expected_themeFillShade = request.param
        e = element(cxml)
        if isinstance(e, CT_R):
            obj = Run(e, None)
        elif isinstance(e, CT_P):
            obj = Paragraph(e, None)
        elif isinstance(e, CT_Tc):
            obj = _Cell(e, None)
        else:
            obj = None
        return obj, expected_themeFillShade

    @pytest.fixture(params=[
        ('w:r', 'A0', 'A0'),
        ('w:r/w:rPr', 'F1', 'F1'),
        ('w:r/w:rPr/w:shd{w:themeFillShade=F0}', 'D8', 'D8'),
        ('w:r/w:rPr/w:shd{w:themeFillShade=F0,w:fill=none}', 'E5', 'E5'),

        ('w:p', '7F', '7F'),
        ('w:p/w:pPr', '2C', '2C'),
        ('w:p/w:pPr/w:shd{w:themeFillShade=F0}', '0A', '0A'),
        ('w:p/w:pPr/w:shd{w:themeFillShade=F0,w:fill=none}', '1C', '1C'),

        ('w:tc', 'B2', 'B2'),
        ('w:tc/w:rPr', '2B', '2B'),
        ('w:tc/w:tcPr/w:shd{w:themeFillShade=F0}', '6D', '6D'),
        ('w:tc/w:tcPr/w:shd{w:themeFillShade=F0,w:fill=none}', 'DF', 'DF'),
    ])
    def shd_themeFillShade_set_fixture(self, request):
        cxml, themeFillShade, expected_themeFillShade = request.param
        e = element(cxml)
        if isinstance(e, CT_R):
            obj = Run(e, None)
        elif isinstance(e, CT_P):
            obj = Paragraph(e, None)
        elif isinstance(e, CT_Tc):
            obj = _Cell(e, None)
        else:
            obj = None

        obj.shd_themeFillShade = themeFillShade
        return obj, expected_themeFillShade

    @pytest.fixture(params=[
        ('w:r', None),
        ('w:r/w:rPr', None),
        ('w:r/w:rPr/w:shd{w:val=nil,w:themeShade=AB}', 'AB'),
        ('w:r/w:rPr/w:shd{w:val=nil,w:themeShade=BF}', 'BF'),

        ('w:p', None),
        ('w:p/w:pPr', None),
        ('w:p/w:pPr/w:shd{w:val=nil,w:themeShade=E0}', 'E0'),
        ('w:p/w:pPr/w:shd{w:val=nil,w:themeShade=1F}', '1F'),

        ('w:tc', None),
        ('w:tc/w:tcPr', None),
        ('w:tc/w:tcPr/w:shd{w:val=nil,w:themeShade=A4}', 'A4'),
        ('w:tc/w:tcPr/w:shd{w:val=nil,w:themeShade=F2}', 'F2'),
    ])
    def shd_themeShade_get_fixture(self, request):
        cxml, expected_themeShade = request.param
        e = element(cxml)
        if isinstance(e, CT_R):
            obj = Run(e, None)
        elif isinstance(e, CT_P):
            obj = Paragraph(e, None)
        elif isinstance(e, CT_Tc):
            obj = _Cell(e, None)
        else:
            obj = None
        return obj, expected_themeShade

    @pytest.fixture(params=[
        ('w:r', 'A0', 'A0'),
        ('w:r/w:rPr', 'F1', 'F1'),
        ('w:r/w:rPr/w:shd{w:themeShade=F0}', 'D8', 'D8'),
        ('w:r/w:rPr/w:shd{w:themeShade=F0,w:fill=none}', 'E5', 'E5'),

        ('w:p', '7F', '7F'),
        ('w:p/w:pPr', '2C', '2C'),
        ('w:p/w:pPr/w:shd{w:themeShade=F0}', '0A', '0A'),
        ('w:p/w:pPr/w:shd{w:themeShade=F0,w:fill=none}', '1C', '1C'),

        ('w:tc', 'B2', 'B2'),
        ('w:tc/w:rPr', '2B', '2B'),
        ('w:tc/w:tcPr/w:shd{w:themeShade=F0}', '6D', '6D'),
        ('w:tc/w:tcPr/w:shd{w:themeShade=F0,w:fill=none}', 'DF', 'DF'),
    ])
    def shd_themeShade_set_fixture(self, request):
        cxml, themeShade, expected_themeShade = request.param
        e = element(cxml)
        if isinstance(e, CT_R):
            obj = Run(e, None)
        elif isinstance(e, CT_P):
            obj = Paragraph(e, None)
        elif isinstance(e, CT_Tc):
            obj = _Cell(e, None)
        else:
            obj = None

        obj.shd_themeShade = themeShade
        return obj, expected_themeShade

    @pytest.fixture(params=[
        ('w:r', None),
        ('w:r/w:rPr', None),
        ('w:r/w:rPr/w:shd{w:val=nil,w:themeTint=AB}', 'AB'),
        ('w:r/w:rPr/w:shd{w:val=nil,w:themeTint=BF}', 'BF'),

        ('w:p', None),
        ('w:p/w:pPr', None),
        ('w:p/w:pPr/w:shd{w:val=nil,w:themeTint=E0}', 'E0'),
        ('w:p/w:pPr/w:shd{w:val=nil,w:themeTint=1F}', '1F'),

        ('w:tc', None),
        ('w:tc/w:tcPr', None),
        ('w:tc/w:tcPr/w:shd{w:val=nil,w:themeTint=A4}', 'A4'),
        ('w:tc/w:tcPr/w:shd{w:val=nil,w:themeTint=F2}', 'F2'),
    ])
    def shd_themeTint_get_fixture(self, request):
        cxml, expected_themeTint = request.param
        e = element(cxml)
        if isinstance(e, CT_R):
            obj = Run(e, None)
        elif isinstance(e, CT_P):
            obj = Paragraph(e, None)
        elif isinstance(e, CT_Tc):
            obj = _Cell(e, None)
        else:
            obj = None
        return obj, expected_themeTint

    @pytest.fixture(params=[
        ('w:r', 'A0', 'A0'),
        ('w:r/w:rPr', 'F1', 'F1'),
        ('w:r/w:rPr/w:shd{w:themeTint=F0}', 'D8', 'D8'),
        ('w:r/w:rPr/w:shd{w:themeTint=F0,w:fill=none}', 'E5', 'E5'),

        ('w:p', '7F', '7F'),
        ('w:p/w:pPr', '2C', '2C'),
        ('w:p/w:pPr/w:shd{w:themeTint=F0}', '0A', '0A'),
        ('w:p/w:pPr/w:shd{w:themeTint=F0,w:fill=none}', '1C', '1C'),

        ('w:tc', 'B2', 'B2'),
        ('w:tc/w:rPr', '2B', '2B'),
        ('w:tc/w:tcPr/w:shd{w:themeTint=F0}', '6D', '6D'),
        ('w:tc/w:tcPr/w:shd{w:themeTint=F0,w:fill=none}', 'DF', 'DF'),
    ])
    def shd_themeTint_set_fixture(self, request):
        cxml, themeTint, expected_themeTint = request.param
        e = element(cxml)
        if isinstance(e, CT_R):
            obj = Run(e, None)
        elif isinstance(e, CT_P):
            obj = Paragraph(e, None)
        elif isinstance(e, CT_Tc):
            obj = _Cell(e, None)
        else:
            obj = None

        obj.shd_themeTint = themeTint
        return obj, expected_themeTint

    @pytest.fixture(params=[
        ('w:r', None),
        ('w:r/w:rPr', None),
        ('w:r/w:rPr/w:shd{w:val=nil,w:themeFillTint=AB}', 'AB'),
        ('w:r/w:rPr/w:shd{w:val=nil,w:themeFillTint=BF}', 'BF'),

        ('w:p', None),
        ('w:p/w:pPr', None),
        ('w:p/w:pPr/w:shd{w:val=nil,w:themeFillTint=E0}', 'E0'),
        ('w:p/w:pPr/w:shd{w:val=nil,w:themeFillTint=1F}', '1F'),

        ('w:tc', None),
        ('w:tc/w:tcPr', None),
        ('w:tc/w:tcPr/w:shd{w:val=nil,w:themeFillTint=A4}', 'A4'),
        ('w:tc/w:tcPr/w:shd{w:val=nil,w:themeFillTint=F2}', 'F2'),
    ])
    def shd_themeFillTint_get_fixture(self, request):
        cxml, expected_themeFillTint = request.param
        e = element(cxml)
        if isinstance(e, CT_R):
            obj = Run(e, None)
        elif isinstance(e, CT_P):
            obj = Paragraph(e, None)
        elif isinstance(e, CT_Tc):
            obj = _Cell(e, None)
        else:
            obj = None
        return obj, expected_themeFillTint

    @pytest.fixture(params=[
        ('w:r', 'A0', 'A0'),
        ('w:r/w:rPr', 'F1', 'F1'),
        ('w:r/w:rPr/w:shd{w:themeFillTint=F0}', 'D8', 'D8'),
        ('w:r/w:rPr/w:shd{w:themeFillTint=F0,w:fill=none}', 'E5', 'E5'),

        ('w:p', '7F', '7F'),
        ('w:p/w:pPr', '2C', '2C'),
        ('w:p/w:pPr/w:shd{w:themeFillTint=F0}', '0A', '0A'),
        ('w:p/w:pPr/w:shd{w:themeFillTint=F0,w:fill=none}', '1C', '1C'),

        ('w:tc', 'B2', 'B2'),
        ('w:tc/w:rPr', '2B', '2B'),
        ('w:tc/w:tcPr/w:shd{w:themeFillTint=F0}', '6D', '6D'),
        ('w:tc/w:tcPr/w:shd{w:themeFillTint=F0,w:fill=none}', 'DF', 'DF'),
    ])
    def shd_themeFillTint_set_fixture(self, request):
        cxml, themeFillTint, expected_themeFillTint = request.param
        e = element(cxml)
        if isinstance(e, CT_R):
            obj = Run(e, None)
        elif isinstance(e, CT_P):
            obj = Paragraph(e, None)
        elif isinstance(e, CT_Tc):
            obj = _Cell(e, None)
        else:
            obj = None

        obj.shd_themeFillTint = themeFillTint
        return obj, expected_themeFillTint