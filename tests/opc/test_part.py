# encoding: utf-8

"""Unit test suite for docx.opc.part module"""

from __future__ import absolute_import, division, print_function, unicode_literals

import pytest

from docx.opc.package import OpcPackage
from docx.opc.packuri import PackURI
from docx.opc.part import Part, PartFactory, XmlPart
from docx.opc.rel import _Relationship, Relationships
from docx.oxml.xmlchemy import BaseOxmlElement

from ..unitutil.cxml import element
from ..unitutil.mock import (
    ANY,
    class_mock,
    cls_attr_mock,
    function_mock,
    initializer_mock,
    instance_mock,
    loose_mock,
    Mock,
)


class DescribePart(object):

    def it_can_be_constructed_by_PartFactory(
        self, partname_, content_type_, blob_, package_, __init_
    ):
        part = Part.load(partname_, content_type_, blob_, package_)

        __init_.assert_called_once_with(ANY, partname_, content_type_, blob_, package_)
        assert isinstance(part, Part)

    def it_knows_its_partname(self, partname_get_fixture):
        part, expected_partname = partname_get_fixture
        assert part.partname == expected_partname

    def it_can_change_its_partname(self, partname_set_fixture):
        part, new_partname = partname_set_fixture
        part.partname = new_partname
        assert part.partname == new_partname

    def it_knows_its_content_type(self, content_type_fixture):
        part, expected_content_type = content_type_fixture
        assert part.content_type == expected_content_type

    def it_knows_the_package_it_belongs_to(self, package_get_fixture):
        part, expected_package = package_get_fixture
        assert part.package == expected_package

    def it_can_be_notified_after_unmarshalling_is_complete(self, part):
        part.after_unmarshal()

    def it_can_be_notified_before_marshalling_is_started(self, part):
        part.before_marshal()

    def it_uses_the_load_blob_as_its_blob(self, blob_fixture):
        part, load_blob = blob_fixture
        assert part.blob is load_blob

    # fixtures ---------------------------------------------

    @pytest.fixture
    def blob_fixture(self, blob_):
        part = Part(None, None, blob_, None)
        return part, blob_

    @pytest.fixture
    def content_type_fixture(self):
        content_type = 'content/type'
        part = Part(None, content_type, None, None)
        return part, content_type

    @pytest.fixture
    def package_get_fixture(self, package_):
        part = Part(None, None, None, package_)
        return part, package_

    @pytest.fixture
    def part(self):
        part = Part(None, None)
        return part

    @pytest.fixture
    def partname_get_fixture(self):
        partname = PackURI('/part/name')
        part = Part(partname, None, None, None)
        return part, partname

    @pytest.fixture
    def partname_set_fixture(self):
        old_partname = PackURI('/old/part/name')
        new_partname = PackURI('/new/part/name')
        part = Part(old_partname, None, None, None)
        return part, new_partname

    # fixture components ---------------------------------------------

    @pytest.fixture
    def blob_(self, request):
        return instance_mock(request, bytes)

    @pytest.fixture
    def content_type_(self, request):
        return instance_mock(request, str)

    @pytest.fixture
    def __init_(self, request):
        return initializer_mock(request, Part)

    @pytest.fixture
    def package_(self, request):
        return instance_mock(request, OpcPackage)

    @pytest.fixture
    def partname_(self, request):
        return instance_mock(request, PackURI)


