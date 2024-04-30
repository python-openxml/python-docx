# pyright: reportPrivateUsage=false

"""Unit test suite for docx.opc.part module"""

from __future__ import annotations

import pytest

from docx.opc.package import OpcPackage
from docx.opc.packuri import PackURI
from docx.opc.part import Part, PartFactory, XmlPart
from docx.opc.rel import Relationships, _Relationship
from docx.oxml.xmlchemy import BaseOxmlElement

from ..unitutil.cxml import element
from ..unitutil.mock import (
    ANY,
    FixtureRequest,
    Mock,
    class_mock,
    cls_attr_mock,
    function_mock,
    initializer_mock,
    instance_mock,
    loose_mock,
    property_mock,
)


class DescribePart:
    """Unit-test suite for `docx.opc.part.Part` objects."""

    def it_can_be_constructed_by_PartFactory(self, package_: Mock, init__: Mock):
        part = Part.load(PackURI("/part/name"), "content/type", b"1be2", package_)

        init__.assert_called_once_with(ANY, "/part/name", "content/type", b"1be2", package_)
        assert isinstance(part, Part)

    def it_knows_its_partname(self):
        part = Part(PackURI("/part/name"), "content/type")
        assert part.partname == "/part/name"

    def it_can_change_its_partname(self):
        part = Part(PackURI("/old/part/name"), "content/type")
        part.partname = PackURI("/new/part/name")
        assert part.partname == "/new/part/name"

    def it_knows_its_content_type(self):
        part = Part(PackURI("/part/name"), "content/type")
        assert part.content_type == "content/type"

    def it_knows_the_package_it_belongs_to(self, package_: Mock):
        part = Part(PackURI("/part/name"), "content/type", package=package_)
        assert part.package is package_

    def it_can_be_notified_after_unmarshalling_is_complete(self):
        part = Part(PackURI("/part/name"), "content/type")
        part.after_unmarshal()

    def it_can_be_notified_before_marshalling_is_started(self):
        part = Part(PackURI("/part/name"), "content/type")
        part.before_marshal()

    def it_uses_the_load_blob_as_its_blob(self):
        blob = b"abcde"
        part = Part(PackURI("/part/name"), "content/type", blob)
        assert part.blob is blob

    # fixtures ---------------------------------------------

    @pytest.fixture
    def init__(self, request: FixtureRequest):
        return initializer_mock(request, Part)

    @pytest.fixture
    def package_(self, request: FixtureRequest):
        return instance_mock(request, OpcPackage)


class DescribePartRelationshipManagementInterface:
    """Unit-test suite for `docx.opc.package.Part` relationship behaviors."""

    def it_provides_access_to_its_relationships(
        self, Relationships_: Mock, partname_: Mock, rels_: Mock
    ):
        Relationships_.return_value = rels_
        part = Part(partname_, "content_type")

        rels = part.rels

        Relationships_.assert_called_once_with(partname_.baseURI)
        assert rels is rels_

    def it_can_load_a_relationship(self, rels_prop_: Mock, rels_: Mock, other_part_: Mock):
        rels_prop_.return_value = rels_
        part = Part("partname", "content_type")

        part.load_rel("http://rel/type", other_part_, "rId42")

        rels_.add_relationship.assert_called_once_with(
            "http://rel/type", other_part_, "rId42", False
        )

    def it_can_establish_a_relationship_to_another_part(
        self, rels_prop_: Mock, rels_: Mock, rel_: Mock, other_part_: Mock
    ):
        rels_prop_.return_value = rels_
        rels_.get_or_add.return_value = rel_
        rel_.rId = "rId18"
        part = Part("partname", "content_type")

        rId = part.relate_to(other_part_, "http://rel/type")

        rels_.get_or_add.assert_called_once_with("http://rel/type", other_part_)
        assert rId == "rId18"

    def it_can_establish_an_external_relationship(self, rels_prop_: Mock, rels_: Mock):
        rels_prop_.return_value = rels_
        rels_.get_or_add_ext_rel.return_value = "rId27"
        part = Part("partname", "content_type")

        rId = part.relate_to("https://hyper/link", "http://rel/type", is_external=True)

        rels_.get_or_add_ext_rel.assert_called_once_with("http://rel/type", "https://hyper/link")
        assert rId == "rId27"

    def it_can_drop_a_relationship(self, rels_prop_: Mock):
        rels_prop_.return_value = {"rId42": None}
        part = Part(PackURI("/partname"), "content_type")

        part.drop_rel("rId42")

        assert "rId42" not in part.rels

    def it_can_find_a_related_part_by_reltype(
        self, rels_prop_: Mock, rels_: Mock, other_part_: Mock
    ):
        rels_prop_.return_value = rels_
        rels_.part_with_reltype.return_value = other_part_
        part = Part("partname", "content_type")

        related_part = part.part_related_by("http://rel/type")

        rels_.part_with_reltype.assert_called_once_with("http://rel/type")
        assert related_part is other_part_

    def it_can_find_a_related_part_by_rId(self, rels_prop_: Mock, rels_: Mock, other_part_: Mock):
        rels_prop_.return_value = rels_
        rels_.related_parts = {"rId24": other_part_}
        part = Part("partname", "content_type")

        assert part.related_parts["rId24"] is other_part_

    def it_can_find_the_uri_of_an_external_relationship(
        self, rels_prop_: Mock, rel_: Mock, other_part_: Mock
    ):
        rels_prop_.return_value = {"rId7": rel_}
        rel_.target_ref = "https://hyper/link"
        part = Part("partname", "content_type")

        url = part.target_ref("rId7")

        assert url == "https://hyper/link"

    # fixtures ---------------------------------------------

    @pytest.fixture
    def other_part_(self, request: FixtureRequest):
        return instance_mock(request, Part)

    @pytest.fixture
    def partname_(self, request: FixtureRequest):
        return instance_mock(request, PackURI)

    @pytest.fixture
    def Relationships_(self, request: FixtureRequest):
        return class_mock(request, "docx.opc.part.Relationships")

    @pytest.fixture
    def rel_(self, request: FixtureRequest):
        return instance_mock(request, _Relationship)

    @pytest.fixture
    def rels_(self, request: FixtureRequest):
        return instance_mock(request, Relationships)

    @pytest.fixture
    def rels_prop_(self, request: FixtureRequest):
        return property_mock(request, Part, "rels")


