# -*- coding: utf-8 -*-
#
# __init__.py
#
# Copyright (C) 2012, 2013 Steve Canny scanny@cisco.com
#
# This module is part of python-docx and is released under the MIT License:
# http://www.opensource.org/licenses/mit-license.php

from docx.api import Document  # noqa

__version__ = '0.3.0dev1'


from opc import PartFactory
from opc.constants import CONTENT_TYPE as CT

from docx.parts import _Document


PartFactory.part_type_for[CT.WML_DOCUMENT_MAIN] = _Document
