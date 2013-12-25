# encoding: utf-8

"""
Document parts such as _Document, and closely related classes.
"""

from docx.opc.oxml import serialize_part_xml
from docx.opc.package import Part
from docx.oxml.shared import oxml_fromstring
from docx.shared import lazyproperty
from docx.table import Table
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

    @lazyproperty
    def inline_shapes(self):
        """
        The |InlineShapes| instance containing the inline shapes in the
        document.
        """
        return InlineShapes(self._element.body)

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
        """
        Return a paragraph newly added to the end of body content.
        """
        p = self._body.add_p()
        return Paragraph(p)

    def add_table(self, rows, cols):
        """
        Return a table having *rows* rows and *cols* cols, newly appended to
        the main document story.
        """
        tbl = self._body.add_tbl()
        table = Table(tbl)
        for i in range(cols):
            table.columns.add()
        for i in range(rows):
            table.rows.add()
        return table

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

    @property
    def tables(self):
        """
        A sequence containing all the tables in the document, in the order
        they appear.
        """
        return [Table(tbl) for tbl in self._body.tbl_lst]


class InlineShape(object):
    """
    Proxy for an ``<wp:inline>`` element, representing the container for an
    inline graphical object.
    """


class InlineShapes(object):
    """
    Sequence of |InlineShape| instances, supporting len(), iteration, and
    indexed access.
    """
    def __init__(self, body_elm):
        super(InlineShapes, self).__init__()
        self._body = body_elm
