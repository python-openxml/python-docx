# encoding: utf-8

"""
Document parts such as _Document, and closely related classes.
"""

from docx.opc.oxml import serialize_part_xml
from docx.opc.package import Part
from docx.oxml.shared import oxml_fromstring
from docx.text import Paragraph


class _Document(Part):
    """
    Main document part of a WordprocessingML (WML) package, aka a .docx file.
    """
    def __init__(self, partname, content_type, document_elm, package):
        super(_Document, self).__init__(
            partname, content_type, package=package
        )
        self._element = document_elm

    @property
    def blob(self):
        return serialize_part_xml(self._element)

    @property
    def body(self):
        """
        The |_Body| instance containing the content for this document.
        """
        return _Body(self._element.body)

    @staticmethod
    def load(partname, content_type, blob, package):
        document_elm = oxml_fromstring(blob)
        document = _Document(partname, content_type, document_elm, package)
        return document


class _Body(object):
    """
    Proxy for ``<w:body>`` element in this document, having primarily a
    container role.
    """
    def __init__(self, body_elm):
        super(_Body, self).__init__()
        self._body = body_elm

    def add_paragraph(self):
        p = self._body.add_p()
        return Paragraph(p)

    def clear_content(self):
        """
        Return this |_Body| instance after clearing it of all content.
        Section properties for the main document story, if present, are
        preserved.
        """
        self._body.clear_content()
        return self

    @property
    def paragraphs(self):
        return [Paragraph(p) for p in self._body.p_lst]
