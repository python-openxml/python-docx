# -*- coding: utf-8 -*-
#
# oxml/__init__.py
#
# Copyright (C) 2012, 2013 Steve Canny scanny@cisco.com
#
# This module is part of python-docx and is released under the MIT License:
# http://www.opensource.org/licenses/mit-license.php

"""
Initializes oxml sub-package, including registering custom element classes
corresponding to Open XML elements.
"""

from docx.oxml.base import register_custom_element_class
from docx.oxml.parts import CT_Body, CT_Document
from docx.oxml.text import CT_P, CT_PPr, CT_R, CT_Text


# ===========================================================================
# custom element class mappings
# ===========================================================================

register_custom_element_class('w:body',     CT_Body)
register_custom_element_class('w:document', CT_Document)
register_custom_element_class('w:p',        CT_P)
register_custom_element_class('w:pPr',      CT_PPr)
register_custom_element_class('w:r',        CT_R)
register_custom_element_class('w:t',        CT_Text)
