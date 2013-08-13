# -*- coding: utf-8 -*-
#
# oxml/text.py
#
# Copyright (C) 2013 Steve Canny scanny@cisco.com
#
# This module is part of python-docx and is released under the MIT License:
# http://www.opensource.org/licenses/mit-license.php

"""
Custom element classes related to text, such as paragraph (CT_P) and runs
(CT_R).
"""

from docx.oxml.base import (
    _Element, nsdecls, OxmlBaseElement, oxml_fromstring, qn
)


class CT_P(OxmlBaseElement):
    """
    ``<w:p>`` element, containing the properties and text for a paragraph.
    """
    def __setattr__(self, attr, value):
        """
        Implement setter side of properties. Filters ``__setattr__`` messages
        to ObjectifiedElement base class to intercept messages intended for
        custom property setters.
        """
        if attr == 'style':
            self._set_style(value)
        else:
            super(CT_P, self).__setattr__(attr, value)

    def add_r(self):
        """
        Return a newly added CT_R (<w:r>) element.
        """
        r = CT_R.new()
        self.append(r)
        return r

    @staticmethod
    def new():
        """
        Return a new ``<w:p>`` element.
        """
        xml = '<w:p %s/>' % nsdecls('w')
        p = oxml_fromstring(xml)
        return p

    @property
    def r_elms(self):
        """
        Sequence containing a reference to each run element in this paragraph.
        """
        if not hasattr(self, 'r'):
            return ()
        return tuple([r for r in self.r])

    @property
    def style(self):
        """
        String contained in w:val attribute of <w:pPr><w:pStyle> child, or
        None if that element is not present.
        """
        return self.pPr.style if self._has_pPr else None

    def _get_or_add_pPr(self):
        """
        Return the pPr child element of this <w:p> element, adding a new one
        if one is not present.
        """
        if not self._has_pPr:
            self.insert(0, CT_PPr.new())
        return self.pPr

    @property
    def _has_pPr(self):
        """
        Return True if this <w:p> element has a <w:pPr> child element, False
        otherwise.
        """
        return hasattr(self, 'pPr')

    def _set_style(self, style):
        """
        Set style of this <w:p> element to *style*. If *style* is None,
        remove the style element. If the pPr element is empty after the
        operation, remove it.
        """
        pPr = self._get_or_add_pPr()
        pPr.style = style
        if pPr.countchildren() == 0:
            self.remove(pPr)


class CT_PPr(OxmlBaseElement):
    """
    ``<w:pPr>`` element, containing the properties for a paragraph.
    """
    def __setattr__(self, attr, value):
        """
        Implement setter side of properties. Filters ``__setattr__`` messages
        to ObjectifiedElement base class to intercept messages intended for
        custom property setters.
        """
        if attr == 'style':
            self._set_style(value)
        else:
            super(CT_PPr, self).__setattr__(attr, value)

    @staticmethod
    def new():
        """
        Return a new ``<w:pPr>`` element.
        """
        xml = '<w:pPr %s/>' % nsdecls('w')
        pPr = oxml_fromstring(xml)
        return pPr

    @property
    def style(self):
        """
        String contained in <w:pStyle> child, or None if that element is not
        present.
        """
        if not hasattr(self, 'pStyle'):
            return None
        return self.pStyle.get(qn('w:val'))

    def _set_style(self, style):
        """
        Set w:val attribute of <w:pStyle> child element to *style*, adding a
        new element if necessary. If *style* is |None|, remove the <w:pStyle>
        element if present.
        """
        if not hasattr(self, 'pStyle'):
            pStyle = _Element('w:pStyle')
            self.insert(0, pStyle)
        if style is None:
            self.remove(self.pStyle)
        else:
            self.pStyle.set(qn('w:val'), style)


class CT_R(OxmlBaseElement):
    """
    ``<w:r>`` element, containing the properties and text for a run.
    """
    @staticmethod
    def new():
        """
        Return a new ``<w:r>`` element.
        """
        xml = '<w:r %s/>' % nsdecls('w')
        return oxml_fromstring(xml)

    def add_t(self, text):
        """
        Return a newly added CT_T (<w:t>) element containing *text*.
        """
        t = CT_Text.new(text)
        self.append(t)
        return t

    @property
    def t_elms(self):
        """
        Sequence of the <w:t> elements in this paragraph.
        """
        if not hasattr(self, 't'):
            return ()
        return tuple([t for t in self.t])


class CT_Text(OxmlBaseElement):
    """
    ``<w:t>`` element, containing a sequence of characters within a run.
    """
    @staticmethod
    def new(text):
        """
        Return a new ``<w:t>`` element.
        """
        xml = '<w:t %s>%s</w:t>' % (nsdecls('w'), text)
        return oxml_fromstring(xml)
