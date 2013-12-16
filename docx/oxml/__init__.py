# encoding: utf-8

"""
Initializes oxml sub-package, including registering custom element classes
corresponding to Open XML elements.
"""

from docx.oxml.shared import register_custom_element_class


# ===========================================================================
# custom element class mappings
# ===========================================================================

from docx.oxml.parts import CT_Body, CT_Document
register_custom_element_class('w:body',     CT_Body)
register_custom_element_class('w:document', CT_Document)

from docx.oxml.text import CT_P, CT_PPr, CT_R, CT_String, CT_Text
register_custom_element_class('w:p',      CT_P)
register_custom_element_class('w:pPr',    CT_PPr)
register_custom_element_class('w:pStyle', CT_String)
register_custom_element_class('w:r',      CT_R)
register_custom_element_class('w:t',      CT_Text)
