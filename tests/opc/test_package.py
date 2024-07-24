# pyright: reportPrivateUsage=false

"""Unit test suite for docx.opc.package module"""

from __future__ import annotations

import pytest

from docx.opc.constants import RELATIONSHIP_TYPE as RT
from docx.opc.coreprops import CoreProperties
from docx.opc.package import OpcPackage, Unmarshaller
from docx.opc.packuri import PACKAGE_URI, PackURI
from docx.opc.part import Part
from docx.opc.parts.coreprops import CorePropertiesPart
from docx.opc.pkgreader import PackageReader
from docx.opc.rel import Relationships, _Relationship

from ..unitutil.mock import (
    FixtureRequest,
    Mock,
    call,
    class_mock,
    instance_mock,
    loose_mock,
    method_mock,
    patch,
    property_mock,
)


class DescribeOpcPackage:
    """Unit-test suite for `docx.opc.package.OpcPackage` objects."""

    def it_can_open_a_pkg_file(self, PackageReader_, PartFactory_, Unmarshaller_):
        # mockery ----------------------
        pkg_file = Mock(name="pkg_file")
        pkg_reader = PackageReader_.from_file.return_value
        # exercise ---------------------
        pkg = OpcPackage.open(pkg_file)
        # verify -----------------------
        PackageReader_.from_file.assert_called_once_with(pkg_file)
        Unmarshaller_.unmarshal.assert_called_once_with(pkg_reader, pkg, PartFactory_)
        assert isinstance(pkg, OpcPackage)

    def it_initializes_its_rels_collection_on_first_reference(self, Relationships_):
        pkg = OpcPackage()
        rels = pkg.rels
        Relationships_.assert_called_once_with(PACKAGE_URI.baseURI)
        assert rels == Relationships_.return_value

    def it_can_add_a_relationship_to_a_part(self, rels_prop_: Mock, rels_: Mock, part_: Mock):
        rels_prop_.return_value = rels_
        pkg = OpcPackage()

        pkg.load_rel("http://rel/type", part_, "rId99")

        rels_.add_relationship.assert_called_once_with("http://rel/type", part_, "rId99", False)

    def it_can_establish_a_relationship_to_another_part(
        self, rels_prop_: Mock, rels_: Mock, rel_: Mock, part_: Mock
    ):
        rel_.rId = "rId99"
        rels_.get_or_add.return_value = rel_
        rels_prop_.return_value = rels_
        pkg = OpcPackage()

        rId = pkg.relate_to(part_, "http://rel/type")

        rels_.get_or_add.assert_called_once_with("http://rel/type", part_)
        assert rId == "rId99"

    def it_can_provide_a_list_of_the_parts_it_contains(self):
        # mockery ----------------------
        parts = [Mock(name="part1"), Mock(name="part2")]
        pkg = OpcPackage()
        # verify -----------------------
        with patch.object(OpcPackage, "iter_parts", return_value=parts):
            assert pkg.parts == [parts[0], parts[1]]

    def it_can_iterate_over_parts_by_walking_rels_graph(self, rels_prop_: Mock):
        # +----------+       +--------+
        # | pkg_rels |-----> | part_1 |
        # +----------+       +--------+
        #      |               |    ^
        #      v               v    |
        #   external         +--------+
        #                    | part_2 |
        #                    +--------+
        part1, part2 = (Mock(name="part1"), Mock(name="part2"))
        part1.rels = {1: Mock(name="rel1", is_external=False, target_part=part2)}
        part2.rels = {1: Mock(name="rel2", is_external=False, target_part=part1)}
        pkg = OpcPackage()
        rels_prop_.return_value = {
            1: Mock(name="rel3", is_external=False, target_part=part1),
            2: Mock(name="rel4", is_external=True),
        }
        # verify -----------------------
        assert part1 in pkg.iter_parts()
        assert part2 in pkg.iter_parts()
        assert len(list(pkg.iter_parts())) == 2

    def it_can_find_the_next_available_vector_partname(
        self, next_partname_fixture, iter_parts_, PackURI_, packuri_
    ):
        """A vector partname is one with a numeric suffix, like header42.xml."""
        parts_, expected_value = next_partname_fixture
        iter_parts_.return_value = iter(parts_)
        PackURI_.return_value = packuri_
        package = OpcPackage()

        partname = package.next_partname(template="/foo/bar/baz%d.xml")

        PackURI_.assert_called_once_with(expected_value)
        assert partname is packuri_

    def it_can_find_a_part_related_by_reltype(self, related_part_fixture_):
        pkg, reltype, related_part_ = related_part_fixture_
        related_part = pkg.part_related_by(reltype)
        pkg.rels.part_with_reltype.assert_called_once_with(reltype)
        assert related_part is related_part_

    def it_can_save_to_a_pkg_file(
        self, pkg_file_: Mock, PackageWriter_: Mock, parts_prop_: Mock, parts_: list[Mock]
    ):
        parts_prop_.return_value = parts_
        pkg = OpcPackage()
        pkg.save(pkg_file_)
        for part in parts_:
            part.before_marshal.assert_called_once_with()
        PackageWriter_.write.assert_called_once_with(pkg_file_, pkg.rels, parts_)

    def it_provides_access_to_the_core_properties(self, core_props_fixture):
        opc_package, core_properties_ = core_props_fixture
        core_properties = opc_package.core_properties
        assert core_properties is core_properties_

    def it_provides_access_to_the_core_properties_part_to_help(self, core_props_part_fixture):
        opc_package, core_properties_part_ = core_props_part_fixture
        core_properties_part = opc_package._core_properties_part
        assert core_properties_part is core_properties_part_

    def it_creates_a_default_core_props_part_if_none_present(
        self, part_related_by_, CorePropertiesPart_, relate_to_, core_properties_part_
    ):
        part_related_by_.side_effect = KeyError
        CorePropertiesPart_.default.return_value = core_properties_part_
        opc_package = OpcPackage()

        core_properties_part = opc_package._core_properties_part

        CorePropertiesPart_.default.assert_called_once_with(opc_package)
        relate_to_.assert_called_once_with(opc_package, core_properties_part_, RT.CORE_PROPERTIES)
        assert core_properties_part is core_properties_part_

    # fixtures ---------------------------------------------

    @pytest.fixture
    def core_props_fixture(
        self, _core_properties_part_prop_, core_properties_part_, core_properties_
    ):
        opc_package = OpcPackage()
        _core_properties_part_prop_.return_value = core_properties_part_
        core_properties_part_.core_properties = core_properties_
        return opc_package, core_properties_

    @pytest.fixture
    def core_props_part_fixture(self, part_related_by_, core_properties_part_):
        opc_package = OpcPackage()
        part_related_by_.return_value = core_properties_part_
        return opc_package, core_properties_part_

    @pytest.fixture(params=[((), 1), ((1,), 2), ((1, 2), 3), ((2, 3), 1), ((1, 3), 2)])
    def next_partname_fixture(self, request, iter_parts_):
        existing_partname_ns, next_partname_n = request.param
        parts_ = [
            instance_mock(request, Part, name="part[%d]" % idx, partname="/foo/bar/baz%d.xml" % n)
            for idx, n in enumerate(existing_partname_ns)
        ]
        expected_value = "/foo/bar/baz%d.xml" % next_partname_n
        return parts_, expected_value

    @pytest.fixture
    def related_part_fixture_(self, request: FixtureRequest, rels_prop_: Mock, rels_: Mock):
        related_part_ = instance_mock(request, Part, name="related_part_")
        rels_.part_with_reltype.return_value = related_part_
        pkg = OpcPackage()
        rels_prop_.return_value = rels_
        return pkg, "http://rel/type", related_part_

    # fixture components -----------------------------------

    @pytest.fixture
    def CorePropertiesPart_(self, request: FixtureRequest):
        return class_mock(request, "docx.opc.package.CorePropertiesPart")

    @pytest.fixture
    def core_properties_(self, request: FixtureRequest):
        return instance_mock(request, CoreProperties)

    @pytest.fixture
    def core_properties_part_(self, request: FixtureRequest):
        return instance_mock(request, CorePropertiesPart)

    @pytest.fixture
    def _core_properties_part_prop_(self, request: FixtureRequest):
        return property_mock(request, OpcPackage, "_core_properties_part")

    @pytest.fixture
    def iter_parts_(self, request: FixtureRequest):
        return method_mock(request, OpcPackage, "iter_parts")

    @pytest.fixture
    def PackageReader_(self, request: FixtureRequest):
        return class_mock(request, "docx.opc.package.PackageReader")

    @pytest.fixture
    def PackURI_(self, request: FixtureRequest):
        return class_mock(request, "docx.opc.package.PackURI")

    @pytest.fixture
    def packuri_(self, request: FixtureRequest):
        return instance_mock(request, PackURI)

    @pytest.fixture
    def PackageWriter_(self, request: FixtureRequest):
        return class_mock(request, "docx.opc.package.PackageWriter")

    @pytest.fixture
    def PartFactory_(self, request: FixtureRequest):
        return class_mock(request, "docx.opc.package.PartFactory")

    @pytest.fixture
    def part_(self, request: FixtureRequest):
        return instance_mock(request, Part)

    @pytest.fixture
    def part_related_by_(self, request: FixtureRequest):
        return method_mock(request, OpcPackage, "part_related_by")

    @pytest.fixture
    def parts_(self, request: FixtureRequest):
        part_ = instance_mock(request, Part, name="part_")
        part_2_ = instance_mock(request, Part, name="part_2_")
        return [part_, part_2_]

    @pytest.fixture
    def parts_prop_(self, request: FixtureRequest):
        return property_mock(request, OpcPackage, "parts")

    @pytest.fixture
    def pkg_file_(self, request: FixtureRequest):
        return loose_mock(request)

    @pytest.fixture
    def Relationships_(self, request: FixtureRequest):
        return class_mock(request, "docx.opc.package.Relationships")

    @pytest.fixture
    def rel_(self, request: FixtureRequest):
        return instance_mock(request, _Relationship)

    @pytest.fixture
    def relate_to_(self, request: FixtureRequest):
        return method_mock(request, OpcPackage, "relate_to")

    @pytest.fixture
    def rels_(self, request: FixtureRequest):
        return instance_mock(request, Relationships)

    @pytest.fixture
    def rels_prop_(self, request: FixtureRequest):
        return property_mock(request, OpcPackage, "rels")

    @pytest.fixture
    def Unmarshaller_(self, request: FixtureRequest):
        return class_mock(request, "docx.opc.package.Unmarshaller")


