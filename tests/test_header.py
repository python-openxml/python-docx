# import pytest
from unitutil.file import absjoin, test_file_dir
from docx.api import Document
from docx.opc.constants import CONTENT_TYPE as CT
from docx.parts.header import HeaderPart


dir_pkg_path = absjoin(test_file_dir, 'expanded_docx')


class DescribeHeader(object):
    def it_loads_header_as_header_part(self):
        document = Document(dir_pkg_path)
        for rel_id, part in document.part.related_parts.items():
            if part.content_type == CT.WML_HEADER:
                assert isinstance(part, HeaderPart)
