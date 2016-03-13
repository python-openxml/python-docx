# encoding: utf-8

"""
Initializes oxml sub-package, including registering custom element classes
corresponding to Open XML elements.
"""

from __future__ import absolute_import

from lxml import etree

from .ns import NamespacePrefixedTag, nsmap


# configure XML parser
element_class_lookup = etree.ElementNamespaceClassLookup()
oxml_parser = etree.XMLParser(remove_blank_text=True)
oxml_parser.set_element_class_lookup(element_class_lookup)


def parse_xml(xml):
    """
    Return root lxml element obtained by parsing XML character string in
    *xml*, which can be either a Python 2.x string or unicode. The custom
    parser is used, so custom element classes are produced for elements in
    *xml* that have them.
    """
    root_element = etree.fromstring(xml, oxml_parser)
    return root_element


def register_element_cls(tag, cls):
    """
    Register *cls* to be constructed when the oxml parser encounters an
    element with matching *tag*. *tag* is a string of the form
    ``nspfx:tagroot``, e.g. ``'w:document'``.
    """
    nspfx, tagroot = tag.split(':')
    namespace = element_class_lookup.get_namespace(nsmap[nspfx])
    namespace[tagroot] = cls


def OxmlElement(nsptag_str, attrs=None, nsdecls=None):
    """
    Return a 'loose' lxml element having the tag specified by *nsptag_str*.
    *nsptag_str* must contain the standard namespace prefix, e.g. 'a:tbl'.
    The resulting element is an instance of the custom element class for this
    tag name if one is defined. A dictionary of attribute values may be
    provided as *attrs*; they are set if present. All namespaces defined in
    the dict *nsdecls* are declared in the element using the key as the
    prefix and the value as the namespace name. If *nsdecls* is not provided,
    a single namespace declaration is added based on the prefix on
    *nsptag_str*.
    """
    nsptag = NamespacePrefixedTag(nsptag_str)
    if nsdecls is None:
        nsdecls = nsptag.nsmap
    return oxml_parser.makeelement(
        nsptag.clark_name, attrib=attrs, nsmap=nsdecls
    )


# ===========================================================================
# custom element class mappings
# ===========================================================================

from .shared import CT_DecimalNumber, CT_OnOff, CT_String


from .coreprops import CT_CoreProperties
register_element_cls('cp:coreProperties', CT_CoreProperties)

from .document import CT_Body, CT_Document
register_element_cls('w:body',     CT_Body)
register_element_cls('w:document', CT_Document)

from .numbering import (
    CT_Num, CT_Numbering, CT_NumLvl, CT_NumPr
)
register_element_cls('w:abstractNumId', CT_DecimalNumber)
register_element_cls('w:ilvl',          CT_DecimalNumber)
register_element_cls('w:lvlOverride',   CT_NumLvl)
register_element_cls('w:num',           CT_Num)
register_element_cls('w:numId',         CT_DecimalNumber)
register_element_cls('w:numPr',         CT_NumPr)
register_element_cls('w:numbering',     CT_Numbering)
register_element_cls('w:startOverride', CT_DecimalNumber)

from .section import CT_PageMar, CT_PageSz, CT_SectPr, CT_SectType
register_element_cls('w:pgMar',  CT_PageMar)
register_element_cls('w:pgSz',   CT_PageSz)
register_element_cls('w:sectPr', CT_SectPr)
register_element_cls('w:type',   CT_SectType)

from .shape import (
    CT_Blip, CT_BlipFillProperties, CT_GraphicalObject,
    CT_GraphicalObjectData, CT_Inline, CT_NonVisualDrawingProps, CT_Picture,
    CT_PictureNonVisual, CT_Point2D, CT_PositiveSize2D, CT_ShapeProperties,
    CT_Transform2D
)
register_element_cls('a:blip',        CT_Blip)
register_element_cls('a:ext',         CT_PositiveSize2D)
register_element_cls('a:graphic',     CT_GraphicalObject)
register_element_cls('a:graphicData', CT_GraphicalObjectData)
register_element_cls('a:off',         CT_Point2D)
register_element_cls('a:xfrm',        CT_Transform2D)
register_element_cls('pic:blipFill',  CT_BlipFillProperties)
register_element_cls('pic:cNvPr',     CT_NonVisualDrawingProps)
register_element_cls('pic:nvPicPr',   CT_PictureNonVisual)
register_element_cls('pic:pic',       CT_Picture)
register_element_cls('pic:spPr',      CT_ShapeProperties)
register_element_cls('wp:docPr',      CT_NonVisualDrawingProps)
register_element_cls('wp:extent',     CT_PositiveSize2D)
register_element_cls('wp:inline',     CT_Inline)

