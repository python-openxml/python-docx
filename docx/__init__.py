# encoding: utf-8

from docx.api import Document  # noqa

__version__ = '0.3.0dev1'


# register custom Part classes with opc package reader

from docx.opc.constants import CONTENT_TYPE as CT
from docx.opc.package import PartFactory

from docx.parts.document import _Document

PartFactory.part_type_for[CT.WML_DOCUMENT_MAIN] = _Document

del CT, _Document, PartFactory
