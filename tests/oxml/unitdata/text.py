# encoding: utf-8

"""
Test data builders for text XML elements
"""

from ...unitdata import BaseBuilder


class CT_PBuilder(BaseBuilder):
    """
    Test data builder for a CT_P (<w:p>) XML element that appears within the
    body element of a document.xml file.
    """
    def __init__(self):
        """Establish instance variables with default values"""
        super(CT_PBuilder, self).__init__()
        self._pPr = None
        self._r = []

    @property
    def is_empty(self):
        return self._pPr is None and len(self._r) == 0

    def with_pPr(self, pPr=None):
        """Add a <w:pPr> child element"""
        if pPr is None:
            pPr = a_pPr()
        self._pPr = pPr
        return self

    def with_r(self, count=1):
        """Add *count* empty run elements"""
        for i in range(count):
            self._r.append(an_r())
        return self

    @property
    def xml(self):
        """Return element XML based on attribute settings"""
        indent = ' ' * self._indent
        if self.is_empty:
            xml = '%s<w:p%s/>\n' % (indent, self._nsdecls)
        else:
            xml = '%s<w:p%s>\n' % (indent, self._nsdecls)
            if self._pPr:
                xml += self._pPr.with_indent(self._indent+2).xml
            for r in self._r:
                xml += r.with_indent(self._indent+2).xml
            xml += '%s</w:p>\n' % indent
        return xml


class CT_PPrBuilder(BaseBuilder):
    """
    Test data builder for a CT_PPr (<w:pPr>) XML element that appears as a
    child of a <w:p> element in a document.xml file.
    """
    def __init__(self):
        """Establish instance variables with default values"""
        super(CT_PPrBuilder, self).__init__()
        self._pStyle = None

    @property
    def is_empty(self):
        return self._pStyle is None

    def with_style(self, style='foobar'):
        """Add pStyle child with inner text *style*"""
        self._pStyle = '<w:pStyle w:val="%s"/>' % style
        return self

    @property
    def xml(self):
        """Return element XML based on attribute settings"""
        indent = ' ' * self._indent
        if self.is_empty:
            xml = '%s<w:pPr%s/>\n' % (indent, self._nsdecls)
        else:
            xml = '%s<w:pPr%s>\n' % (indent, self._nsdecls)
            if self._pStyle:
                xml += '%s%s\n' % (indent+'  ', self._pStyle)
            xml += '%s</w:pPr>\n' % indent
        return xml


class CT_RBuilder(BaseBuilder):
    """
    Test data builder for a CT_R (<w:r>) XML element that appears within the
    body element of a document.xml file.
    """
    def __init__(self):
        """Establish instance variables with default values"""
        super(CT_RBuilder, self).__init__()
        self._t = []

    @property
    def is_empty(self):
        return len(self._t) == 0

    def with_t(self, text):
        """Add an text element containing *text*"""
        self._t.append(a_t(text))
        return self

    @property
    def xml(self):
        """Return element XML based on attribute settings"""
        indent = ' ' * self._indent
        if self.is_empty:
            xml = '%s<w:r%s/>\n' % (indent, self._nsdecls)
        else:
            xml = '%s<w:r%s>\n' % (indent, self._nsdecls)
            for t_builder in self._t:
                xml += t_builder.with_indent(self._indent+2).xml
            xml += '%s</w:r>\n' % indent
        return xml


class CT_TextBuilder(BaseBuilder):
    """
    Test data builder for a CT_Text (<w:t>) XML element that appears within a
    run element.
    """
    def __init__(self, text):
        """Establish instance variables with default values"""
        super(CT_TextBuilder, self).__init__()
        self._text = text

    @property
    def xml(self):
        """Return element XML based on attribute settings"""
        indent = ' ' * self._indent
        return '%s<w:t%s>%s</w:t>\n' % (indent, self._nsdecls, self._text)


class CT_SectPrBuilder(BaseBuilder):
    """
    Test data builder for a CT_SectPr (<w:sectPr>) XML element that appears
    within the body element of a document.xml file.
    """
    def __init__(self):
        """Establish instance variables with default values"""
        super(CT_SectPrBuilder, self).__init__()

    @property
    def xml(self):
        """Return element XML based on attribute settings"""
        tmpl = '%s<w:sectPr/>\n'
        indent = ' ' * self._indent
        return tmpl % (indent)


def a_p():
    """Return a CT_PBuilder instance"""
    return CT_PBuilder()


def a_pPr():
    """Return a CT_PPrBuilder instance"""
    return CT_PPrBuilder()


def a_t(text):
    """Return a CT_TextBuilder instance"""
    return CT_TextBuilder(text)


def a_sectPr():
    """Return a CT_SectPr instance"""
    return CT_SectPrBuilder()


def an_r():
    """Return a CT_RBuilder instance"""
    return CT_RBuilder()
