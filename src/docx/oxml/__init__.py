"""Initializes oxml sub-package.

This including registering custom element classes corresponding to Open XML elements.
"""

from __future__ import annotations

from docx.oxml.drawing import CT_Drawing
from docx.oxml.parser import OxmlElement, parse_xml, register_element_cls
from docx.oxml.shape import (
    CT_Anchor,
    CT_Blip,
    CT_BlipFillProperties,
    CT_GraphicalObject,
    CT_GraphicalObjectData,
    CT_Inline,
    CT_NonVisualDrawingProps,
    CT_Picture,
    CT_PictureNonVisual,
    CT_Point2D,
    CT_PositiveSize2D,
    CT_ShapeProperties,
    CT_Transform2D,
)
from docx.oxml.shared import CT_DecimalNumber, CT_OnOff, CT_String
from docx.oxml.text.hyperlink import CT_Hyperlink
from docx.oxml.text.pagebreak import CT_LastRenderedPageBreak
from docx.oxml.text.run import (
    CT_R,
    CT_Br,
    CT_Cr,
    CT_NoBreakHyphen,
    CT_PTab,
    CT_Text,
)

# -- `OxmlElement` and `parse_xml()` are not used in this module but several downstream
# -- "extension" packages expect to find them here and there's no compelling reason
# -- not to republish them here so those keep working.
__all__ = ["OxmlElement", "parse_xml"]

# ---------------------------------------------------------------------------
# DrawingML-related elements

register_element_cls("a:blip", CT_Blip)
register_element_cls("a:ext", CT_PositiveSize2D)
register_element_cls("a:graphic", CT_GraphicalObject)
register_element_cls("a:graphicData", CT_GraphicalObjectData)
register_element_cls("a:off", CT_Point2D)
register_element_cls("a:xfrm", CT_Transform2D)
register_element_cls("pic:blipFill", CT_BlipFillProperties)
register_element_cls("pic:cNvPr", CT_NonVisualDrawingProps)
register_element_cls("pic:nvPicPr", CT_PictureNonVisual)
register_element_cls("pic:pic", CT_Picture)
register_element_cls("pic:spPr", CT_ShapeProperties)
register_element_cls("w:drawing", CT_Drawing)
register_element_cls("wp:anchor", CT_Anchor)
register_element_cls("wp:docPr", CT_NonVisualDrawingProps)
register_element_cls("wp:extent", CT_PositiveSize2D)
register_element_cls("wp:inline", CT_Inline)

# ---------------------------------------------------------------------------
# hyperlink-related elements

register_element_cls("w:hyperlink", CT_Hyperlink)

# ---------------------------------------------------------------------------
# text-related elements

register_element_cls("w:br", CT_Br)
register_element_cls("w:cr", CT_Cr)
register_element_cls("w:lastRenderedPageBreak", CT_LastRenderedPageBreak)
register_element_cls("w:noBreakHyphen", CT_NoBreakHyphen)
register_element_cls("w:ptab", CT_PTab)
register_element_cls("w:r", CT_R)
register_element_cls("w:t", CT_Text)

# ---------------------------------------------------------------------------
# header/footer-related mappings

register_element_cls("w:evenAndOddHeaders", CT_OnOff)
register_element_cls("w:titlePg", CT_OnOff)

# ---------------------------------------------------------------------------
# other custom element class mappings

from .coreprops import CT_CoreProperties  # noqa

register_element_cls("cp:coreProperties", CT_CoreProperties)

from .document import CT_Body, CT_Document  # noqa

register_element_cls("w:body", CT_Body)
register_element_cls("w:document", CT_Document)

from .numbering import CT_Num, CT_Numbering, CT_NumLvl, CT_NumPr  # noqa

register_element_cls("w:abstractNumId", CT_DecimalNumber)
register_element_cls("w:ilvl", CT_DecimalNumber)
register_element_cls("w:lvlOverride", CT_NumLvl)
register_element_cls("w:num", CT_Num)
register_element_cls("w:numId", CT_DecimalNumber)
register_element_cls("w:numPr", CT_NumPr)
register_element_cls("w:numbering", CT_Numbering)
register_element_cls("w:startOverride", CT_DecimalNumber)

from .section import (  # noqa
    CT_HdrFtr,
    CT_HdrFtrRef,
    CT_PageMar,
    CT_PageSz,
    CT_SectPr,
    CT_SectType,
)

register_element_cls("w:footerReference", CT_HdrFtrRef)
register_element_cls("w:ftr", CT_HdrFtr)
register_element_cls("w:hdr", CT_HdrFtr)
register_element_cls("w:headerReference", CT_HdrFtrRef)
register_element_cls("w:pgMar", CT_PageMar)
register_element_cls("w:pgSz", CT_PageSz)
register_element_cls("w:sectPr", CT_SectPr)
register_element_cls("w:type", CT_SectType)

