# pyright: reportPrivateUsage=false

"""Unit test suite for the docx.opc.rel module."""

import pytest

from docx.opc.oxml import CT_Relationships
from docx.opc.packuri import PackURI
from docx.opc.part import Part
from docx.opc.rel import Relationships, _Relationship

from ..unitutil.mock import Mock, PropertyMock, call, class_mock, instance_mock, patch


class Describe_Relationship:
    def it_remembers_construction_values(self):
        # test data --------------------
        rId = "rId9"
        reltype = "reltype"
        target = Mock(name="target_part")
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
        with pytest.raises(ValueError, match="target_part property on _Relat"):
            rel.target_part

    def it_should_have_target_ref_for_external_rel(self):
        rel = _Relationship(None, None, "target", None, external=True)
        assert rel.target_ref == "target"

    def it_should_have_relative_ref_for_internal_rel(self):
        """
        Internal relationships (TargetMode == 'Internal' in the XML) should
        have a relative ref, e.g. '../slideLayouts/slideLayout1.xml', for
        the target_ref attribute.
        """
        part = Mock(name="part", partname=PackURI("/ppt/media/image1.png"))
        baseURI = "/ppt/slides"
        rel = _Relationship(None, None, part, baseURI)  # external=False
        assert rel.target_ref == "../media/image1.png"


