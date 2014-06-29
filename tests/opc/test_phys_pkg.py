# encoding: utf-8

"""
Test suite for docx.opc.phys_pkg module
"""

from __future__ import absolute_import

try:
    from io import BytesIO  # Python 3
except ImportError:
    from StringIO import StringIO as BytesIO

import hashlib
import pytest

from zipfile import ZIP_DEFLATED, ZipFile

from docx.opc.exceptions import PackageNotFoundError
from docx.opc.packuri import PACKAGE_URI, PackURI
from docx.opc.phys_pkg import (
    _DirPkgReader, PhysPkgReader, PhysPkgWriter, _ZipPkgReader, _ZipPkgWriter
)

from ..unitutil.file import absjoin, test_file_dir
from ..unitutil.mock import class_mock, loose_mock, Mock


test_docx_path = absjoin(test_file_dir, 'test.docx')
dir_pkg_path = absjoin(test_file_dir, 'expanded_docx')
zip_pkg_path = test_docx_path


class DescribeDirPkgReader(object):

    def it_is_used_by_PhysPkgReader_when_pkg_is_a_dir(self):
        phys_reader = PhysPkgReader(dir_pkg_path)
        assert isinstance(phys_reader, _DirPkgReader)

    def it_doesnt_mind_being_closed_even_though_it_doesnt_need_it(
            self, dir_reader):
        dir_reader.close()

    def it_can_retrieve_the_blob_for_a_pack_uri(self, dir_reader):
        pack_uri = PackURI('/word/document.xml')
        blob = dir_reader.blob_for(pack_uri)
        sha1 = hashlib.sha1(blob).hexdigest()
        assert sha1 == '0e62d87ea74ea2b8088fd11ee97b42da9b4c77b0'

    def it_can_get_the_content_types_xml(self, dir_reader):
        sha1 = hashlib.sha1(dir_reader.content_types_xml).hexdigest()
        assert sha1 == '89aadbb12882dd3d7340cd47382dc2c73d75dd81'

    def it_can_retrieve_the_rels_xml_for_a_source_uri(self, dir_reader):
        rels_xml = dir_reader.rels_xml_for(PACKAGE_URI)
        sha1 = hashlib.sha1(rels_xml).hexdigest()
        assert sha1 == 'ebacdddb3e7843fdd54c2f00bc831551b26ac823'

    def it_returns_none_when_part_has_no_rels_xml(self, dir_reader):
        partname = PackURI('/ppt/viewProps.xml')
        rels_xml = dir_reader.rels_xml_for(partname)
        assert rels_xml is None

    # fixtures ---------------------------------------------

    @pytest.fixture
    def pkg_file_(self, request):
        return loose_mock(request)

    @pytest.fixture(scope='class')
    def dir_reader(self):
        return _DirPkgReader(dir_pkg_path)


class DescribePhysPkgReader(object):

    def it_raises_when_pkg_path_is_not_a_package(self):
        with pytest.raises(PackageNotFoundError):
            PhysPkgReader('foobar')


class DescribeZipPkgReader(object):

    def it_is_used_by_PhysPkgReader_when_pkg_is_a_zip(self):
        phys_reader = PhysPkgReader(zip_pkg_path)
        assert isinstance(phys_reader, _ZipPkgReader)

    def it_is_used_by_PhysPkgReader_when_pkg_is_a_stream(self):
        with open(zip_pkg_path, 'rb') as stream:
            phys_reader = PhysPkgReader(stream)
        assert isinstance(phys_reader, _ZipPkgReader)

    def it_opens_pkg_file_zip_on_construction(self, ZipFile_, pkg_file_):
        _ZipPkgReader(pkg_file_)
        ZipFile_.assert_called_once_with(pkg_file_, 'r')

    def it_can_be_closed(self, ZipFile_):
        # mockery ----------------------
        zipf = ZipFile_.return_value
        zip_pkg_reader = _ZipPkgReader(None)
        # exercise ---------------------
        zip_pkg_reader.close()
        # verify -----------------------
        zipf.close.assert_called_once_with()

    def it_can_retrieve_the_blob_for_a_pack_uri(self, phys_reader):
        pack_uri = PackURI('/word/document.xml')
        blob = phys_reader.blob_for(pack_uri)
        sha1 = hashlib.sha1(blob).hexdigest()
        assert sha1 == 'b9b4a98bcac7c5a162825b60c3db7df11e02ac5f'

    def it_has_the_content_types_xml(self, phys_reader):
        sha1 = hashlib.sha1(phys_reader.content_types_xml).hexdigest()
        assert sha1 == 'cd687f67fd6b5f526eedac77cf1deb21968d7245'

    def it_can_retrieve_rels_xml_for_source_uri(self, phys_reader):
        rels_xml = phys_reader.rels_xml_for(PACKAGE_URI)
        sha1 = hashlib.sha1(rels_xml).hexdigest()
        assert sha1 == '90965123ed2c79af07a6963e7cfb50a6e2638565'

    def it_returns_none_when_part_has_no_rels_xml(self, phys_reader):
        partname = PackURI('/ppt/viewProps.xml')
        rels_xml = phys_reader.rels_xml_for(partname)
        assert rels_xml is None

    # fixtures ---------------------------------------------

    @pytest.fixture(scope='class')
    def phys_reader(self, request):
        phys_reader = _ZipPkgReader(zip_pkg_path)
        request.addfinalizer(phys_reader.close)
        return phys_reader

    @pytest.fixture
    def pkg_file_(self, request):
        return loose_mock(request)


class DescribeZipPkgWriter(object):

    def it_is_used_by_PhysPkgWriter_unconditionally(self, tmp_docx_path):
        phys_writer = PhysPkgWriter(tmp_docx_path)
        assert isinstance(phys_writer, _ZipPkgWriter)

    def it_opens_pkg_file_zip_on_construction(self, ZipFile_):
        pkg_file = Mock(name='pkg_file')
        _ZipPkgWriter(pkg_file)
        ZipFile_.assert_called_once_with(
            pkg_file, 'w', compression=ZIP_DEFLATED
        )

    def it_can_be_closed(self, ZipFile_):
        # mockery ----------------------
        zipf = ZipFile_.return_value
        zip_pkg_writer = _ZipPkgWriter(None)
        # exercise ---------------------
        zip_pkg_writer.close()
        # verify -----------------------
        zipf.close.assert_called_once_with()

    def it_can_write_a_blob(self, pkg_file):
        # setup ------------------------
        pack_uri = PackURI('/part/name.xml')
        blob = '<BlobbityFooBlob/>'.encode('utf-8')
        # exercise ---------------------
        pkg_writer = PhysPkgWriter(pkg_file)
        pkg_writer.write(pack_uri, blob)
        pkg_writer.close()
        # verify -----------------------
        written_blob_sha1 = hashlib.sha1(blob).hexdigest()
        zipf = ZipFile(pkg_file, 'r')
        retrieved_blob = zipf.read(pack_uri.membername)
        zipf.close()
        retrieved_blob_sha1 = hashlib.sha1(retrieved_blob).hexdigest()
        assert retrieved_blob_sha1 == written_blob_sha1

    # fixtures ---------------------------------------------

    @pytest.fixture
    def pkg_file(self, request):
        pkg_file = BytesIO()
        request.addfinalizer(pkg_file.close)
        return pkg_file


# fixtures -------------------------------------------------

@pytest.fixture
def tmp_docx_path(tmpdir):
    return str(tmpdir.join('test_python-docx.docx'))


@pytest.fixture
def ZipFile_(request):
    return class_mock(request, 'docx.opc.phys_pkg.ZipFile')
