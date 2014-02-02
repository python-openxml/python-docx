# encoding: utf-8

"""
Custom element classes related to the numbering part
"""

from docx.oxml.shared import OxmlBaseElement


class CT_Numbering(OxmlBaseElement):
    """
    ``<w:numbering>`` element, the root element of a numbering part, i.e.
    numbering.xml
    """
