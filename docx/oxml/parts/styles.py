# encoding: utf-8

"""
Custom element classes related to the styles part
"""

from docx.oxml.shared import OxmlBaseElement, qn


class CT_Styles(OxmlBaseElement):
    """
    ``<w:styles>`` element, the root element of a styles part, i.e.
    styles.xml
    """
    @property
    def style_lst(self):
        """
        List of <w:style> child elements.
        """
        return self.findall(qn('w:style'))
