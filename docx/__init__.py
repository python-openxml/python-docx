# encoding: utf-8

from docx.api import Document  # noqa

__version__ = '0.5.3'


# register custom Part classes with opc package reader

from docx.opc.constants import CONTENT_TYPE as CT, RELATIONSHIP_TYPE as RT
from docx.opc.package import PartFactory

from docx.parts.document import DocumentPart
from docx.parts.image import ImagePart
from docx.parts.numbering import NumberingPart
from docx.parts.styles import StylesPart
from docx.parts.notes import NotesPart


def part_class_selector(content_type, reltype):
    if reltype == RT.IMAGE:
        return ImagePart
    return None


PartFactory.part_class_selector = part_class_selector
PartFactory.part_type_for[CT.WML_DOCUMENT_MAIN] = DocumentPart
PartFactory.part_type_for[CT.WML_NUMBERING] = NumberingPart
PartFactory.part_type_for[CT.WML_STYLES] = StylesPart
PartFactory.part_type_for[CT.WML_ENDNOTES] = NotesPart
PartFactory.part_type_for[CT.WML_FOOTNOTES] = NotesPart

del CT, DocumentPart, PartFactory, part_class_selector
