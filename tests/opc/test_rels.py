# encoding: utf-8

"""
Test suite for docx.opc relationships
"""

from __future__ import absolute_import

import pytest

from docx.opc.constants import RELATIONSHIP_TYPE as RT
from docx.opc.package import Part
from docx.opc.rel import _Relationship, Relationships

from ..unitutil.mock import class_mock, instance_mock, loose_mock


class DescribeRelationships(object):

    def it_can_add_a_relationship_if_not_found(
            self, rels_with_matching_rel_, rels_with_missing_rel_):

        rels, reltype, part, matching_rel = rels_with_matching_rel_
        assert rels.get_or_add(reltype, part) == matching_rel

        rels, reltype, part, new_rel = rels_with_missing_rel_
        assert rels.get_or_add(reltype, part) == new_rel

    def it_knows_the_next_available_rId(self, rels_with_rId_gap):
        rels, expected_next_rId = rels_with_rId_gap
        next_rId = rels._next_rId
        assert next_rId == expected_next_rId

    def it_can_find_a_related_part_by_reltype(
            self, rels_with_target_known_by_reltype):
        rels, reltype, known_target_part = rels_with_target_known_by_reltype
        part = rels.part_with_reltype(reltype)
        assert part is known_target_part

    def it_can_find_a_related_part_by_rId(self, rels_with_known_target_part):
        rels, rId, known_target_part = rels_with_known_target_part
        part = rels.related_parts[rId]
        assert part is known_target_part

    def it_raises_KeyError_on_part_with_rId_not_found(self, rels):
        with pytest.raises(KeyError):
            rels.related_parts['rId666']

    # def it_raises_on_add_rel_with_duplicate_rId(self, rels, rel):
    #     with pytest.raises(ValueError):
    #         rels.add_rel(rel)

    # fixtures ---------------------------------------------

    @pytest.fixture
    def _baseURI(self):
        return '/baseURI'

    @pytest.fixture
    def _Relationship_(self, request):
        return class_mock(request, 'docx.opc.rel._Relationship')

    @pytest.fixture
    def rels(self, _baseURI):
        return Relationships(_baseURI)

    @pytest.fixture
    def rels_with_known_target_part(self, rels, _rel_with_known_target_part):
        rel, rId, target_part = _rel_with_known_target_part
        rels.add_relationship(None, target_part, rId)
        return rels, rId, target_part

    @pytest.fixture
    def rels_with_matching_rel_(self, request, rels):
        matching_reltype_ = instance_mock(
            request, str, name='matching_reltype_'
        )
        matching_part_ = instance_mock(
            request, Part, name='matching_part_'
        )
        matching_rel_ = instance_mock(
            request, _Relationship, name='matching_rel_',
            reltype=matching_reltype_, target_part=matching_part_,
            is_external=False
        )
        rels[1] = matching_rel_
        return rels, matching_reltype_, matching_part_, matching_rel_

    @pytest.fixture
    def rels_with_missing_rel_(self, request, rels, _Relationship_):
        missing_reltype_ = instance_mock(
            request, str, name='missing_reltype_'
        )
        missing_part_ = instance_mock(
            request, Part, name='missing_part_'
        )
        new_rel_ = instance_mock(
            request, _Relationship, name='new_rel_',
            reltype=missing_reltype_, target_part=missing_part_,
            is_external=False
        )
        _Relationship_.return_value = new_rel_
        return rels, missing_reltype_, missing_part_, new_rel_

    @pytest.fixture
    def rels_with_rId_gap(self, request, rels):
        rel_with_rId1 = instance_mock(
            request, _Relationship, name='rel_with_rId1', rId='rId1'
        )
        rel_with_rId3 = instance_mock(
            request, _Relationship, name='rel_with_rId3', rId='rId3'
        )
        rels['rId1'] = rel_with_rId1
        rels['rId3'] = rel_with_rId3
        return rels, 'rId2'

    @pytest.fixture
    def rels_with_target_known_by_reltype(
            self, rels, _rel_with_target_known_by_reltype):
        rel, reltype, target_part = _rel_with_target_known_by_reltype
        rels[1] = rel
        return rels, reltype, target_part

    @pytest.fixture
    def _rel_with_known_target_part(
            self, _rId, _reltype, _target_part, _baseURI):
        rel = _Relationship(_rId, _reltype, _target_part, _baseURI)
        return rel, _rId, _target_part

    @pytest.fixture
    def _rel_with_target_known_by_reltype(
            self, _rId, _reltype, _target_part, _baseURI):
        rel = _Relationship(_rId, _reltype, _target_part, _baseURI)
        return rel, _reltype, _target_part

    @pytest.fixture
    def _reltype(self):
        return RT.SLIDE

    @pytest.fixture
    def _rId(self):
        return 'rId6'

    @pytest.fixture
    def _target_part(self, request):
        return loose_mock(request)
