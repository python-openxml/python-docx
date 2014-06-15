# encoding: utf-8

"""
Provides StylesPart and related objects
"""

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

from ..opc.package import Part
from ..oxml import parse_xml
from ..shared import lazyproperty


class StylesPart(Part):
    """
    Proxy for the styles.xml part containing style definitions for a document
    or glossary.
    """
    def __init__(self, partname, content_type, element, package):
        super(StylesPart, self).__init__(
            partname, content_type, element=element, package=package
        )

    @classmethod
    def load(cls, partname, content_type, blob, package):
        """
        Provides PartFactory interface for loading a styles part from a WML
        package.
        """
        styles_elm = parse_xml(blob)
        styles_part = cls(partname, content_type, styles_elm, package)
        return styles_part

    @classmethod
    def new(cls):
        """
        Return newly created empty styles part, containing only the root
        ``<w:styles>`` element.
        """
        raise NotImplementedError

    @lazyproperty
    def styles(self):
        """
        The |_Styles| instance containing the styles (<w:style> element
        proxies) for this styles part.
        """
        return _Styles(self._element)


class _Styles(object):
    """
    Collection of |_Style| instances corresponding to the ``<w:style>``
    elements in a styles part.
    """
    def __init__(self, styles_elm):
        super(_Styles, self).__init__()
        self._styles_elm = styles_elm

    def __len__(self):
        return len(self._styles_elm.style_lst)
