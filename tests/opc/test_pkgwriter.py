# pyright: reportPrivateUsage=false

"""Test suite for opc.pkgwriter module."""

from __future__ import annotations

import pytest

from docx.opc.constants import CONTENT_TYPE as CT
from docx.opc.packuri import PackURI
from docx.opc.part import Part
from docx.opc.phys_pkg import _ZipPkgWriter
from docx.opc.pkgwriter import PackageWriter, _ContentTypesItem
from docx.opc.rel import Relationships

from ..unitutil.mock import (
    FixtureRequest,
    Mock,
    call,
    class_mock,
    instance_mock,
    method_mock,
    patch,
)
from .unitdata.types import a_Default, a_Types, an_Override


class DescribePackageWriter:
    def it_can_write_a_package(self, PhysPkgWriter_, _write_methods):
        # mockery ----------------------
        pkg_file = Mock(name="pkg_file")
        pkg_rels = Mock(name="pkg_rels")
        parts = Mock(name="parts")
        phys_writer = PhysPkgWriter_.return_value
        # exercise ---------------------
        PackageWriter.write(pkg_file, pkg_rels, parts)
        # verify -----------------------
        expected_calls = [
            call._write_content_types_stream(phys_writer, parts),
            call._write_pkg_rels(phys_writer, pkg_rels),
            call._write_parts(phys_writer, parts),
        ]
        PhysPkgWriter_.assert_called_once_with(pkg_file)
        assert _write_methods.mock_calls == expected_calls
        phys_writer.close.assert_called_once_with()

    def it_can_write_a_content_types_stream(self, write_cti_fixture):
        _ContentTypesItem_, parts_, phys_pkg_writer_, blob_ = write_cti_fixture
        PackageWriter._write_content_types_stream(phys_pkg_writer_, parts_)
        _ContentTypesItem_.from_parts.assert_called_once_with(parts_)
        phys_pkg_writer_.write.assert_called_once_with("/[Content_Types].xml", blob_)

    def it_can_write_a_pkg_rels_item(self):
        # mockery ----------------------
        phys_writer = Mock(name="phys_writer")
        pkg_rels = Mock(name="pkg_rels")
        # exercise ---------------------
        PackageWriter._write_pkg_rels(phys_writer, pkg_rels)
        # verify -----------------------
        phys_writer.write.assert_called_once_with("/_rels/.rels", pkg_rels.xml)

    def it_can_write_a_list_of_parts(
        self, phys_pkg_writer_: Mock, part_: Mock, part_2_: Mock, rels_: Mock
    ):
        rels_.__len__.return_value = 1
        part_.rels = rels_
        part_2_.rels = []

        PackageWriter._write_parts(phys_pkg_writer_, [part_, part_2_])

        expected_calls = [
            call(part_.partname, part_.blob),
            call(part_.partname.rels_uri, part_.rels.xml),
            call(part_2_.partname, part_2_.blob),
        ]
        assert phys_pkg_writer_.write.mock_calls == expected_calls

    # fixtures ---------------------------------------------

    @pytest.fixture
    def blob_(self, request: FixtureRequest):
        return instance_mock(request, str)

    @pytest.fixture
    def cti_(self, request: FixtureRequest, blob_):
        return instance_mock(request, _ContentTypesItem, blob=blob_)

    @pytest.fixture
    def _ContentTypesItem_(self, request: FixtureRequest, cti_):
        _ContentTypesItem_ = class_mock(request, "docx.opc.pkgwriter._ContentTypesItem")
        _ContentTypesItem_.from_parts.return_value = cti_
        return _ContentTypesItem_

    @pytest.fixture
    def part_(self, request: FixtureRequest):
        return instance_mock(request, Part)

    @pytest.fixture
    def part_2_(self, request: FixtureRequest):
        return instance_mock(request, Part)

    @pytest.fixture
    def parts_(self, request: FixtureRequest):
        return instance_mock(request, list)

    @pytest.fixture
    def PhysPkgWriter_(self):
        p = patch("docx.opc.pkgwriter.PhysPkgWriter")
        yield p.start()
        p.stop()

    @pytest.fixture
    def phys_pkg_writer_(self, request: FixtureRequest):
        return instance_mock(request, _ZipPkgWriter)

    @pytest.fixture
    def rels_(self, request: FixtureRequest):
        return instance_mock(request, Relationships)

    @pytest.fixture
    def write_cti_fixture(self, _ContentTypesItem_, parts_, phys_pkg_writer_, blob_):
        return _ContentTypesItem_, parts_, phys_pkg_writer_, blob_

    @pytest.fixture
    def _write_methods(self):
        """Mock that patches all the _write_* methods of PackageWriter"""
        root_mock = Mock(name="PackageWriter")
        patch1 = patch.object(PackageWriter, "_write_content_types_stream")
        patch2 = patch.object(PackageWriter, "_write_pkg_rels")
        patch3 = patch.object(PackageWriter, "_write_parts")
        root_mock.attach_mock(patch1.start(), "_write_content_types_stream")
        root_mock.attach_mock(patch2.start(), "_write_pkg_rels")
        root_mock.attach_mock(patch3.start(), "_write_parts")

        yield root_mock

        patch1.stop()
        patch2.stop()
        patch3.stop()

    @pytest.fixture
    def xml_for_(self, request: FixtureRequest):
        return method_mock(request, _ContentTypesItem, "xml_for")


class Describe_ContentTypesItem:
    def it_can_compose_content_types_element(self, xml_for_fixture):
        cti, expected_xml = xml_for_fixture
        types_elm = cti._element
        assert types_elm.xml == expected_xml

    # fixtures ---------------------------------------------

    def _mock_part(self, request: FixtureRequest, name, partname_str, content_type):
        partname = PackURI(partname_str)
        return instance_mock(request, Part, name=name, partname=partname, content_type=content_type)

    @pytest.fixture(
        params=[
            ("Default", "/ppt/MEDIA/image.PNG", CT.PNG),
            ("Default", "/ppt/media/image.xml", CT.XML),
            ("Default", "/ppt/media/image.rels", CT.OPC_RELATIONSHIPS),
            ("Default", "/ppt/media/image.jpeg", CT.JPEG),
            ("Override", "/docProps/core.xml", "app/vnd.core"),
            ("Override", "/ppt/slides/slide1.xml", "app/vnd.ct_sld"),
            ("Override", "/zebra/foo.bar", "app/vnd.foobar"),
        ]
    )
    def xml_for_fixture(self, request: FixtureRequest):
        elm_type, partname_str, content_type = request.param
        part_ = self._mock_part(request, "part_", partname_str, content_type)
        cti = _ContentTypesItem.from_parts([part_])
        # expected_xml -----------------
        types_bldr = a_Types().with_nsdecls()
        ext = partname_str.split(".")[-1].lower()
        if elm_type == "Default" and ext not in ("rels", "xml"):
            default_bldr = a_Default()
            default_bldr.with_Extension(ext)
            default_bldr.with_ContentType(content_type)
            types_bldr.with_child(default_bldr)

        types_bldr.with_child(
            a_Default().with_Extension("rels").with_ContentType(CT.OPC_RELATIONSHIPS)
        )
        types_bldr.with_child(a_Default().with_Extension("xml").with_ContentType(CT.XML))

        if elm_type == "Override":
            override_bldr = an_Override()
            override_bldr.with_PartName(partname_str)
            override_bldr.with_ContentType(content_type)
            types_bldr.with_child(override_bldr)

        expected_xml = types_bldr.xml()
        return cti, expected_xml
