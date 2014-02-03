# encoding: utf-8

"""
Custom element classes related to the styles part
"""

from docx.oxml.shared import OxmlBaseElement


class CT_Styles(OxmlBaseElement):
    """
    ``<w:styles>`` element, the root element of a styles part, i.e.
    styles.xml
    """