from .styles import CT_LatentStyles, CT_LsdException, CT_Style, CT_Styles
register_element_cls('w:basedOn',        CT_String)
register_element_cls('w:latentStyles',   CT_LatentStyles)
register_element_cls('w:locked',         CT_OnOff)
register_element_cls('w:lsdException',   CT_LsdException)
register_element_cls('w:name',           CT_String)
register_element_cls('w:next',           CT_String)
register_element_cls('w:qFormat',        CT_OnOff)
register_element_cls('w:semiHidden',     CT_OnOff)
register_element_cls('w:style',          CT_Style)
register_element_cls('w:styles',         CT_Styles)
register_element_cls('w:uiPriority',     CT_DecimalNumber)
register_element_cls('w:unhideWhenUsed', CT_OnOff)

from .table import (
    CT_Row, CT_Tbl, CT_TblGrid, CT_TblGridCol, CT_TblLayoutType, CT_TblPr,
    CT_TblWidth, CT_Tc, CT_TcPr, CT_VMerge
)
register_element_cls('w:bidiVisual', CT_OnOff)
register_element_cls('w:gridCol',    CT_TblGridCol)
register_element_cls('w:gridSpan',   CT_DecimalNumber)
register_element_cls('w:tbl',        CT_Tbl)
register_element_cls('w:tblGrid',    CT_TblGrid)
register_element_cls('w:tblLayout',  CT_TblLayoutType)
register_element_cls('w:tblPr',      CT_TblPr)
register_element_cls('w:tblStyle',   CT_String)
register_element_cls('w:tc',         CT_Tc)
register_element_cls('w:tcPr',       CT_TcPr)
register_element_cls('w:tcW',        CT_TblWidth)
register_element_cls('w:tr',         CT_Row)
register_element_cls('w:vMerge',     CT_VMerge)

from .text.font import (
    CT_Color, CT_Fonts, CT_HpsMeasure, CT_RPr, CT_Underline,
    CT_VerticalAlignRun
)
register_element_cls('w:b',          CT_OnOff)
register_element_cls('w:bCs',        CT_OnOff)
register_element_cls('w:caps',       CT_OnOff)
register_element_cls('w:color',      CT_Color)
register_element_cls('w:cs',         CT_OnOff)
register_element_cls('w:dstrike',    CT_OnOff)
register_element_cls('w:emboss',     CT_OnOff)
register_element_cls('w:i',          CT_OnOff)
register_element_cls('w:iCs',        CT_OnOff)
register_element_cls('w:imprint',    CT_OnOff)
register_element_cls('w:noProof',    CT_OnOff)
register_element_cls('w:oMath',      CT_OnOff)
register_element_cls('w:outline',    CT_OnOff)
register_element_cls('w:rFonts',     CT_Fonts)
register_element_cls('w:rPr',        CT_RPr)
register_element_cls('w:rStyle',     CT_String)
register_element_cls('w:rtl',        CT_OnOff)
register_element_cls('w:shadow',     CT_OnOff)
register_element_cls('w:smallCaps',  CT_OnOff)
register_element_cls('w:snapToGrid', CT_OnOff)
register_element_cls('w:specVanish', CT_OnOff)
register_element_cls('w:strike',     CT_OnOff)
register_element_cls('w:sz',         CT_HpsMeasure)
register_element_cls('w:u',          CT_Underline)
register_element_cls('w:vanish',     CT_OnOff)
register_element_cls('w:vertAlign',  CT_VerticalAlignRun)
register_element_cls('w:webHidden',  CT_OnOff)

from .text.paragraph import CT_P
register_element_cls('w:p', CT_P)

from .text.hyperlink import CT_Hyperlink
register_element_cls('w:hyperlink', CT_Hyperlink)

from .text.parfmt import CT_Ind, CT_Jc, CT_PPr, CT_Spacing
register_element_cls('w:ind',             CT_Ind)
register_element_cls('w:jc',              CT_Jc)
register_element_cls('w:keepLines',       CT_OnOff)
register_element_cls('w:keepNext',        CT_OnOff)
register_element_cls('w:pageBreakBefore', CT_OnOff)
register_element_cls('w:pPr',             CT_PPr)
register_element_cls('w:pStyle',          CT_String)
register_element_cls('w:spacing',         CT_Spacing)
register_element_cls('w:widowControl',    CT_OnOff)

from .text.run import CT_Br, CT_R, CT_Text
register_element_cls('w:br', CT_Br)
register_element_cls('w:r',  CT_R)
register_element_cls('w:t',  CT_Text)