from .settings import CT_Settings  # noqa

register_element_cls("w:settings", CT_Settings)

from .styles import CT_LatentStyles, CT_LsdException, CT_Style, CT_Styles  # noqa

register_element_cls("w:basedOn", CT_String)
register_element_cls("w:latentStyles", CT_LatentStyles)
register_element_cls("w:locked", CT_OnOff)
register_element_cls("w:lsdException", CT_LsdException)
register_element_cls("w:name", CT_String)
register_element_cls("w:next", CT_String)
register_element_cls("w:qFormat", CT_OnOff)
register_element_cls("w:semiHidden", CT_OnOff)
register_element_cls("w:style", CT_Style)
register_element_cls("w:styles", CT_Styles)
register_element_cls("w:uiPriority", CT_DecimalNumber)
register_element_cls("w:unhideWhenUsed", CT_OnOff)

from .table import (  # noqa
    CT_Height,
    CT_Row,
    CT_Tbl,
    CT_TblGrid,
    CT_TblGridCol,
    CT_TblLayoutType,
    CT_TblPr,
    CT_TblWidth,
    CT_Tc,
    CT_TcPr,
    CT_TrPr,
    CT_VMerge,
    CT_VerticalJc,
)

register_element_cls("w:bidiVisual", CT_OnOff)
register_element_cls("w:gridCol", CT_TblGridCol)
register_element_cls("w:gridSpan", CT_DecimalNumber)
register_element_cls("w:tbl", CT_Tbl)
register_element_cls("w:tblGrid", CT_TblGrid)
register_element_cls("w:tblLayout", CT_TblLayoutType)
register_element_cls("w:tblPr", CT_TblPr)
register_element_cls("w:tblStyle", CT_String)
register_element_cls("w:tc", CT_Tc)
register_element_cls("w:tcPr", CT_TcPr)
register_element_cls("w:tcW", CT_TblWidth)
register_element_cls("w:tr", CT_Row)
register_element_cls("w:trHeight", CT_Height)
register_element_cls("w:trPr", CT_TrPr)
register_element_cls("w:vAlign", CT_VerticalJc)
register_element_cls("w:vMerge", CT_VMerge)

from .text.font import (  # noqa
    CT_Color,
    CT_Fonts,
    CT_Highlight,
    CT_HpsMeasure,
    CT_RPr,
    CT_Underline,
    CT_VerticalAlignRun,
)

register_element_cls("w:b", CT_OnOff)
register_element_cls("w:bCs", CT_OnOff)
register_element_cls("w:caps", CT_OnOff)
register_element_cls("w:color", CT_Color)
register_element_cls("w:cs", CT_OnOff)
register_element_cls("w:dstrike", CT_OnOff)
register_element_cls("w:emboss", CT_OnOff)
register_element_cls("w:highlight", CT_Highlight)
register_element_cls("w:i", CT_OnOff)
register_element_cls("w:iCs", CT_OnOff)
register_element_cls("w:imprint", CT_OnOff)
register_element_cls("w:noProof", CT_OnOff)
register_element_cls("w:oMath", CT_OnOff)
register_element_cls("w:outline", CT_OnOff)
register_element_cls("w:rFonts", CT_Fonts)
register_element_cls("w:rPr", CT_RPr)
register_element_cls("w:rStyle", CT_String)
register_element_cls("w:rtl", CT_OnOff)
register_element_cls("w:shadow", CT_OnOff)
register_element_cls("w:smallCaps", CT_OnOff)
register_element_cls("w:snapToGrid", CT_OnOff)
register_element_cls("w:specVanish", CT_OnOff)
register_element_cls("w:strike", CT_OnOff)
register_element_cls("w:sz", CT_HpsMeasure)
register_element_cls("w:u", CT_Underline)
register_element_cls("w:vanish", CT_OnOff)
register_element_cls("w:vertAlign", CT_VerticalAlignRun)
register_element_cls("w:webHidden", CT_OnOff)

from .text.paragraph import CT_P  # noqa

register_element_cls("w:p", CT_P)

from .text.parfmt import (  # noqa
    CT_Ind,
    CT_Jc,
    CT_PPr,
    CT_Spacing,
    CT_TabStop,
    CT_TabStops,
)

register_element_cls("w:ind", CT_Ind)
register_element_cls("w:jc", CT_Jc)
register_element_cls("w:keepLines", CT_OnOff)
register_element_cls("w:keepNext", CT_OnOff)
register_element_cls("w:pageBreakBefore", CT_OnOff)
register_element_cls("w:pPr", CT_PPr)
register_element_cls("w:pStyle", CT_String)
register_element_cls("w:spacing", CT_Spacing)
register_element_cls("w:tab", CT_TabStop)
register_element_cls("w:tabs", CT_TabStops)
register_element_cls("w:widowControl", CT_OnOff)
