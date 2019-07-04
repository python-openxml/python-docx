# encoding: utf-8

"""Test suite for the docx.oxml.text module"""

from __future__ import absolute_import, division, print_function, unicode_literals

import pytest

from docx.exceptions import InvalidSpanError
from docx.oxml import parse_xml
from docx.oxml.table import CT_Row, CT_Tc

from ..unitutil.cxml import element, xml
from ..unitutil.file import snippet_seq
from ..unitutil.mock import call, instance_mock, method_mock, property_mock


class DescribeCT_Row(object):

    def it_can_add_a_trPr(self, add_trPr_fixture):
        tr, expected_xml = add_trPr_fixture
        tr._add_trPr()
        assert tr.xml == expected_xml

    def it_raises_on_tc_at_grid_col(self, tc_raise_fixture):
        tr, idx = tc_raise_fixture
        with pytest.raises(ValueError):
            tr.tc_at_grid_col(idx)

    # fixtures -------------------------------------------------------

    @pytest.fixture(params=[
        ('w:tr',                    'w:tr/w:trPr'),
        ('w:tr/w:tblPrEx',          'w:tr/(w:tblPrEx,w:trPr)'),
        ('w:tr/w:tc',               'w:tr/(w:trPr,w:tc)'),
        ('w:tr/(w:sdt,w:del,w:tc)', 'w:tr/(w:trPr,w:sdt,w:del,w:tc)'),
    ])
    def add_trPr_fixture(self, request):
        tr_cxml, expected_cxml = request.param
        tr = element(tr_cxml)
        expected_xml = xml(expected_cxml)
        return tr, expected_xml

    @pytest.fixture(params=[(0, 0, 3), (1, 0, 1)])
    def tc_raise_fixture(self, request):
        snippet_idx, row_idx, col_idx = request.param
        tbl = parse_xml(snippet_seq('tbl-cells')[snippet_idx])
        tr = tbl.tr_lst[row_idx]
        return tr, col_idx


