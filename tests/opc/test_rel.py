# encoding: utf-8

"""
Unit test suite for the docx.opc.rel module
"""

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

import pytest

from docx.opc.oxml import CT_Relationships
from docx.opc.packuri import PackURI
from docx.opc.rel import _Relationship, Relationships

from ..unitutil.mock import call, class_mock, Mock, patch, PropertyMock


class Describe_Relationship(object):

    def it_remembers_construction_values(self):
        # test data --------------------
        rId = 'rId9'
        reltype = 'reltype'
        target = Mock(name='target_part')
        external = False
        # exercise ---------------------
        rel = _Relationship(rId, reltype, target, None, external)
        # verify -----------------------
        assert rel.rId == rId
        assert rel.reltype == reltype
        assert rel.target_part == target
        assert rel.is_external == external

    def it_should_raise_on_target_part_access_on_external_rel(self):
        rel = _Relationship(None, None, None, None, external=True)
        with pytest.raises(ValueError):
            rel.target_part

    def it_should_have_target_ref_for_external_rel(self):
        rel = _Relationship(None, None, 'target', None, external=True)
        assert rel.target_ref == 'target'

    def it_should_have_relative_ref_for_internal_rel(self):
        """
        Internal relationships (TargetMode == 'Internal' in the XML) should
        have a relative ref, e.g. '../slideLayouts/slideLayout1.xml', for
        the target_ref attribute.
        """
        part = Mock(name='part', partname=PackURI('/ppt/media/image1.png'))
        baseURI = '/ppt/slides'
        rel = _Relationship(None, None, part, baseURI)  # external=False
        assert rel.target_ref == '../media/image1.png'


class DescribeRelationships(object):

    def it_has_a_len(self):
        rels = Relationships(None)
        assert len(rels) == 0

    def it_has_dict_style_lookup_of_rel_by_rId(self):
        rel = Mock(name='rel', rId='foobar')
        rels = Relationships(None)
        rels['foobar'] = rel
        assert rels['foobar'] == rel

    def it_should_raise_on_failed_lookup_by_rId(self):
        rels = Relationships(None)
        with pytest.raises(KeyError):
            rels['barfoo']

    def it_can_add_a_relationship(self, _Relationship_):
        baseURI, rId, reltype, target, external = (
            'baseURI', 'rId9', 'reltype', 'target', False
        )
        rels = Relationships(baseURI)
        rel = rels.add_relationship(reltype, target, rId, external)
        _Relationship_.assert_called_once_with(
            rId, reltype, target, baseURI, external
        )
        assert rels[rId] == rel
        assert rel == _Relationship_.return_value

    def it_can_add_an_external_relationship(self, add_ext_rel_fixture_):
        rels, reltype, url = add_ext_rel_fixture_
        rId = rels.get_or_add_ext_rel(reltype, url)
        rel = rels[rId]
        assert rel.is_external
        assert rel.target_ref == url
        assert rel.reltype == reltype

    def it_should_return_an_existing_one_if_it_matches(
            self, add_matching_ext_rel_fixture_):
        rels, reltype, url, rId = add_matching_ext_rel_fixture_
        _rId = rels.get_or_add_ext_rel(reltype, url)
        assert _rId == rId
        assert len(rels) == 1

    def it_can_compose_rels_xml(self, rels, rels_elm):
        # exercise ---------------------
        rels.xml
        # verify -----------------------
        rels_elm.assert_has_calls(
            [
                call.add_rel(
                    'rId1', 'http://rt-hyperlink', 'http://some/link', True
                ),
                call.add_rel(
                    'rId2', 'http://rt-image', '../media/image1.png', False
                ),
                call.xml()
            ],
            any_order=True
        )

    # fixtures ---------------------------------------------

    @pytest.fixture
    def add_ext_rel_fixture_(self, reltype, url):
        rels = Relationships(None)
        return rels, reltype, url

    @pytest.fixture
    def add_matching_ext_rel_fixture_(self, request, reltype, url):
        rId = 'rId369'
        rels = Relationships(None)
        rels.add_relationship(reltype, url, rId, is_external=True)
        return rels, reltype, url, rId

    @pytest.fixture
    def _Relationship_(self, request):
        return class_mock(request, 'docx.opc.rel._Relationship')

    @pytest.fixture
    def rels(self):
        """
        Populated Relationships instance that will exercise the rels.xml
        property.
        """
        rels = Relationships('/baseURI')
        rels.add_relationship(
            reltype='http://rt-hyperlink', target='http://some/link',
            rId='rId1', is_external=True
        )
        part = Mock(name='part')
        part.partname.relative_ref.return_value = '../media/image1.png'
        rels.add_relationship(reltype='http://rt-image', target=part,
                              rId='rId2')
        return rels

    @pytest.fixture
    def rels_elm(self, request):
        """
        Return a rels_elm mock that will be returned from
        CT_Relationships.new()
        """
        # create rels_elm mock with a .xml property
        rels_elm = Mock(name='rels_elm')
        xml = PropertyMock(name='xml')
        type(rels_elm).xml = xml
        rels_elm.attach_mock(xml, 'xml')
        rels_elm.reset_mock()  # to clear attach_mock call
        # patch CT_Relationships to return that rels_elm
        patch_ = patch.object(CT_Relationships, 'new', return_value=rels_elm)
        patch_.start()
        request.addfinalizer(patch_.stop)
        return rels_elm

    @pytest.fixture
    def reltype(self):
        return 'http://rel/type'

    @pytest.fixture
    def url(self):
        return 'https://github.com/scanny/python-docx'
