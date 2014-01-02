# encoding: utf-8

from docx.api import Document  # noqa

__version__ = '0.3.0a1'


# register custom Part classes with opc package reader

from docx.opc.constants import CONTENT_TYPE as CT, RELATIONSHIP_TYPE as RT
from docx.opc.package import PartFactory

from docx.parts.document import DocumentPart
from docx.parts.image import ImagePart


def part_class_selector(content_type, reltype):
    if reltype == RT.IMAGE:
        return ImagePart
    return None


PartFactory.part_class_selector = part_class_selector
PartFactory.part_type_for[CT.WML_DOCUMENT_MAIN] = DocumentPart

del CT, DocumentPart, PartFactory, part_class_selector