class DescribePartRelationshipManagementInterface(object):

    def it_provides_access_to_its_relationships(self, rels_fixture):
        part, Relationships_, partname_, rels_ = rels_fixture
        rels = part.rels
        Relationships_.assert_called_once_with(partname_.baseURI)
        assert rels is rels_

    def it_can_load_a_relationship(self, load_rel_fixture):
        part, rels_, reltype_, target_, rId_ = load_rel_fixture
        part.load_rel(reltype_, target_, rId_)
        rels_.add_relationship.assert_called_once_with(
            reltype_, target_, rId_, False
        )

    def it_can_establish_a_relationship_to_another_part(
            self, relate_to_part_fixture):
        part, target_, reltype_, rId_ = relate_to_part_fixture
        rId = part.relate_to(target_, reltype_)
        part.rels.get_or_add.assert_called_once_with(reltype_, target_)
        assert rId is rId_

    def it_can_establish_an_external_relationship(
            self, relate_to_url_fixture):
        part, url_, reltype_, rId_ = relate_to_url_fixture
        rId = part.relate_to(url_, reltype_, is_external=True)
        part.rels.get_or_add_ext_rel.assert_called_once_with(reltype_, url_)
        assert rId is rId_

    def it_can_drop_a_relationship(self, drop_rel_fixture):
        part, rId, rel_should_be_gone = drop_rel_fixture
        part.drop_rel(rId)
        if rel_should_be_gone:
            assert rId not in part.rels
        else:
            assert rId in part.rels

    def it_can_find_a_related_part_by_reltype(self, related_part_fixture):
        part, reltype_, related_part_ = related_part_fixture
        related_part = part.part_related_by(reltype_)
        part.rels.part_with_reltype.assert_called_once_with(reltype_)
        assert related_part is related_part_

    def it_can_find_a_related_part_by_rId(self, related_parts_fixture):
        part, related_parts_ = related_parts_fixture
        assert part.related_parts is related_parts_

    def it_can_find_the_uri_of_an_external_relationship(
            self, target_ref_fixture):
        part, rId_, url_ = target_ref_fixture
        url = part.target_ref(rId_)
        assert url == url_

    # fixtures ---------------------------------------------

    @pytest.fixture(params=[
        ('w:p', True),
        ('w:p/r:a{r:id=rId42}', True),
        ('w:p/r:a{r:id=rId42}/r:b{r:id=rId42}', False),
    ])
    def drop_rel_fixture(self, request, part):
        part_cxml, rel_should_be_dropped = request.param
        rId = 'rId42'
        part._element = element(part_cxml)
        part._rels = {rId: None}
        return part, rId, rel_should_be_dropped

    @pytest.fixture
    def load_rel_fixture(self, part, rels_, reltype_, part_, rId_):
        part._rels = rels_
        return part, rels_, reltype_, part_, rId_

    @pytest.fixture
    def relate_to_part_fixture(
            self, request, part, reltype_, part_, rels_, rId_):
        part._rels = rels_
        target_ = part_
        return part, target_, reltype_, rId_

    @pytest.fixture
    def relate_to_url_fixture(
            self, request, part, rels_, url_, reltype_, rId_):
        part._rels = rels_
        return part, url_, reltype_, rId_

    @pytest.fixture
    def related_part_fixture(self, request, part, rels_, reltype_, part_):
        part._rels = rels_
        return part, reltype_, part_

    @pytest.fixture
    def related_parts_fixture(self, request, part, rels_, related_parts_):
        part._rels = rels_
        return part, related_parts_

    @pytest.fixture
    def rels_fixture(self, Relationships_, partname_, rels_):
        part = Part(partname_, None)
        return part, Relationships_, partname_, rels_

    @pytest.fixture
    def target_ref_fixture(self, request, part, rId_, rel_, url_):
        part._rels = {rId_: rel_}
        return part, rId_, url_

    # fixture components ---------------------------------------------

    @pytest.fixture
    def part(self):
        return Part(None, None)

    @pytest.fixture
    def part_(self, request):
        return instance_mock(request, Part)

    @pytest.fixture
    def partname_(self, request):
        return instance_mock(request, PackURI)

    @pytest.fixture
    def Relationships_(self, request, rels_):
        return class_mock(
            request, 'docx.opc.part.Relationships', return_value=rels_
        )

    @pytest.fixture
    def rel_(self, request, rId_, url_):
        return instance_mock(
            request, _Relationship, rId=rId_, target_ref=url_
        )

    @pytest.fixture
    def rels_(self, request, part_, rel_, rId_, related_parts_):
        rels_ = instance_mock(request, Relationships)
        rels_.part_with_reltype.return_value = part_
        rels_.get_or_add.return_value = rel_
        rels_.get_or_add_ext_rel.return_value = rId_
        rels_.related_parts = related_parts_
        return rels_

    @pytest.fixture
    def related_parts_(self, request):
        return instance_mock(request, dict)

    @pytest.fixture
    def reltype_(self, request):
        return instance_mock(request, str)

    @pytest.fixture
    def rId_(self, request):
        return instance_mock(request, str)

    @pytest.fixture
    def url_(self, request):
        return instance_mock(request, str)


