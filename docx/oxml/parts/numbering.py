# encoding: utf-8

"""
Custom element classes related to the numbering part
"""

from docx.oxml.shared import OxmlBaseElement, qn


class CT_Numbering(OxmlBaseElement):
    """
    ``<w:numbering>`` element, the root element of a numbering part, i.e.
    numbering.xml
    """
    @property
    def num_lst(self):
        """
        List of <w:num> child elements.
        """
        return self.findall(qn('w:num'))