class DescribeCT_Tc(object):

    def it_can_merge_to_another_tc(
        self, tr_, _span_dimensions_, _tbl_, _grow_to_, top_tc_
    ):
        top_tr_ = tr_
        tc, other_tc = element('w:tc'), element('w:tc')
        top, left, height, width = 0, 1, 2, 3
        _span_dimensions_.return_value = top, left, height, width
        _tbl_.return_value.tr_lst = [tr_]
        tr_.tc_at_grid_col.return_value = top_tc_

        merged_tc = tc.merge(other_tc)

        _span_dimensions_.assert_called_once_with(tc, other_tc)
        top_tr_.tc_at_grid_col.assert_called_once_with(left)
        top_tc_._grow_to.assert_called_once_with(width, height)
        assert merged_tc is top_tc_

    def it_knows_its_extents_to_help(self, extents_fixture):
        tc, attr_name, expected_value = extents_fixture
        extent = getattr(tc, attr_name)
        assert extent == expected_value

    def it_calculates_the_dimensions_of_a_span_to_help(self, span_fixture):
        tc, other_tc, expected_dimensions = span_fixture
        dimensions = tc._span_dimensions(other_tc)
        assert dimensions == expected_dimensions

    def it_raises_on_invalid_span(self, span_raise_fixture):
        tc, other_tc = span_raise_fixture
        with pytest.raises(InvalidSpanError):
            tc._span_dimensions(other_tc)

    def it_can_grow_itself_to_help_merge(self, grow_to_fixture):
        tc, width, height, top_tc, expected_calls = grow_to_fixture
        tc._grow_to(width, height, top_tc)
        assert tc._span_to_width.call_args_list == expected_calls

    def it_can_extend_its_horz_span_to_help_merge(
        self, top_tc_, grid_span_, _move_content_to_, _swallow_next_tc_
    ):
        grid_span_.side_effect = [1, 3, 4]
        grid_width, vMerge = 4, 'continue'
        tc = element('w:tc')

        tc._span_to_width(grid_width, top_tc_, vMerge)

        _move_content_to_.assert_called_once_with(tc, top_tc_)
        assert _swallow_next_tc_.call_args_list == [
            call(tc, grid_width, top_tc_), call(tc, grid_width, top_tc_)
        ]
        assert tc.vMerge == vMerge

    def it_can_swallow_the_next_tc_help_merge(self, swallow_fixture):
        tc, grid_width, top_tc, tr, expected_xml = swallow_fixture
        tc._swallow_next_tc(grid_width, top_tc)
        assert tr.xml == expected_xml

    def it_adds_cell_widths_on_swallow(self, add_width_fixture):
        tc, grid_width, top_tc, tr, expected_xml = add_width_fixture
        tc._swallow_next_tc(grid_width, top_tc)
        assert tr.xml == expected_xml

    def it_raises_on_invalid_swallow(self, swallow_raise_fixture):
        tc, grid_width, top_tc, tr = swallow_raise_fixture
        with pytest.raises(InvalidSpanError):
            tc._swallow_next_tc(grid_width, top_tc)

    def it_can_move_its_content_to_help_merge(self, move_fixture):
        tc, tc_2, expected_tc_xml, expected_tc_2_xml = move_fixture
        tc._move_content_to(tc_2)
        assert tc.xml == expected_tc_xml
        assert tc_2.xml == expected_tc_2_xml

    def it_raises_on_tr_above(self, tr_above_raise_fixture):
        tc = tr_above_raise_fixture
        with pytest.raises(ValueError):
            tc._tr_above

    # fixtures -------------------------------------------------------

    @pytest.fixture(params=[
        # both cells have a width
        ('w:tr/(w:tc/(w:tcPr/w:tcW{w:w=1440,w:type=dxa},w:p),'
         'w:tc/(w:tcPr/w:tcW{w:w=1440,w:type=dxa},w:p))',      0, 2,
         'w:tr/(w:tc/(w:tcPr/(w:tcW{w:w=2880,w:type=dxa},'
         'w:gridSpan{w:val=2}),w:p))'),
        # neither have a width
        ('w:tr/(w:tc/w:p,w:tc/w:p)',                           0, 2,
         'w:tr/(w:tc/(w:tcPr/w:gridSpan{w:val=2},w:p))'),
        # only second one has a width
        ('w:tr/(w:tc/w:p,'
         'w:tc/(w:tcPr/w:tcW{w:w=1440,w:type=dxa},w:p))',      0, 2,
         'w:tr/(w:tc/(w:tcPr/w:gridSpan{w:val=2},w:p))'),
        # only first one has a width
        ('w:tr/(w:tc/(w:tcPr/w:tcW{w:w=1440,w:type=dxa},w:p),'
         'w:tc/w:p)',                                          0, 2,
         'w:tr/(w:tc/(w:tcPr/(w:tcW{w:w=1440,w:type=dxa},'
         'w:gridSpan{w:val=2}),w:p))'),
    ])
    def add_width_fixture(self, request):
        tr_cxml, tc_idx, grid_width, expected_tr_cxml = request.param
        tr = element(tr_cxml)
        tc = top_tc = tr[tc_idx]
        expected_tr_xml = xml(expected_tr_cxml)
        return tc, grid_width, top_tc, tr, expected_tr_xml

    @pytest.fixture(params=[
        (0, 0, 0, 'top',    0), (2, 0, 1, 'top',    0),
        (2, 1, 1, 'top',    0), (4, 2, 1, 'top',    1),
        (0, 0, 0, 'left',   0), (1, 0, 1, 'left',   2),
        (3, 1, 0, 'left',   0), (3, 1, 1, 'left',   2),
        (0, 0, 0, 'bottom', 1), (1, 0, 0, 'bottom', 1),
        (2, 0, 1, 'bottom', 2), (4, 1, 1, 'bottom', 3),
        (0, 0, 0, 'right',  1), (1, 0, 0, 'right',  2),
        (0, 0, 0, 'right',  1), (4, 2, 1, 'right',  3),
    ])
    def extents_fixture(self, request):
        snippet_idx, row, col, attr_name, expected_value = request.param
        tbl = self._snippet_tbl(snippet_idx)
        tc = tbl.tr_lst[row].tc_lst[col]
        return tc, attr_name, expected_value

    @pytest.fixture(params=[
        (0, 0, 0, 2, 1),
        (0, 0, 1, 1, 2),
        (0, 1, 1, 2, 2),
        (1, 0, 0, 2, 2),
        (2, 0, 0, 2, 2),
        (2, 1, 2, 1, 2),
    ])
    def grow_to_fixture(self, request, _span_to_width_):
        snippet_idx, row, col, width, height = request.param
        tbl = self._snippet_tbl(snippet_idx)
        tc = tbl.tr_lst[row].tc_lst[col]
        start = 0 if height == 1 else 1
        end = start + height
        expected_calls = [
            call(width, tc, None),
            call(width, tc, 'restart'),
            call(width, tc, 'continue'),
            call(width, tc, 'continue'),
        ][start:end]
        return tc, width, height, None, expected_calls

    @pytest.fixture(params=[
        ('w:tc/w:p',             'w:tc/w:p',
         'w:tc/w:p',             'w:tc/w:p'),
        ('w:tc/w:p',             'w:tc/w:p/w:r',
         'w:tc/w:p',             'w:tc/w:p/w:r'),
        ('w:tc/w:p/w:r',         'w:tc/w:p',
         'w:tc/w:p',             'w:tc/w:p/w:r'),
        ('w:tc/(w:p/w:r,w:sdt)', 'w:tc/w:p',
         'w:tc/w:p',             'w:tc/(w:p/w:r,w:sdt)'),
        ('w:tc/(w:p/w:r,w:sdt)', 'w:tc/(w:tbl,w:p)',
         'w:tc/w:p',             'w:tc/(w:tbl,w:p/w:r,w:sdt)'),
    ])
    def move_fixture(self, request):
        tc_cxml, tc_2_cxml, expected_tc_cxml, expected_tc_2_cxml = (
            request.param
        )
        tc, tc_2 = element(tc_cxml), element(tc_2_cxml)
        expected_tc_xml = xml(expected_tc_cxml)
        expected_tc_2_xml = xml(expected_tc_2_cxml)
        return tc, tc_2, expected_tc_xml, expected_tc_2_xml

    @pytest.fixture(params=[
        (0, 0, 0, 0, 1, (0, 0, 1, 2)),
        (0, 0, 1, 2, 1, (0, 1, 3, 1)),
        (0, 2, 2, 1, 1, (1, 1, 2, 2)),
        (0, 1, 2, 1, 0, (1, 0, 1, 3)),
        (1, 0, 0, 1, 1, (0, 0, 2, 2)),
        (1, 0, 1, 0, 0, (0, 0, 1, 3)),
        (2, 0, 1, 2, 1, (0, 1, 3, 1)),
        (2, 0, 1, 1, 0, (0, 0, 2, 2)),
        (2, 1, 2, 0, 1, (0, 1, 2, 2)),
        (4, 0, 1, 0, 0, (0, 0, 1, 3)),
    ])
    def span_fixture(self, request):
        snippet_idx, row, col, row_2, col_2, expected_value = request.param
        tbl = self._snippet_tbl(snippet_idx)
        tc = tbl.tr_lst[row].tc_lst[col]
        tc_2 = tbl.tr_lst[row_2].tc_lst[col_2]
        return tc, tc_2, expected_value

    @pytest.fixture(params=[
        (1, 0, 0, 1, 0),  # inverted-L horz
        (1, 1, 0, 0, 0),  # same in opposite order
        (2, 0, 2, 0, 1),  # inverted-L vert
        (5, 0, 1, 1, 0),  # tee-shape horz bar
        (5, 1, 0, 2, 1),  # same, opposite side
        (6, 1, 0, 0, 1),  # tee-shape vert bar
        (6, 0, 1, 1, 2),  # same, opposite side
    ])
    def span_raise_fixture(self, request):
        snippet_idx, row, col, row_2, col_2 = request.param
        tbl = self._snippet_tbl(snippet_idx)
        tc = tbl.tr_lst[row].tc_lst[col]
        tc_2 = tbl.tr_lst[row_2].tc_lst[col_2]
        return tc, tc_2

    @pytest.fixture(params=[
        ('w:tr/(w:tc/w:p,w:tc/w:p)',                              0, 2,
         'w:tr/(w:tc/(w:tcPr/w:gridSpan{w:val=2},w:p))'),
        ('w:tr/(w:tc/w:p,w:tc/w:p,w:tc/w:p)',                     1, 2,
         'w:tr/(w:tc/w:p,w:tc/(w:tcPr/w:gridSpan{w:val=2},w:p))'),
        ('w:tr/(w:tc/w:p/w:r/w:t"a",w:tc/w:p/w:r/w:t"b")',        0, 2,
         'w:tr/(w:tc/(w:tcPr/w:gridSpan{w:val=2},w:p/w:r/w:t"a",'
         'w:p/w:r/w:t"b"))'),
        ('w:tr/(w:tc/(w:tcPr/w:gridSpan{w:val=2},w:p),w:tc/w:p)', 0, 3,
         'w:tr/(w:tc/(w:tcPr/w:gridSpan{w:val=3},w:p))'),
        ('w:tr/(w:tc/w:p,w:tc/(w:tcPr/w:gridSpan{w:val=2},w:p))', 0, 3,
         'w:tr/(w:tc/(w:tcPr/w:gridSpan{w:val=3},w:p))'),
    ])
    def swallow_fixture(self, request):
        tr_cxml, tc_idx, grid_width, expected_tr_cxml = request.param
        tr = element(tr_cxml)
        tc = top_tc = tr[tc_idx]
        expected_tr_xml = xml(expected_tr_cxml)
        return tc, grid_width, top_tc, tr, expected_tr_xml

    @pytest.fixture(params=[
        ('w:tr/w:tc/w:p', 0, 2),
        ('w:tr/(w:tc/w:p,w:tc/(w:tcPr/w:gridSpan{w:val=2},w:p))', 0, 2),
    ])
    def swallow_raise_fixture(self, request):
        tr_cxml, tc_idx, grid_width = request.param
        tr = element(tr_cxml)
        tc = top_tc = tr[tc_idx]
        return tc, grid_width, top_tc, tr

    @pytest.fixture(params=[(0, 0, 0), (4, 0, 0)])
    def tr_above_raise_fixture(self, request):
        snippet_idx, row_idx, col_idx = request.param
        tbl = parse_xml(snippet_seq('tbl-cells')[snippet_idx])
        tc = tbl.tr_lst[row_idx].tc_lst[col_idx]
        return tc

    # fixture components ---------------------------------------------

    @pytest.fixture
    def grid_span_(self, request):
        return property_mock(request, CT_Tc, 'grid_span')

    @pytest.fixture
    def _grow_to_(self, request):
        return method_mock(request, CT_Tc, '_grow_to')

    @pytest.fixture
    def _move_content_to_(self, request):
        return method_mock(request, CT_Tc, '_move_content_to')

    @pytest.fixture
    def _span_dimensions_(self, request):
        return method_mock(request, CT_Tc, '_span_dimensions')

    @pytest.fixture
    def _span_to_width_(self, request):
        return method_mock(request, CT_Tc, '_span_to_width', autospec=False)

    def _snippet_tbl(self, idx):
        """
        Return a <w:tbl> element for snippet at *idx* in 'tbl-cells' snippet
        file.
        """
        return parse_xml(snippet_seq('tbl-cells')[idx])

    @pytest.fixture
    def _swallow_next_tc_(self, request):
        return method_mock(request, CT_Tc, '_swallow_next_tc')

    @pytest.fixture
    def _tbl_(self, request):
        return property_mock(request, CT_Tc, '_tbl')

    @pytest.fixture
    def top_tc_(self, request):
        return instance_mock(request, CT_Tc)

    @pytest.fixture
    def tr_(self, request):
        return instance_mock(request, CT_Row)
