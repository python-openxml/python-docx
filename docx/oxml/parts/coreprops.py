# encoding: utf-8

"""
lxml custom element classes for core properties-related XML elements.
"""

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

from ..xmlchemy import BaseOxmlElement


class CT_CoreProperties(BaseOxmlElement):
    """
    ``<cp:coreProperties>`` element, the root element of the Core Properties
    part stored as ``/docProps/core.xml``. Implements many of the Dublin Core
    document metadata elements. String elements resolve to an empty string
    ('') if the element is not present in the XML. String elements are
    limited in length to 255 unicode characters.
    """
