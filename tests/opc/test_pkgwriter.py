# encoding: utf-8

"""
Test suite for opc.pkgwriter module
"""

import pytest

from docx.opc.constants import CONTENT_TYPE as CT
from docx.opc.packuri import PackURI
from docx.opc.part import Part
from docx.opc.phys_pkg import _ZipPkgWriter
from docx.opc.pkgwriter import _ContentTypesItem, PackageWriter

from .unitdata.types import a_Default, a_Types, an_Override
from ..unitutil.mock import (
    call, class_mock, instance_mock, MagicMock, method_mock, Mock, patch
)


class DescribePackageWriter(object):

    def it_can_write_a_package(self, PhysPkgWriter_, _write_methods):
        # mockery ----------------------
        pkg_file = Mock(name='pkg_file')
        pkg_rels = Mock(name='pkg_rels')
        parts = Mock(name='parts')
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
        _ContentTypesItem_, parts_, phys_pkg_writer_, blob_ = (
            write_cti_fixture
        )
        PackageWriter._write_content_types_stream(phys_pkg_writer_, parts_)
        _ContentTypesItem_.from_parts.assert_called_once_with(parts_)
        phys_pkg_writer_.write.assert_called_once_with(
            '/[Content_Types].xml', blob_
        )

    def it_can_write_a_pkg_rels_item(self):
        # mockery ----------------------
        phys_writer = Mock(name='phys_writer')
        pkg_rels = Mock(name='pkg_rels')
        # exercise ---------------------
        PackageWriter._write_pkg_rels(phys_writer, pkg_rels)
        # verify -----------------------
        phys_writer.write.assert_called_once_with('/_rels/.rels',
                                                  pkg_rels.xml)

    def it_can_write_a_list_of_parts(self):
        # mockery ----------------------
        phys_writer = Mock(name='phys_writer')
        rels = MagicMock(name='rels')
        rels.__len__.return_value = 1
        part1 = Mock(name='part1', _rels=rels)
        part2 = Mock(name='part2', _rels=[])
        # exercise ---------------------
        PackageWriter._write_parts(phys_writer, [part1, part2])
        # verify -----------------------
        expected_calls = [
            call(part1.partname, part1.blob),
            call(part1.partname.rels_uri, part1._rels.xml),
            call(part2.partname, part2.blob),
        ]
        assert phys_writer.write.mock_calls == expected_calls

    # fixtures ---------------------------------------------

    @pytest.fixture
    def blob_(self, request):
        return instance_mock(request, str)

    @pytest.fixture
    def cti_(self, request, blob_):
        return instance_mock(request, _ContentTypesItem, blob=blob_)

    @pytest.fixture
    def _ContentTypesItem_(self, request, cti_):
        _ContentTypesItem_ = class_mock(
            request, 'docx.opc.pkgwriter._ContentTypesItem'
        )
        _ContentTypesItem_.from_parts.return_value = cti_
        return _ContentTypesItem_

    @pytest.fixture
    def parts_(self, request):
        return instance_mock(request, list)

    @pytest.fixture
    def PhysPkgWriter_(self, request):
        _patch = patch('docx.opc.pkgwriter.PhysPkgWriter')
        request.addfinalizer(_patch.stop)
        return _patch.start()

    @pytest.fixture
    def phys_pkg_writer_(self, request):
        return instance_mock(request, _ZipPkgWriter)

    @pytest.fixture
    def write_cti_fixture(
            self, _ContentTypesItem_, parts_, phys_pkg_writer_, blob_):
        return _ContentTypesItem_, parts_, phys_pkg_writer_, blob_

    @pytest.fixture
    def _write_methods(self, request):
        """Mock that patches all the _write_* methods of PackageWriter"""
        root_mock = Mock(name='PackageWriter')
        patch1 = patch.object(PackageWriter, '_write_content_types_stream')
        patch2 = patch.object(PackageWriter, '_write_pkg_rels')
        patch3 = patch.object(PackageWriter, '_write_parts')
        root_mock.attach_mock(patch1.start(), '_write_content_types_stream')
        root_mock.attach_mock(patch2.start(), '_write_pkg_rels')
        root_mock.attach_mock(patch3.start(), '_write_parts')

        def fin():
            patch1.stop()
            patch2.stop()
            patch3.stop()

        request.addfinalizer(fin)
        return root_mock

    @pytest.fixture
    def xml_for_(self, request):
        return method_mock(request, _ContentTypesItem, 'xml_for')


class Describe_ContentTypesItem(object):

    def it_can_compose_content_types_element(self, xml_for_fixture):
        cti, expected_xml = xml_for_fixture
        types_elm = cti._element
        assert types_elm.xml == expected_xml

    # fixtures ---------------------------------------------

    def _mock_part(self, request, name, partname_str, content_type):
        partname = PackURI(partname_str)
        return instance_mock(
            request, Part, name=name, partname=partname,
            content_type=content_type
        )

    @pytest.fixture(params=[
        ('Default',  '/ppt/MEDIA/image.PNG',   CT.PNG),
        ('Default',  '/ppt/media/image.xml',   CT.XML),
        ('Default',  '/ppt/media/image.rels',  CT.OPC_RELATIONSHIPS),
        ('Default',  '/ppt/media/image.jpeg',  CT.JPEG),
        ('Override', '/docProps/core.xml',     'app/vnd.core'),
        ('Override', '/ppt/slides/slide1.xml', 'app/vnd.ct_sld'),
        ('Override', '/zebra/foo.bar',         'app/vnd.foobar'),
    ])
    def xml_for_fixture(self, request):
        elm_type, partname_str, content_type = request.param
        part_ = self._mock_part(request, 'part_', partname_str, content_type)
        cti = _ContentTypesItem.from_parts([part_])
        # expected_xml -----------------
        types_bldr = a_Types().with_nsdecls()
        ext = partname_str.split('.')[-1].lower()
        if elm_type == 'Default' and ext not in ('rels', 'xml'):
            default_bldr = a_Default()
            default_bldr.with_Extension(ext)
            default_bldr.with_ContentType(content_type)
            types_bldr.with_child(default_bldr)

        types_bldr.with_child(
            a_Default().with_Extension('rels')
                       .with_ContentType(CT.OPC_RELATIONSHIPS)
        )
        types_bldr.with_child(
            a_Default().with_Extension('xml').with_ContentType(CT.XML)
        )

        if elm_type == 'Override':
            override_bldr = an_Override()
            override_bldr.with_PartName(partname_str)
            override_bldr.with_ContentType(content_type)
            types_bldr.with_child(override_bldr)

        expected_xml = types_bldr.xml()
        return cti, expected_xml
