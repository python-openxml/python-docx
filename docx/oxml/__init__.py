# encoding: utf-8

"""
Initializes oxml sub-package, including registering custom element classes
corresponding to Open XML elements.
"""

from docx.oxml.shared import register_custom_element_class


# ===========================================================================
# custom element class mappings
# ===========================================================================

from docx.oxml.shared import CT_DecimalNumber, CT_OnOff, CT_String

from docx.oxml.shape import (
    CT_Blip, CT_BlipFillProperties, CT_GraphicalObject,
    CT_GraphicalObjectData, CT_Inline, CT_Picture, CT_PositiveSize2D
)
register_custom_element_class('a:blip', CT_Blip)
register_custom_element_class('a:graphic', CT_GraphicalObject)
register_custom_element_class('a:graphicData', CT_GraphicalObjectData)
register_custom_element_class('pic:blipFill', CT_BlipFillProperties)
register_custom_element_class('pic:pic', CT_Picture)
register_custom_element_class('wp:extent', CT_PositiveSize2D)
register_custom_element_class('wp:inline', CT_Inline)

from docx.oxml.parts.document import CT_Body, CT_Document
register_custom_element_class('w:body', CT_Body)
register_custom_element_class('w:document', CT_Document)

from docx.oxml.parts.numbering import (
    CT_Num, CT_Numbering, CT_NumLvl, CT_NumPr
)
register_custom_element_class('w:abstractNumId', CT_DecimalNumber)
register_custom_element_class('w:ilvl', CT_DecimalNumber)
register_custom_element_class('w:lvlOverride', CT_NumLvl)
register_custom_element_class('w:num', CT_Num)
register_custom_element_class('w:numId', CT_DecimalNumber)
register_custom_element_class('w:numPr', CT_NumPr)
register_custom_element_class('w:numbering', CT_Numbering)

from docx.oxml.parts.styles import CT_Style, CT_Styles
register_custom_element_class('w:style', CT_Style)
register_custom_element_class('w:styles', CT_Styles)

from docx.oxml.table import CT_Row, CT_Tbl, CT_TblGrid, CT_TblPr, CT_Tc
register_custom_element_class('w:tbl', CT_Tbl)
register_custom_element_class('w:tblGrid', CT_TblGrid)
register_custom_element_class('w:tblPr', CT_TblPr)
register_custom_element_class('w:tblStyle', CT_String)
register_custom_element_class('w:tc', CT_Tc)
register_custom_element_class('w:tr', CT_Row)

from docx.oxml.text import (
    CT_Br, CT_P, CT_PPr, CT_R, CT_RPr, CT_Text, CT_Underline
)
register_custom_element_class('w:b', CT_OnOff)
register_custom_element_class('w:bCs', CT_OnOff)
register_custom_element_class('w:br', CT_Br)
register_custom_element_class('w:caps', CT_OnOff)
register_custom_element_class('w:cs', CT_OnOff)
register_custom_element_class('w:dstrike', CT_OnOff)
register_custom_element_class('w:emboss', CT_OnOff)
register_custom_element_class('w:i', CT_OnOff)
register_custom_element_class('w:iCs', CT_OnOff)
register_custom_element_class('w:imprint', CT_OnOff)
register_custom_element_class('w:noProof', CT_OnOff)
register_custom_element_class('w:oMath', CT_OnOff)
register_custom_element_class('w:outline', CT_OnOff)
register_custom_element_class('w:p', CT_P)
register_custom_element_class('w:pPr', CT_PPr)
register_custom_element_class('w:pStyle', CT_String)
register_custom_element_class('w:r', CT_R)
register_custom_element_class('w:rPr', CT_RPr)
register_custom_element_class('w:rStyle', CT_String)
register_custom_element_class('w:rtl', CT_OnOff)
register_custom_element_class('w:shadow', CT_OnOff)
register_custom_element_class('w:smallCaps', CT_OnOff)
register_custom_element_class('w:snapToGrid', CT_OnOff)
register_custom_element_class('w:specVanish', CT_OnOff)
register_custom_element_class('w:strike', CT_OnOff)
register_custom_element_class('w:t', CT_Text)
register_custom_element_class('w:u', CT_Underline)
register_custom_element_class('w:vanish', CT_OnOff)
register_custom_element_class('w:webHidden', CT_OnOff)
