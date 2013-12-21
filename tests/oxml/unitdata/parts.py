# encoding: utf-8

"""
Test data builders for parts XML.
"""

from ...unitdata import BaseBuilder, nsdecls
from .text import a_p, a_sectPr


class CT_BodyBuilder(BaseBuilder):
    """
    Test data builder for CT_Body (<w:body>) XML element that appears in
    document.xml files.
    """
    def __init__(self):
        """Establish instance variables with default values"""
        super(CT_BodyBuilder, self).__init__()
        self._p = None
        self._sectPr = None

    @property
    def is_empty(self):
        return self._p is None and self._sectPr is None

    def with_p(self):
        """Add an empty paragraph element"""
        self._p = a_p()
        return self

    def with_sectPr(self):
        """Add an empty section properties element"""
        self._sectPr = a_sectPr()
        return self

    @property
    def xml(self):
        """Return element XML based on attribute settings"""
        indent = ' ' * self._indent
        if self.is_empty:
            xml = '%s<w:body %s/>\n' % (indent, nsdecls('w'))
        else:
            xml = '%s<w:body %s>\n' % (indent, nsdecls('w'))
            if self._p:
                xml += self._p.with_indent(self._indent+2).xml
            if self._sectPr:
                xml += self._sectPr.with_indent(self._indent+2).xml
            xml += '%s</w:body>\n' % indent
        return xml


class CT_DocumentBuilder(BaseBuilder):
    """
    XML data builder for CT_Document (<w:document>) element, the root element
    in document.xml files.
    """
    def __init__(self):
        """Establish instance variables with default values"""
        super(CT_DocumentBuilder, self).__init__()
        self._body = None

    def with_body(self):
        """Add an empty body element"""
        self._body = a_body().with_indent(2)
        return self

    @property
    def xml(self):
        """
        Return XML string based on settings accumulated via method calls.
        """
        if not self._body:
            return '<w:document %s/>\n' % nsdecls('w')

        xml = '<w:document %s>\n' % nsdecls('w')
        xml += self._body.xml
        xml += '</w:document>\n'
        return xml


def a_body():
    """Return a CT_BodyBuilder instance"""
    return CT_BodyBuilder()


def a_document():
    """Return a CT_DocumentBuilder instance"""
    return CT_DocumentBuilder()
