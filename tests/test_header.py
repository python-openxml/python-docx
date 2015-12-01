# import pytest
from unitutil.file import absjoin, test_file_dir
from docx.api import Document
from docx.oxml.ns import qn
from docx.opc.constants import CONTENT_TYPE as CT, RELATIONSHIP_TYPE as RT
from docx.parts.header import HeaderPart


dir_pkg_path = absjoin(test_file_dir, 'expanded_docx')


class DescribeHeaderLoad(object):
    def it_has_part_as_header_part(self):
        document = Document(dir_pkg_path)
        header_part_exists = False
        for rel_id, part in document.part.related_parts.items():
            if part.content_type == CT.WML_HEADER:
                header_part_exists = True
                assert isinstance(part, HeaderPart)

        assert header_part_exists

    def it_has_rel_as_header_rel(self):
        document = Document(dir_pkg_path)
        header_rel_exists = False
        for rel_id, rel in document.part.rels.items():
            if rel.reltype == RT.HEADER:
                header_rel_exists = True

        assert header_rel_exists


class DescribeClearHeader(object):
    def it_removes_header_part(self):
        document = Document(dir_pkg_path)
        document.remove_headers()

        for rel_id, part in document.part.related_parts.items():
            assert part.content_type != CT.WML_HEADER

        header_elm_tag = 'w:headerReference'
        sentinel_sectPr = document._body._body.get_or_add_sectPr()
        header_elms = sentinel_sectPr.findall(qn(header_elm_tag))
        assert len(header_elms) == 0


class DescribeAddHeader(object):
    def it_adds_a_header(self):
        document = Document(dir_pkg_path)
        document.remove_headers()

        header = document.add_header('foobar')
        header_elm_tag = 'w:headerReference'
        sentinel_sectPr = document._body._body.get_or_add_sectPr()
        header_elms = sentinel_sectPr.findall(qn(header_elm_tag))
        assert len(header_elms) == 1

        assert header
        import uuid
        random_name = uuid.uuid4().hex
        finish_path = '{}.docx'.format(random_name)
        document.save(finish_path)
        print 'file {} header removed!'.format(finish_path)

# class DescribeHeaderAdd(object):