class DescribePartFactory:
    def it_constructs_part_from_selector_if_defined(self, cls_selector_fixture):
        # fixture ----------------------
        (
            cls_selector_fn_,
            part_load_params,
            CustomPartClass_,
            part_of_custom_type_,
        ) = cls_selector_fixture
        partname, content_type, reltype, blob, package = part_load_params
        # exercise ---------------------
        PartFactory.part_class_selector = cls_selector_fn_
        part = PartFactory(partname, content_type, reltype, blob, package)
        # verify -----------------------
        cls_selector_fn_.assert_called_once_with(content_type, reltype)
        CustomPartClass_.load.assert_called_once_with(partname, content_type, blob, package)
        assert part is part_of_custom_type_

    def it_constructs_custom_part_type_for_registered_content_types(
        self, part_args_, CustomPartClass_, part_of_custom_type_
    ):
        # fixture ----------------------
        partname, content_type, reltype, package, blob = part_args_
        # exercise ---------------------
        PartFactory.part_type_for[content_type] = CustomPartClass_
        part = PartFactory(partname, content_type, reltype, blob, package)
        # verify -----------------------
        CustomPartClass_.load.assert_called_once_with(partname, content_type, blob, package)
        assert part is part_of_custom_type_

    def it_constructs_part_using_default_class_when_no_custom_registered(
        self, part_args_2_, DefaultPartClass_, part_of_default_type_
    ):
        partname, content_type, reltype, blob, package = part_args_2_
        part = PartFactory(partname, content_type, reltype, blob, package)
        DefaultPartClass_.load.assert_called_once_with(partname, content_type, blob, package)
        assert part is part_of_default_type_

    # fixtures ---------------------------------------------

    @pytest.fixture
    def blob_(self, request):
        return instance_mock(request, str)

    @pytest.fixture
    def blob_2_(self, request):
        return instance_mock(request, str)

    @pytest.fixture
    def cls_method_fn_(self, request, cls_selector_fn_):
        return function_mock(request, "docx.opc.part.cls_method_fn", return_value=cls_selector_fn_)

    @pytest.fixture
    def cls_selector_fixture(
        self,
        cls_selector_fn_,
        cls_method_fn_,
        part_load_params,
        CustomPartClass_,
        part_of_custom_type_,
    ):
        original_part_class_selector = PartFactory.part_class_selector
        yield (
            cls_selector_fn_,
            part_load_params,
            CustomPartClass_,
            part_of_custom_type_,
        )
        PartFactory.part_class_selector = original_part_class_selector

    @pytest.fixture
    def cls_selector_fn_(self, request, CustomPartClass_):
        cls_selector_fn_ = loose_mock(request)
        # Python 3 version
        cls_selector_fn_.return_value = CustomPartClass_
        # Python 2 version
        cls_selector_fn_.__func__ = loose_mock(
            request, name="__func__", return_value=cls_selector_fn_
        )
        return cls_selector_fn_

    @pytest.fixture
    def content_type_(self, request):
        return instance_mock(request, str)

    @pytest.fixture
    def content_type_2_(self, request):
        return instance_mock(request, str)

    @pytest.fixture
    def CustomPartClass_(self, request, part_of_custom_type_):
        CustomPartClass_ = Mock(name="CustomPartClass", spec=Part)
        CustomPartClass_.load.return_value = part_of_custom_type_
        return CustomPartClass_

    @pytest.fixture
    def DefaultPartClass_(self, request, part_of_default_type_):
        DefaultPartClass_ = cls_attr_mock(request, PartFactory, "default_part_type")
        DefaultPartClass_.load.return_value = part_of_default_type_
        return DefaultPartClass_

    @pytest.fixture
    def package_(self, request):
        return instance_mock(request, OpcPackage)

    @pytest.fixture
    def package_2_(self, request):
        return instance_mock(request, OpcPackage)

    @pytest.fixture
    def part_load_params(self, partname_, content_type_, reltype_, blob_, package_):
        return partname_, content_type_, reltype_, blob_, package_

    @pytest.fixture
    def part_of_custom_type_(self, request):
        return instance_mock(request, Part)

    @pytest.fixture
    def part_of_default_type_(self, request):
        return instance_mock(request, Part)

    @pytest.fixture
    def partname_(self, request):
        return instance_mock(request, PackURI)

    @pytest.fixture
    def partname_2_(self, request):
        return instance_mock(request, PackURI)

    @pytest.fixture
    def part_args_(self, request, partname_, content_type_, reltype_, package_, blob_):
        return partname_, content_type_, reltype_, blob_, package_

    @pytest.fixture
    def part_args_2_(self, request, partname_2_, content_type_2_, reltype_2_, package_2_, blob_2_):
        return partname_2_, content_type_2_, reltype_2_, blob_2_, package_2_

    @pytest.fixture
    def reltype_(self, request):
        return instance_mock(request, str)

    @pytest.fixture
    def reltype_2_(self, request):
        return instance_mock(request, str)


