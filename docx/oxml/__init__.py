# encoding: utf-8

"""
Initializes oxml sub-package, including registering custom element classes
corresponding to Open XML elements.
"""

from docx.oxml.shared import register_custom_element_class


class ValidationError(Exception):
    """
    Raised when invalid XML is encountered, such as on attempt to access a
    missing required child element
    """


# ===========================================================================
# custom element class mappings
# ===========================================================================

from docx.oxml.parts import CT_Body, CT_Document
register_custom_element_class('w:body', CT_Body)
register_custom_element_class('w:document', CT_Document)

from docx.oxml.table import CT_Row, CT_Tbl, CT_TblGrid, CT_Tc
register_custom_element_class('w:tbl', CT_Tbl)
register_custom_element_class('w:tblGrid', CT_TblGrid)
register_custom_element_class('w:tc', CT_Tc)
register_custom_element_class('w:tr', CT_Row)

from docx.oxml.text import CT_P, CT_PPr, CT_R, CT_String, CT_Text
register_custom_element_class('w:p', CT_P)
register_custom_element_class('w:pPr', CT_PPr)
register_custom_element_class('w:pStyle', CT_String)
register_custom_element_class('w:r', CT_R)
register_custom_element_class('w:t', CT_Text)