class DescribePartFactory(object):

    def it_constructs_part_from_selector_if_defined(
            self, cls_selector_fixture):
        # fixture ----------------------
        (cls_selector_fn_, part_load_params, CustomPartClass_,
         part_of_custom_type_) = cls_selector_fixture
        partname, content_type, reltype, blob, package = part_load_params
        # exercise ---------------------
        PartFactory.part_class_selector = cls_selector_fn_
        part = PartFactory(partname, content_type, reltype, blob, package)
        # verify -----------------------
        cls_selector_fn_.assert_called_once_with(content_type, reltype)
        CustomPartClass_.load.assert_called_once_with(
            partname, content_type, blob, package
        )
        assert part is part_of_custom_type_

    def it_constructs_custom_part_type_for_registered_content_types(
            self, part_args_, CustomPartClass_, part_of_custom_type_):
        # fixture ----------------------
        partname, content_type, reltype, package, blob = part_args_
        # exercise ---------------------
        PartFactory.part_type_for[content_type] = CustomPartClass_
        part = PartFactory(partname, content_type, reltype, blob, package)
        # verify -----------------------
        CustomPartClass_.load.assert_called_once_with(
            partname, content_type, blob, package
        )
        assert part is part_of_custom_type_

    def it_constructs_part_using_default_class_when_no_custom_registered(
            self, part_args_2_, DefaultPartClass_, part_of_default_type_):
        partname, content_type, reltype, blob, package = part_args_2_
        part = PartFactory(partname, content_type, reltype, blob, package)
        DefaultPartClass_.load.assert_called_once_with(
            partname, content_type, blob, package
        )
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
        return function_mock(
            request, 'docx.opc.part.cls_method_fn',
            return_value=cls_selector_fn_
        )

    @pytest.fixture
    def cls_selector_fixture(
            self, request, cls_selector_fn_, cls_method_fn_, part_load_params,
            CustomPartClass_, part_of_custom_type_):
        def reset_part_class_selector():
            PartFactory.part_class_selector = original_part_class_selector
        original_part_class_selector = PartFactory.part_class_selector
        request.addfinalizer(reset_part_class_selector)
        return (
            cls_selector_fn_, part_load_params, CustomPartClass_,
            part_of_custom_type_
        )

    @pytest.fixture
    def cls_selector_fn_(self, request, CustomPartClass_):
        cls_selector_fn_ = loose_mock(request)
        # Python 3 version
        cls_selector_fn_.return_value = CustomPartClass_
        # Python 2 version
        cls_selector_fn_.__func__ = loose_mock(
            request, name='__func__', return_value=cls_selector_fn_
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
        CustomPartClass_ = Mock(name='CustomPartClass', spec=Part)
        CustomPartClass_.load.return_value = part_of_custom_type_
        return CustomPartClass_

    @pytest.fixture
    def DefaultPartClass_(self, request, part_of_default_type_):
        DefaultPartClass_ = cls_attr_mock(
            request, PartFactory, 'default_part_type'
        )
        DefaultPartClass_.load.return_value = part_of_default_type_
        return DefaultPartClass_

    @pytest.fixture
    def package_(self, request):
        return instance_mock(request, OpcPackage)

    @pytest.fixture
    def package_2_(self, request):
        return instance_mock(request, OpcPackage)

    @pytest.fixture
    def part_load_params(
            self, partname_, content_type_, reltype_, blob_, package_):
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
    def part_args_(
            self, request, partname_, content_type_, reltype_, package_,
            blob_):
        return partname_, content_type_, reltype_, blob_, package_

    @pytest.fixture
    def part_args_2_(
            self, request, partname_2_, content_type_2_, reltype_2_,
            package_2_, blob_2_):
        return partname_2_, content_type_2_, reltype_2_, blob_2_, package_2_

    @pytest.fixture
    def reltype_(self, request):
        return instance_mock(request, str)

    @pytest.fixture
    def reltype_2_(self, request):
        return instance_mock(request, str)


class DescribeXmlPart(object):

    def it_can_be_constructed_by_PartFactory(
        self, partname_, content_type_, blob_, package_, element_, parse_xml_, __init_
    ):
        part = XmlPart.load(partname_, content_type_, blob_, package_)

        parse_xml_.assert_called_once_with(blob_)
        __init_.assert_called_once_with(
            ANY, partname_, content_type_, element_, package_
        )
        assert isinstance(part, XmlPart)

    def it_can_serialize_to_xml(self, blob_fixture):
        xml_part, element_, serialize_part_xml_ = blob_fixture
        blob = xml_part.blob
        serialize_part_xml_.assert_called_once_with(element_)
        assert blob is serialize_part_xml_.return_value

    def it_knows_its_the_part_for_its_child_objects(self, part_fixture):
        xml_part = part_fixture
        assert xml_part.part is xml_part

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
        return function_mock(
            request, 'docx.opc.part.parse_xml', return_value=element_
        )

    @pytest.fixture
    def partname_(self, request):
        return instance_mock(request, PackURI)

    @pytest.fixture
    def serialize_part_xml_(self, request):
        return function_mock(
            request, 'docx.opc.part.serialize_part_xml'
        )