class DescribeXmlPart:
    def it_can_be_constructed_by_PartFactory(
        self, partname_, content_type_, blob_, package_, element_, parse_xml_, __init_
    ):
        part = XmlPart.load(partname_, content_type_, blob_, package_)

        parse_xml_.assert_called_once_with(blob_)
        __init_.assert_called_once_with(ANY, partname_, content_type_, element_, package_)
        assert isinstance(part, XmlPart)

    def it_can_serialize_to_xml(self, blob_fixture):
        xml_part, element_, serialize_part_xml_ = blob_fixture
        blob = xml_part.blob
        serialize_part_xml_.assert_called_once_with(element_)
        assert blob is serialize_part_xml_.return_value

    def it_knows_its_the_part_for_its_child_objects(self, part_fixture):
        xml_part = part_fixture
        assert xml_part.part is xml_part

    @pytest.mark.parametrize(
        ("part_cxml", "rel_should_be_dropped"),
        [
            ("w:p", True),
            ("w:p/r:a{r:id=rId42}", True),
            ("w:p/r:a{r:id=rId42}/r:b{r:id=rId42}", False),
        ],
    )
    def it_only_drops_a_relationship_with_zero_reference_count(
        self, part_cxml: str, rel_should_be_dropped: bool, rels_prop_: Mock, package_: Mock
    ):
        rels_prop_.return_value = {"rId42": None}
        part = XmlPart(PackURI("/partname"), "content_type", element(part_cxml), package_)

        part.drop_rel("rId42")

        assert ("rId42" not in part.rels) is rel_should_be_dropped

    # fixtures -------------------------------------------------------

    @pytest.fixture
    def blob_fixture(self, request, element_, serialize_part_xml_):
        xml_part = XmlPart(None, None, element_, None)
        return xml_part, element_, serialize_part_xml_

    @pytest.fixture
    def part_fixture(self):
        return XmlPart(None, None, None, None)

    # fixture components ---------------------------------------------

    @pytest.fixture
    def blob_(self, request):
        return instance_mock(request, str)

    @pytest.fixture
    def content_type_(self, request):
        return instance_mock(request, str)

    @pytest.fixture
    def element_(self, request):
        return instance_mock(request, BaseOxmlElement)

    @pytest.fixture
    def __init_(self, request):
        return initializer_mock(request, XmlPart)

    @pytest.fixture
    def package_(self, request):
        return instance_mock(request, OpcPackage)

    @pytest.fixture
    def parse_xml_(self, request, element_):
        return function_mock(request, "docx.opc.part.parse_xml", return_value=element_)

    @pytest.fixture
    def partname_(self, request):
        return instance_mock(request, PackURI)

    @pytest.fixture
    def rels_prop_(self, request: FixtureRequest):
        return property_mock(request, XmlPart, "rels")

    @pytest.fixture
    def serialize_part_xml_(self, request):
        return function_mock(request, "docx.opc.part.serialize_part_xml")
