# encoding: utf-8

"""
Custom element classes for shape-related elements like ``<w:inline>``
"""

from docx.oxml.shared import OxmlBaseElement, qn


class CT_Blip(OxmlBaseElement):
    """
    ``<a:blip>`` element, specifies image source and adjustments such as
    alpha and tint.
    """
    @property
    def link(self):
        return self.get(qn('r:link'))


class CT_BlipFillProperties(OxmlBaseElement):
    """
    ``<pic:blipFill>`` element, specifies picture properties
    """
    @property
    def blip(self):
        return self.find(qn('a:blip'))


class CT_GraphicalObject(OxmlBaseElement):
    """
    ``<a:graphic>`` element, container for a DrawingML object
    """
    @property
    def graphicData(self):
        return self.find(qn('a:graphicData'))


class CT_GraphicalObjectData(OxmlBaseElement):
    """
    ``<a:graphicData>`` element, container for the XML of a DrawingML object
    """
    @property
    def pic(self):
        return self.find(qn('pic:pic'))

    @property
    def uri(self):
        return self.get('uri')


class CT_Inline(OxmlBaseElement):
    """
    ``<w:inline>`` element, container for an inline shape.
    """
    @property
    def graphic(self):
        return self.find(qn('a:graphic'))


class CT_Picture(OxmlBaseElement):
    """
    ``<pic:pic>`` element, a DrawingML picture
    """
    @property
    def blipFill(self):
        return self.find(qn('pic:blipFill'))