class DescribeUnmarshaller:
    def it_can_unmarshal_from_a_pkg_reader(
        self,
        pkg_reader_,
        pkg_,
        part_factory_,
        _unmarshal_parts_,
        _unmarshal_relationships_,
        parts_dict_,
    ):
        _unmarshal_parts_.return_value = parts_dict_
        Unmarshaller.unmarshal(pkg_reader_, pkg_, part_factory_)

        _unmarshal_parts_.assert_called_once_with(pkg_reader_, pkg_, part_factory_)
        _unmarshal_relationships_.assert_called_once_with(pkg_reader_, pkg_, parts_dict_)
        for part in parts_dict_.values():
            part.after_unmarshal.assert_called_once_with()
        pkg_.after_unmarshal.assert_called_once_with()

    def it_can_unmarshal_parts(
        self,
        pkg_reader_,
        pkg_,
        part_factory_,
        parts_dict_,
        partnames_,
        content_types_,
        reltypes_,
        blobs_,
    ):
        # fixture ----------------------
        partname_, partname_2_ = partnames_
        content_type_, content_type_2_ = content_types_
        reltype_, reltype_2_ = reltypes_
        blob_, blob_2_ = blobs_
        # exercise ---------------------
        parts = Unmarshaller._unmarshal_parts(pkg_reader_, pkg_, part_factory_)
        # verify -----------------------
        assert part_factory_.call_args_list == [
            call(partname_, content_type_, reltype_, blob_, pkg_),
            call(partname_2_, content_type_2_, reltype_2_, blob_2_, pkg_),
        ]
        assert parts == parts_dict_

    def it_can_unmarshal_relationships(self):
        # test data --------------------
        reltype = "http://reltype"
        # mockery ----------------------
        pkg_reader = Mock(name="pkg_reader")
        pkg_reader.iter_srels.return_value = (
            (
                "/",
                Mock(
                    name="srel1",
                    rId="rId1",
                    reltype=reltype,
                    target_partname="partname1",
                    is_external=False,
                ),
            ),
            (
                "/",
                Mock(
                    name="srel2",
                    rId="rId2",
                    reltype=reltype,
                    target_ref="target_ref_1",
                    is_external=True,
                ),
            ),
            (
                "partname1",
                Mock(
                    name="srel3",
                    rId="rId3",
                    reltype=reltype,
                    target_partname="partname2",
                    is_external=False,
                ),
            ),
            (
                "partname2",
                Mock(
                    name="srel4",
                    rId="rId4",
                    reltype=reltype,
                    target_ref="target_ref_2",
                    is_external=True,
                ),
            ),
        )
        pkg = Mock(name="pkg")
        parts = {}
        for num in range(1, 3):
            name = "part%d" % num
            part = Mock(name=name)
            parts["partname%d" % num] = part
            pkg.attach_mock(part, name)
        # exercise ---------------------
        Unmarshaller._unmarshal_relationships(pkg_reader, pkg, parts)
        # verify -----------------------
        expected_pkg_calls = [
            call.load_rel(reltype, parts["partname1"], "rId1", False),
            call.load_rel(reltype, "target_ref_1", "rId2", True),
            call.part1.load_rel(reltype, parts["partname2"], "rId3", False),
            call.part2.load_rel(reltype, "target_ref_2", "rId4", True),
        ]
        assert pkg.mock_calls == expected_pkg_calls

    # fixtures ---------------------------------------------

    @pytest.fixture
    def blobs_(self, request: FixtureRequest):
        blob_ = loose_mock(request, spec=str, name="blob_")
        blob_2_ = loose_mock(request, spec=str, name="blob_2_")
        return blob_, blob_2_

    @pytest.fixture
    def content_types_(self, request: FixtureRequest):
        content_type_ = loose_mock(request, spec=str, name="content_type_")
        content_type_2_ = loose_mock(request, spec=str, name="content_type_2_")
        return content_type_, content_type_2_

    @pytest.fixture
    def part_factory_(self, request, parts_):
        part_factory_ = loose_mock(request, spec=Part)
        part_factory_.side_effect = parts_
        return part_factory_

    @pytest.fixture
    def partnames_(self, request: FixtureRequest):
        partname_ = loose_mock(request, spec=str, name="partname_")
        partname_2_ = loose_mock(request, spec=str, name="partname_2_")
        return partname_, partname_2_

    @pytest.fixture
    def parts_(self, request: FixtureRequest):
        part_ = instance_mock(request, Part, name="part_")
        part_2_ = instance_mock(request, Part, name="part_2")
        return part_, part_2_

    @pytest.fixture
    def parts_dict_(self, request, partnames_, parts_):
        partname_, partname_2_ = partnames_
        part_, part_2_ = parts_
        return {partname_: part_, partname_2_: part_2_}

    @pytest.fixture
    def pkg_(self, request: FixtureRequest):
        return instance_mock(request, OpcPackage)

    @pytest.fixture
    def pkg_reader_(self, request, partnames_, content_types_, reltypes_, blobs_):
        partname_, partname_2_ = partnames_
        content_type_, content_type_2_ = content_types_
        reltype_, reltype_2_ = reltypes_
        blob_, blob_2_ = blobs_
        iter_spart_items = (
            (partname_, content_type_, reltype_, blob_),
            (partname_2_, content_type_2_, reltype_2_, blob_2_),
        )
        pkg_reader_ = instance_mock(request, PackageReader)
        pkg_reader_.iter_sparts.return_value = iter_spart_items
        return pkg_reader_

    @pytest.fixture
    def reltypes_(self, request: FixtureRequest):
        reltype_ = instance_mock(request, str, name="reltype_")
        reltype_2_ = instance_mock(request, str, name="reltype_2")
        return reltype_, reltype_2_

    @pytest.fixture
    def _unmarshal_parts_(self, request: FixtureRequest):
        return method_mock(request, Unmarshaller, "_unmarshal_parts", autospec=False)

    @pytest.fixture
    def _unmarshal_relationships_(self, request: FixtureRequest):
        return method_mock(request, Unmarshaller, "_unmarshal_relationships", autospec=False)