class DescribeRelationships:
    def it_can_add_a_relationship(self, _Relationship_):
        baseURI, rId, reltype, target, external = (
            "baseURI",
            "rId9",
            "reltype",
            "target",
            False,
        )
        rels = Relationships(baseURI)
        rel = rels.add_relationship(reltype, target, rId, external)
        _Relationship_.assert_called_once_with(rId, reltype, target, baseURI, external)
        assert rels[rId] == rel
        assert rel == _Relationship_.return_value

    def it_can_add_an_external_relationship(self, add_ext_rel_fixture_):
        rels, reltype, url = add_ext_rel_fixture_
        rId = rels.get_or_add_ext_rel(reltype, url)
        rel = rels[rId]
        assert rel.is_external
        assert rel.target_ref == url
        assert rel.reltype == reltype

    def it_can_find_a_relationship_by_rId(self):
        rel = Mock(name="rel", rId="foobar")
        rels = Relationships(None)
        rels["foobar"] = rel
        assert rels["foobar"] == rel

    def it_can_find_or_add_a_relationship(
        self, rels_with_matching_rel_, rels_with_missing_rel_
    ):
        rels, reltype, part, matching_rel = rels_with_matching_rel_
        assert rels.get_or_add(reltype, part) == matching_rel

        rels, reltype, part, new_rel = rels_with_missing_rel_
        assert rels.get_or_add(reltype, part) == new_rel

    def it_can_find_or_add_an_external_relationship(
        self, add_matching_ext_rel_fixture_
    ):
        rels, reltype, url, rId = add_matching_ext_rel_fixture_
        _rId = rels.get_or_add_ext_rel(reltype, url)
        assert _rId == rId
        assert len(rels) == 1

    def it_can_find_a_related_part_by_rId(self, rels_with_known_target_part):
        rels, rId, known_target_part = rels_with_known_target_part
        part = rels.related_parts[rId]
        assert part is known_target_part

    def it_raises_on_related_part_not_found(self, rels):
        with pytest.raises(KeyError):
            rels.related_parts["rId666"]

    def it_can_find_a_related_part_by_reltype(self, rels_with_target_known_by_reltype):
        rels, reltype, known_target_part = rels_with_target_known_by_reltype
        part = rels.part_with_reltype(reltype)
        assert part is known_target_part

    def it_can_compose_rels_xml(self, rels, rels_elm):
        # exercise ---------------------
        rels.xml
        # verify -----------------------
        rels_elm.assert_has_calls(
            [
                call.add_rel("rId1", "http://rt-hyperlink", "http://some/link", True),
                call.add_rel("rId2", "http://rt-image", "../media/image1.png", False),
                call.xml(),
            ],
            any_order=True,
        )

    def it_knows_the_next_available_rId_to_help(self, rels_with_rId_gap):
        rels, expected_next_rId = rels_with_rId_gap
        next_rId = rels._next_rId
        assert next_rId == expected_next_rId

    # fixtures ---------------------------------------------

    @pytest.fixture
    def add_ext_rel_fixture_(self, reltype, url):
        rels = Relationships(None)
        return rels, reltype, url

    @pytest.fixture
    def add_matching_ext_rel_fixture_(self, request, reltype, url):
        rId = "rId369"
        rels = Relationships(None)
        rels.add_relationship(reltype, url, rId, is_external=True)
        return rels, reltype, url, rId

    # fixture components -----------------------------------

    @pytest.fixture
    def _baseURI(self):
        return "/baseURI"

    @pytest.fixture
    def _Relationship_(self, request):
        return class_mock(request, "docx.opc.rel._Relationship")

    @pytest.fixture
    def _rel_with_target_known_by_reltype(self, _rId, reltype, _target_part, _baseURI):
        rel = _Relationship(_rId, reltype, _target_part, _baseURI)
        return rel, reltype, _target_part

    @pytest.fixture
    def rels(self):
        """
        Populated Relationships instance that will exercise the rels.xml
        property.
        """
        rels = Relationships("/baseURI")
        rels.add_relationship(
            reltype="http://rt-hyperlink",
            target="http://some/link",
            rId="rId1",
            is_external=True,
        )
        part = Mock(name="part")
        part.partname.relative_ref.return_value = "../media/image1.png"
        rels.add_relationship(reltype="http://rt-image", target=part, rId="rId2")
        return rels

    @pytest.fixture
    def rels_elm(self):
        """
        Return a rels_elm mock that will be returned from
        CT_Relationships.new()
        """
        # create rels_elm mock with a .xml property
        rels_elm = Mock(name="rels_elm")
        xml = PropertyMock(name="xml")
        type(rels_elm).xml = xml
        rels_elm.attach_mock(xml, "xml")
        rels_elm.reset_mock()  # to clear attach_mock call
        # patch CT_Relationships to return that rels_elm
        patch_ = patch.object(CT_Relationships, "new", return_value=rels_elm)
        patch_.start()
        yield rels_elm
        patch_.stop()

    @pytest.fixture
    def _rel_with_known_target_part(self, _rId, reltype, _target_part, _baseURI):
        rel = _Relationship(_rId, reltype, _target_part, _baseURI)
        return rel, _rId, _target_part

    @pytest.fixture
    def rels_with_known_target_part(self, rels, _rel_with_known_target_part):
        rel, rId, target_part = _rel_with_known_target_part
        rels.add_relationship(None, target_part, rId)
        return rels, rId, target_part

    @pytest.fixture
    def rels_with_matching_rel_(self, request, rels):
        matching_reltype_ = instance_mock(request, str, name="matching_reltype_")
        matching_part_ = instance_mock(request, Part, name="matching_part_")
        matching_rel_ = instance_mock(
            request,
            _Relationship,
            name="matching_rel_",
            reltype=matching_reltype_,
            target_part=matching_part_,
            is_external=False,
        )
        rels[1] = matching_rel_
        return rels, matching_reltype_, matching_part_, matching_rel_

    @pytest.fixture
    def rels_with_missing_rel_(self, request, rels, _Relationship_):
        missing_reltype_ = instance_mock(request, str, name="missing_reltype_")
        missing_part_ = instance_mock(request, Part, name="missing_part_")
        new_rel_ = instance_mock(
            request,
            _Relationship,
            name="new_rel_",
            reltype=missing_reltype_,
            target_part=missing_part_,
            is_external=False,
        )
        _Relationship_.return_value = new_rel_
        return rels, missing_reltype_, missing_part_, new_rel_

    @pytest.fixture
    def rels_with_rId_gap(self, request):
        rels = Relationships(None)
        rel_with_rId1 = instance_mock(
            request, _Relationship, name="rel_with_rId1", rId="rId1"
        )
        rel_with_rId3 = instance_mock(
            request, _Relationship, name="rel_with_rId3", rId="rId3"
        )
        rels["rId1"] = rel_with_rId1
        rels["rId3"] = rel_with_rId3
        return rels, "rId2"

    @pytest.fixture
    def rels_with_target_known_by_reltype(
        self, rels, _rel_with_target_known_by_reltype
    ):
        rel, reltype, target_part = _rel_with_target_known_by_reltype
        rels[1] = rel
        return rels, reltype, target_part

    @pytest.fixture
    def reltype(self):
        return "http://rel/type"

    @pytest.fixture
    def _rId(self):
        return "rId6"

    @pytest.fixture
    def _target_part(self, request):
        return instance_mock(request, Part)

    @pytest.fixture
    def url(self):
        return "https://github.com/scanny/python-docx"
